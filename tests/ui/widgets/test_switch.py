import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import Switch
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_switch(page):
    widget = Switch(label='Works with the tools you know and love', value=True)
    serve_component(page, widget)
    expect(page.locator('.switch')).to_have_count(1)

def test_switch_focus(page):
    widget = Switch(label='Test Switch', value=True)
    serve_component(page, widget)
    switch = page.locator('.MuiSwitch-input')
    expect(switch).to_have_count(1)
    widget.focus()
    expect(switch).to_be_focused()
