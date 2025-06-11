import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import ColorPicker
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_color_picker_basic_functionality(page):
    widget = ColorPicker(label='Color', value='#FF0000')
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.MuiColorInput-TextField')).to_have_count(1)
    expect(page.locator('.MuiInputBase-input')).to_have_value('#FF0000')

    # Open color picker
    page.locator('.MuiColorInput-Button').click()

    # Verify color picker popover is open
    expect(page.locator('.MuiColorInput-Popover')).to_be_visible()

    # Select a new color (click in the color area)
    color_area = page.locator('.MuiColorInput-ColorSpace')
    color_area.click(position={'x': 100, 'y': 100})

    # Verify value is updated
    wait_until(lambda: widget.value != '#FF0000', page)
    expect(page.locator('.MuiInputBase-input')).not_to_have_value('#FF0000')

@pytest.mark.parametrize('format', ['hex', 'rgb', 'hsl'])
def test_color_picker_formats(page, format):
    widget = ColorPicker(label='Color', value='#FF0000', format=format)
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.MuiColorInput-TextField')).to_have_count(1)

    # Open color picker
    page.locator('.MuiColorInput-Button').click()

    # Verify color picker popover is open
    expect(page.locator('.MuiColorInput-Popover')).to_be_visible()

    # Select a new color (click in the color area)
    color_area = page.locator('.MuiColorInput-ColorSpace')
    color_area.click(position={'x': 100, 'y': 100})

    # Verify input format
    if format == 'hex':
        wait_until(lambda: widget.value.startswith('#'), page)
    elif format == 'rgb':
        wait_until(lambda: widget.value.startswith('rgb'), page)
    elif format == 'hsl':
        wait_until(lambda: widget.value.startswith('hsl'), page)

def test_color_picker_alpha(page):
    widget = ColorPicker(label='Color', value='#FF0000', alpha=True)
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.MuiColorInput-TextField')).to_have_count(1)

    # Open color picker
    page.locator('.MuiColorInput-Button').click()

    # Verify alpha slider is present
    expect(page.locator('.MuiColorInput-AlphaSlider')).to_be_visible()

    # Change alpha value (click on the slider handle)
    alpha_slider = page.locator('.MuiColorInput-AlphaSlider')
    alpha_slider.click(position={'x': 10, 'y': 0})

    # Verify value includes alpha
    wait_until(lambda: len(widget.value) == 9, page)
    expect(page.locator('.MuiInputBase-input')).to_have_value(widget.value)

def test_color_picker_disabled_state(page):
    widget = ColorPicker(label='Color', value='#FF0000', disabled=True)
    serve_component(page, widget)

    # Verify disabled state
    expect(page.locator('.MuiColorInput-TextField')).to_have_count(1)
    expect(page.locator('.MuiInputBase-root.Mui-disabled')).to_have_count(1)

@pytest.mark.parametrize('size', ['small', 'large'])
def test_color_picker_sizes(page, size):
    widget = ColorPicker(label='Color', value='#FF0000', size=size)
    serve_component(page, widget)

    expect(page.locator('.MuiColorInput-TextField')).to_have_count(1)
    expect(page.locator(f'.MuiInputBase-size{size.capitalize()}')).to_have_count(1)

@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_color_picker_colors(page, color):
    widget = ColorPicker(label='Color', value='#FF0000', color=color)
    serve_component(page, widget)

    expect(page.locator('.MuiColorInput-TextField')).to_have_count(1)
    expect(page.locator(f'.MuiInputBase-color{color.capitalize()}')).to_have_count(1)

def test_color_picker_label(page):
    label = 'Choose a color'
    widget = ColorPicker(label=label, value='#FF0000')
    serve_component(page, widget)

    expect(page.locator('.MuiColorInput-TextField')).to_have_count(1)
    expect(page.locator('.MuiInputLabel-root')).to_have_text(label)

def test_color_picker_value_updates(page):
    widget = ColorPicker(label='Color', value='#FF0000')
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.MuiInputBase-input')).to_have_value('#FF0000')

    # Update value programmatically
    widget.value = '#00FF00'
    expect(page.locator('.MuiInputBase-input')).to_have_value('#00FF00')

    # Update to None
    widget.value = None
    expect(page.locator('.MuiInputBase-input')).to_have_value('')

def test_color_picker_invalid_value(page):
    widget = ColorPicker(label='Color', value='invalid-color')
    serve_component(page, widget)

    expect(page.locator('.MuiInputBase-input')).to_have_value('invalid-color')

def test_color_picker_popover_position(page):
    widget = ColorPicker(label='Color', value='#FF0000')
    serve_component(page, widget)

    # Open color picker
    page.locator('.MuiColorInput-Button').click()

    # Verify popover is positioned correctly
    popover = page.locator('.MuiColorInput-Popover')
    expect(popover).to_be_visible()

    # Verify popover is within viewport
    popover_box = popover.bounding_box()
    viewport = page.viewport_size
    assert popover_box['x'] >= 0
    assert popover_box['y'] >= 0
    assert popover_box['x'] + popover_box['width'] <= viewport['width']
    assert popover_box['y'] + popover_box['height'] <= viewport['height']
