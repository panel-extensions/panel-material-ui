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


def test_toggle_icon_active_icon_not_outlined(page):
    # When an active_icon is provided, the inactive icon should NOT be
    # forced to the outlined variant.
    widget = ToggleIcon(icon="thumb_down", active_icon="thumb_up", size="small")
    serve_component(page, widget)

    icon = page.locator('.MuiCheckbox-root .material-icons')
    expect(icon).to_have_count(1)
    expect(icon).to_have_text("thumb_down")
    expect(page.locator('.MuiCheckbox-root .material-icons-outlined')).to_have_count(0)


def test_toggle_icon_no_active_icon_is_outlined(page):
    # Without an active_icon, the inactive icon defaults to the outlined variant.
    widget = ToggleIcon(icon="thumb_down", size="small")
    serve_component(page, widget)

    icon = page.locator('.MuiCheckbox-root .material-icons-outlined')
    expect(icon).to_have_count(1)
    expect(icon).to_have_text("thumb_down")


def test_toggle_icon_explicit_outlined_suffix_not_doubled(page):
    # An icon name already ending in _outlined should render outlined exactly
    # once, not have the default variant re-appended.
    widget = ToggleIcon(icon="thumb_down_outlined", size="small")
    serve_component(page, widget)

    icon = page.locator('.MuiCheckbox-root .material-icons-outlined')
    expect(icon).to_have_count(1)
    expect(icon).to_have_text("thumb_down")


def test_toggle_icon_rounded_suffix_preserved(page):
    # A non-outlined variant suffix must be preserved, not overridden by the
    # outlined default applied when no active_icon is set.
    widget = ToggleIcon(icon="thumb_down_rounded", size="small")
    serve_component(page, widget)

    icon = page.locator('.MuiCheckbox-root .material-icons-round')
    expect(icon).to_have_count(1)
    expect(icon).to_have_text("thumb_down")
    expect(page.locator('.MuiCheckbox-root .material-icons-outlined')).to_have_count(0)
