import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import ToggleIcon
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_toggle_icon(page):
    widget = ToggleIcon(icon="thumb-up", active_icon="thumb-down", size="small", description="Like")
    serve_component(page, widget)

    expect(page.locator('.toggle-icon')).to_have_count(1)
    icon = page.locator('.MuiCheckbox-root')
    expect(icon).to_have_text("thumb-up")
    icon.click()
    expect(icon).to_have_text("thumb-down")
