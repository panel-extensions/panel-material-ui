import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import RadioBoxGroup
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
def test_radio_box_group_color(page, color):
    widget = RadioBoxGroup(name='RadioBoxGroup test', options=["Option 1", "Option 2", "Option 3"], color=color)
    serve_component(page, widget)

    expect(page.locator(".radio-box-group")).to_have_count(1)
    expect(page.locator(f".MuiRadio-color{color.capitalize()}")).to_have_count(len(widget.options))

@pytest.mark.parametrize('inline', [True, False])
def test_radio_box_group_orientation(page, inline):
    widget = RadioBoxGroup(name='RadioBoxGroup test', options=["Option 1", "Option 2", "Option 3"], inline=inline)
    serve_component(page, widget)

    expect(page.locator(".radio-box-group")).to_have_count(1)
    if inline:
        rbg_orient = page.locator(".MuiRadioGroup-row")
        expect(rbg_orient).to_have_count(1)
