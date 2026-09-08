import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import ColorMap
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_color_map_renders_palette(page):
    widget = ColorMap(label="Palette", options={"Warm": ["#fff", "#f00"], "Cool": ["#fff", "#00f"]})
    serve_component(page, widget)
    expect(page.locator(".MuiSelect-select")).to_have_count(1)


def test_color_map_can_select_palette(page):
    widget = ColorMap(options={"Warm": ["#fff", "#f00"], "Cool": ["#fff", "#00f"]}, value_name="Warm")
    serve_component(page, widget)
    select = page.locator(".MuiSelect-select")
    expect(select).to_have_count(1)
    expect(select).to_contain_text("Warm")
    selected_swatch = select.locator("[aria-hidden=true]")
    expect(selected_swatch).to_have_count(1)
    assert selected_swatch.evaluate("el => getComputedStyle(el).backgroundImage != 'none'")

    page.locator(".MuiSelect-select").click()
    page.locator("[role=option]").filter(has_text="Cool").click()
    expect(page.locator(".MuiSelect-select")).to_contain_text("Cool")


def test_color_map_selected_label_is_below_swatch(page):
    long_name = "A very long palette name that should stay inside the control"
    widget = ColorMap(options={long_name: ["#fff", "#f00"]}, value_name=long_name)
    serve_component(page, widget)

    select = page.locator(".MuiSelect-select")
    swatch = select.locator("[aria-hidden=true]")
    label = select.locator("span").last
    swatch_box = swatch.bounding_box()
    label_box = label.bounding_box()
    select_box = select.bounding_box()

    assert swatch_box is not None
    assert label_box is not None
    assert select_box is not None
    assert label_box["y"] >= swatch_box["y"] + swatch_box["height"]
    assert label_box["x"] + label_box["width"] <= select_box["x"] + select_box["width"]


def test_color_map_menu_options_have_visible_swatches(page):
    options = {"Warm": ["#fff", "#f00"], "Cool": ["#fff", "#00f"]}
    serve_component(page, ColorMap(options=options, value_name="Warm"))

    select = page.locator(".MuiSelect-select")
    expect(select).to_have_count(1)
    expect(select).to_contain_text("Warm")
    selected_swatch = select.locator("[aria-hidden=true]")
    expect(selected_swatch).to_have_count(1)
    assert selected_swatch.evaluate("el => getComputedStyle(el).backgroundImage != 'none'")

    page.locator(".MuiSelect-select").click()
    swatches = page.locator("[role=option] > [aria-hidden=true]")

    expect(swatches).to_have_count(len(options))
    for index in range(len(options)):
        swatch = swatches.nth(index)
        box = swatch.bounding_box()
        assert box["width"] > 0
        assert box["height"] > 0
        assert swatch.evaluate("el => getComputedStyle(el).backgroundImage != 'none'")
