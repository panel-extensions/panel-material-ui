import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Checkbox
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_checkbox(page):
    widget = Checkbox(label='Works with the tools you know and love', value=True)
    serve_component(page, widget)
    expect(page.locator('.checkbox')).to_have_count(1)

def test_checkbox_basic_functionality(page):
    widget = Checkbox(label='Test Checkbox', value=False)
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.checkbox')).to_have_count(1)
    expect(page.locator('.MuiCheckbox-root')).to_have_count(1)
    expect(page.locator('.MuiFormControlLabel-root')).to_have_text('Test Checkbox')
    expect(page.locator('.MuiCheckbox-root')).not_to_be_checked()

    # Click to check
    page.locator('.MuiCheckbox-root').click()
    wait_until(lambda: widget.value is True, page)
    expect(page.locator('.MuiCheckbox-root')).to_be_checked()

    # Click to uncheck
    page.locator('.MuiCheckbox-root').click()
    wait_until(lambda: widget.value is False, page)
    expect(page.locator('.MuiCheckbox-root')).not_to_be_checked()

@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
def test_checkbox_colors(page, color):
    widget = Checkbox(label='Test Checkbox', color=color)
    serve_component(page, widget)

    expect(page.locator('.checkbox')).to_have_count(1)
    expect(page.locator(f'.MuiCheckbox-color{color.capitalize()}')).to_have_count(1)

@pytest.mark.parametrize('size', ["small", "medium", "large"])
def test_checkbox_sizes(page, size):
    widget = Checkbox(label='Test Checkbox', size=size)
    serve_component(page, widget)

    expect(page.locator('.checkbox')).to_have_count(1)
    expect(page.locator(f'.MuiCheckbox-size{size.capitalize()}')).to_have_count(1)

def test_checkbox_disabled_state(page):
    widget = Checkbox(label='Test Checkbox', disabled=True)
    serve_component(page, widget)

    expect(page.locator('.checkbox')).to_have_count(1)
    expect(page.locator('.MuiCheckbox-root')).to_be_disabled()

def test_checkbox_indeterminate_state(page):
    widget = Checkbox(label='Test Checkbox', indeterminate=True, value=None)
    serve_component(page, widget)

    expect(page.locator('.checkbox')).to_have_count(1)
    expect(page.locator('.PrivateSwitchBase-input')).to_have_attribute('data-indeterminate', 'true')

    # Click should change to checked state
    page.locator('.MuiCheckbox-root').click()
    wait_until(lambda: widget.value is True, page)
    expect(page.locator('.MuiCheckbox-root')).to_be_checked()
    expect(page.locator('.PrivateSwitchBase-input')).not_to_have_attribute('data-indeterminate', 'true')

def test_checkbox_value_updates(page):
    widget = Checkbox(label='Test Checkbox', value=False)
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.MuiCheckbox-root')).not_to_be_checked()

    # Update value programmatically
    widget.value = True
    wait_until(lambda: page.locator('.MuiCheckbox-root').is_checked(), page)

    # Update to indeterminate
    widget.indeterminate = True
    widget.value = None
    wait_until(lambda: page.locator('.PrivateSwitchBase-input').get_attribute('data-indeterminate') == 'true', page)

def test_checkbox_label_click(page):
    widget = Checkbox(label='Clickable Label', value=False)
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.MuiCheckbox-root')).not_to_be_checked()

    # Click label to check
    page.locator('.MuiFormControlLabel-root').click()
    wait_until(lambda: widget.value is True, page)
    expect(page.locator('.MuiCheckbox-root')).to_be_checked()

    # Click label to uncheck
    page.locator('.MuiFormControlLabel-root').click()
    wait_until(lambda: widget.value is False, page)
    expect(page.locator('.MuiCheckbox-root')).not_to_be_checked()

def test_checkbox_no_label(page):
    widget = Checkbox(value=False)
    serve_component(page, widget)

    expect(page.locator('.checkbox')).to_have_count(1)
    expect(page.locator('.MuiFormControlLabel-root')).to_have_text('')
    expect(page.locator('.MuiCheckbox-root')).to_have_count(1)

    # Verify checkbox still works without label
    page.locator('.MuiCheckbox-root').click()
    wait_until(lambda: widget.value is True, page)
    expect(page.locator('.MuiCheckbox-root')).to_be_checked()
