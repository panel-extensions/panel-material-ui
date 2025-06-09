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
