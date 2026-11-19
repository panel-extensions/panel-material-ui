import panel as pn
import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui import (
    Button,
    Checkbox,
    Column,
    Compiled,
    Page,
    Row,
    TextInput,
    Typography,
)

pytestmark = pytest.mark.ui


def test_compiled_click_updates_other_node(page):
    status = Typography("clicks: 0", css_classes=["status"])
    button = Button(label="Run")
    button.on_click(lambda event: status.param.update(object=f"clicks: {button.clicks}"))
    serve_component(page, Compiled(Column(status, Row(button))))

    page.locator(".MuiButton-root").click()
    expect(page.locator(".status")).to_contain_text("clicks: 1")
    page.locator(".MuiButton-root").click()
    expect(page.locator(".status")).to_contain_text("clicks: 2")


def test_compiled_patch_keeps_sibling_dom(page):
    first, second = Button(label="First"), Button(label="Second")
    serve_component(page, Compiled(Column(Row(first, second))))

    buttons = page.locator(".MuiButton-root")
    expect(buttons).to_have_count(2)
    handle = buttons.nth(1).element_handle()
    first.label = "Renamed"
    expect(buttons.nth(0)).to_have_text("Renamed")
    assert handle.evaluate("el => el.isConnected")


def test_compiled_text_input_syncs_both_ways(page):
    text = TextInput(value="a")
    serve_component(page, Compiled(Column(text)))

    field = page.locator("input")
    expect(field).to_have_value("a")
    field.fill("typed")
    field.press("Enter")
    wait_until(lambda: text.value == "typed", page)
    text.value = "from python"
    expect(field).to_have_value("from python")


def test_compiled_checkbox_syncs_both_ways(page):
    checkbox = Checkbox(label="On", value=False)
    serve_component(page, Compiled(Column(checkbox)))

    box = page.locator("input[type='checkbox']")
    box.click()
    wait_until(lambda: checkbox.value, page)
    checkbox.value = False
    expect(box).not_to_be_checked()


def test_compiled_visible_toggle(page):
    button = Button(label="Run")
    serve_component(page, Compiled(Column(Row(button))))

    expect(page.locator(".MuiButton-root")).to_be_visible()
    button.visible = False
    expect(page.locator(".MuiButton-root")).to_be_hidden()
    button.visible = True
    expect(page.locator(".MuiButton-root")).to_be_visible()


def test_compiled_add_and_remove_children(page):
    inner = Column(Button(label="A"))
    serve_component(page, Compiled(Column(Row(inner))))

    buttons = page.locator(".MuiButton-root")
    expect(buttons).to_have_count(1)
    added = Button(label="B")
    inner.append(added)
    expect(buttons).to_have_count(2)
    added.label = "C"
    expect(buttons.nth(1)).to_have_text("C")
    inner.remove(added)
    expect(buttons).to_have_count(1)


def test_compiled_fallback_children(page):
    inner = Column(pn.pane.Markdown("classic one", css_classes=["one"]))
    serve_component(page, Compiled(Column(Row(inner), Button(label="Run"))))

    expect(page.locator(".one p")).to_have_text("classic one")
    inner.append(pn.pane.Markdown("classic two", css_classes=["two"]))
    expect(page.locator(".two p")).to_have_text("classic two")
    expect(page.locator(".one p")).to_have_text("classic one")
    expect(page.locator(".MuiButton-root")).to_have_count(1)


def test_compiled_layout_change_rebuilds(page):
    button = Button(label="Run", width=120)
    other = Button(label="Other")
    serve_component(page, Compiled(Column(Row(button, other))))

    buttons = page.locator(".MuiButton-root")
    expect(buttons).to_have_count(2)
    button.width = 300
    wait_until(lambda: buttons.nth(0).bounding_box()["width"] > 250, page)
    other.label = "Renamed"
    expect(buttons.nth(1)).to_have_text("Renamed")


def test_compiled_recovers_from_missed_patches(page):
    button = Button(label="Run")
    compiled = Compiled(Column(Row(button)))
    serve_component(page, compiled)

    expect(page.locator(".MuiButton-root")).to_have_text("Run")
    # Skips a revision, as if a patch had been sent before the view listened.
    compiled._rev += 1
    button.label = "Missed"
    expect(page.locator(".MuiButton-root")).to_have_text("Missed")


def test_compiled_page(page):
    status = Typography("clicks: 0", css_classes=["status"])
    button = Button(label="Run")
    button.on_click(lambda event: status.param.update(object=f"clicks: {button.clicks}"))
    serve_component(page, Compiled(Page(main=[status, button], sidebar=[Checkbox(label="On")], title="Compiled page")))

    expect(page.locator(".title")).to_have_text("Compiled page")
    expect(page.locator("input[type='checkbox']")).to_have_count(1)
    page.locator(".MuiButton-root").click()
    expect(page.locator(".status")).to_contain_text("clicks: 1")


def test_compiled_focus(page):
    text = TextInput(label="Name")
    serve_component(page, Compiled(Column(Button(label="Run"), text)))
    expect(page.locator(".MuiInputBase-input")).to_have_count(1)

    text.focus()

    expect(page.locator(".MuiInputBase-input")).to_be_focused()


def test_compiled_header_inverts_theme(page):
    pg = Page(header=[Button(label="Action", variant="contained")], main=[Button(label="Main", variant="contained")])
    serve_component(page, Compiled(pg))

    expect(page.get_by_role("button", name="Action")).to_have_css("background-color", "rgb(255, 255, 255)")
    expect(page.get_by_role("button", name="Main")).to_have_css("background-color", "rgb(25, 118, 210)")
