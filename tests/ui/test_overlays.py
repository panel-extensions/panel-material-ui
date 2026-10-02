import pytest

pytest.importorskip("playwright")

from panel import Column
from panel.pane import HTML
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Dialog
from panel_material_ui.widgets import AutocompleteInput, MenuButton, Select

pytestmark = pytest.mark.ui

# document.elementFromPoint stops at shadow hosts, so drill into each shadow root.
HIT_TEST = """([x, y]) => {
  let root = document
  let hit = null
  while (root) {
    const next = root.elementFromPoint(x, y)
    if (next == null || next === hit) { break }
    hit = next
    root = next.shadowRoot
  }
  return hit?.closest('[role="option"], [role="menuitem"]')?.textContent ?? null
}"""


def hit_text(page, locator):
    box = locator.bounding_box()
    return page.evaluate(HIT_TEST, [box["x"] + box["width"] / 2, box["y"] + box["height"] / 2])


def test_select_menu_above_later_stacking_context(page):
    select = Select(options=["A", "B", "C", "D"], value="A")
    cover = HTML(
        "", height=300, sizing_mode="stretch_width",
        styles={"position": "relative", "z-index": "2", "background": "red"},
    )
    serve_component(page, Column(
        Column(select, styles={"position": "relative", "z-index": "1"}), cover, width=300,
    ))

    page.locator(".MuiSelect-select").click()
    option = page.locator(".MuiMenuItem-root", has_text="D")
    expect(option).to_be_visible()
    assert hit_text(page, option) == "D"
    option.click()
    expect(page.locator(".MuiMenuItem-root")).to_have_count(0)
    wait_until(lambda: select.value == "D", page)


def test_autocomplete_listbox_not_clipped_by_scroll_container(page):
    options = [f"Option {i}" for i in range(5)]
    widget = AutocompleteInput(options=options, min_characters=0)
    serve_component(page, Column(widget, scroll=True, height=70, width=300))

    page.locator(".MuiInputBase-input").click()
    option = page.locator(".MuiAutocomplete-option", has_text="Option 4")
    expect(option).to_be_visible()
    assert hit_text(page, option) == "Option 4"


def test_menu_positioned_under_anchor_inside_transformed_ancestor(page):
    widget = MenuButton(items=[{"label": "One"}, {"label": "Two"}], label="Menu")
    serve_component(page, Column(widget, styles={"transform": "translate(150px, 100px)"}))

    button = page.locator(".MuiButton-root")
    button.click()
    item = page.locator(".MuiMenuItem-root", has_text="One")
    expect(item).to_be_visible()
    button_box, item_box = button.bounding_box(), item.bounding_box()
    assert abs(item_box["y"] - (button_box["y"] + button_box["height"])) < 30
    assert item_box["x"] < button_box["x"] + button_box["width"]
    assert item_box["x"] + item_box["width"] > button_box["x"]
    assert hit_text(page, item) == "One"


def test_select_menu_inside_dialog_stacks_above_dialog(page):
    select = Select(options=["A", "B", "C"], value="A")
    serve_component(page, Dialog(select, open=True))

    page.locator(".MuiSelect-select").click()
    option = page.locator(".MuiMenuItem-root", has_text="C")
    expect(option).to_be_visible()
    assert hit_text(page, option) == "C"
    option.click()
    wait_until(lambda: select.value == "C", page)


def test_overlay_layers_removed_after_close(page):
    serve_component(page, Select(options=["A", "B"], value="A"))
    expect(page.locator(".MuiSelect-select")).to_be_visible()
    expect(page.locator("[data-pmui-layer]")).to_have_count(0)

    for _ in range(3):
        page.locator(".MuiSelect-select").click()
        expect(page.locator(".MuiMenuItem-root")).to_have_count(2)
        expect(page.locator("[data-pmui-layer]")).to_have_count(1)
        page.keyboard.press("Escape")
        expect(page.locator(".MuiMenuItem-root")).to_have_count(0)
        expect(page.locator("[data-pmui-layer]")).to_have_count(0)
