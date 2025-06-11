import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import RadioButtonGroup
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('button_type', ["primary", "secondary", "error", "info", "success", "warning"])
def test_radio_button_group_color(page, button_type):
    widget = RadioButtonGroup(
        name='RadioButtonGroup test',
        options=["Option 1", "Option 2", "Option 3"],
        button_type=button_type
    )
    serve_component(page, widget)

    expect(page.locator(".radio-button-group")).to_have_count(1)
    if button_type == "error":
        option_color = page.locator(f".Mui-{button_type}")
    else:
        option_color = page.locator(f".MuiToggleButton-{button_type}")
    expect(option_color).to_have_count(len(widget.options))

@pytest.mark.parametrize('orientation', ["horizontal", "vertical"])
def test_radio_button_group_orientation(page, orientation):
    widget = RadioButtonGroup(
        name='RadioButtonGroup test',
        options=["Option 1", "Option 2", "Option 3"],
        orientation=orientation
    )
    serve_component(page, widget)

    expect(page.locator(".radio-button-group")).to_have_count(1)
    expect(page.locator(f".MuiToggleButtonGroup-{orientation}")).to_have_count(1)

@pytest.mark.parametrize('size', ["small", "medium", "large"])
def test_radio_button_group_size(page, size):
    widget = RadioButtonGroup(
        name='RadioButtonGroup test',
        options=["Option 1", "Option 2", "Option 3"],
        size=size
    )
    serve_component(page, widget)

    expect(page.locator(".radio-button-group")).to_have_count(1)
    expect(page.locator(f".MuiToggleButton-size{size.capitalize()}")).to_have_count(len(widget.options))
