import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import CheckBoxGroup
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_checkbox_group_basic_functionality(page):
    widget = CheckBoxGroup(
        options=['Option 1', 'Option 2', 'Option 3'],
        value=['Option 1']
    )
    serve_component(page, widget)

    # Verify basic rendering
    expect(page.locator('.MuiFormControl-root')).to_have_count(1)
    expect(page.locator('.MuiCheckbox-root')).to_have_count(3)
    expect(page.locator('.MuiFormControlLabel-root')).to_have_count(3)

    # Verify initial value
    expect(page.locator('.PrivateSwitchBase-input').first).to_have_attribute('checked', '')
    expect(page.locator('.PrivateSwitchBase-input').nth(1)).not_to_have_attribute('checked', '')
    expect(page.locator('.PrivateSwitchBase-input').nth(2)).not_to_have_attribute('checked', '')

def test_checkbox_group_multiple_selection(page):
    widget = CheckBoxGroup(
        options=['Option 1', 'Option 2', 'Option 3']
    )
    serve_component(page, widget)

    # Select multiple options
    page.locator('.MuiCheckbox-root').first.click()
    page.locator('.MuiCheckbox-root').nth(1).click()

    # Verify selections
    wait_until(lambda: widget.value == ['Option 1', 'Option 2'], page)
    expect(page.locator('.MuiCheckbox-root.Mui-checked')).to_have_count(2)
    expect(page.locator('.MuiCheckbox-root.Mui-checked').nth(0).locator('input')).to_have_attribute('value', 'Option 1')
    expect(page.locator('.MuiCheckbox-root.Mui-checked').nth(1).locator('input')).to_have_attribute('value', 'Option 2')

    # Deselect an option
    page.locator('.MuiCheckbox-root').first.click()
    wait_until(lambda: widget.value == ['Option 2'], page)
    expect(page.locator('.MuiCheckbox-root.Mui-checked')).to_have_count(1)
    expect(page.locator('.MuiCheckbox-root.Mui-checked').locator('input')).to_have_attribute('value', 'Option 2')

@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_checkbox_group_colors(page, color):
    widget = CheckBoxGroup(
        options=['Option 1'],
        color=color
    )
    serve_component(page, widget)

    # Verify color class
    expect(page.locator(f'.MuiCheckbox-color{color.capitalize()}')).to_have_count(1)

@pytest.mark.parametrize('placement', ['top', 'bottom', 'start', 'end'])
def test_checkbox_group_label_placement(page, placement):
    widget = CheckBoxGroup(
        options=['Option 1'],
        label_placement=placement
    )
    serve_component(page, widget)

    # Verify label placement
    expect(page.locator(f'.MuiFormControlLabel-labelPlacement{placement.capitalize()}')).to_have_count(1)

def test_checkbox_group_inline_layout(page):
    widget = CheckBoxGroup(
        options=['Option 1', 'Option 2', 'Option 3'],
        inline=True
    )
    serve_component(page, widget)

    # Verify inline layout
    expect(page.locator('.MuiRadioGroup-root.MuiRadioGroup-row')).to_have_count(1)

def test_checkbox_group_disabled_state(page):
    widget = CheckBoxGroup(
        options=['Option 1', 'Option 2'],
        disabled=True
    )
    serve_component(page, widget)

    # Verify disabled state
    expect(page.locator('.MuiCheckbox-root.Mui-disabled')).to_have_count(2)

def test_checkbox_group_with_label(page):
    label = "Group Label"
    widget = CheckBoxGroup(
        options=['Option 1'],
        label=label
    )
    serve_component(page, widget)

    # Verify label
    expect(page.locator('.MuiFormLabel-root')).to_have_text(label)

def test_checkbox_group_value_updates(page):
    widget = CheckBoxGroup(
        options=['Option 1', 'Option 2', 'Option 3']
    )
    serve_component(page, widget)

    # Update value programmatically
    widget.value = ['Option 2', 'Option 3']

    # Verify UI updates
    expect(page.locator('.MuiCheckbox-root.Mui-checked')).to_have_count(2)
    expect(page.locator('.MuiCheckbox-root.Mui-checked').nth(0).locator('input')).to_have_attribute('value', 'Option 2')
    expect(page.locator('.MuiCheckbox-root.Mui-checked').nth(1).locator('input')).to_have_attribute('value', 'Option 3')

def test_checkbox_group_empty_value(page):
    widget = CheckBoxGroup(
        options=['Option 1', 'Option 2'],
        value=None
    )
    serve_component(page, widget)

    # Verify no options are selected
    expect(page.locator('.MuiCheckbox-root.Mui-checked')).to_have_count(0)
    assert widget.value == []

def test_checkbox_group_click_label(page):
    widget = CheckBoxGroup(
        options=['Option 1']
    )
    serve_component(page, widget)

    # Click label instead of checkbox
    page.locator('.MuiFormControlLabel-root').click()

    # Verify selection
    wait_until(lambda: widget.value == ['Option 1'], page)
    expect(page.locator('.Mui-checked')).to_have_count(1)
