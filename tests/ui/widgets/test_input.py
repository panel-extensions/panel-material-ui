import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import TextInput, PasswordInput, TextAreaInput, Checkbox, Switch, FileInput, ToggleIcon
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


# observe when serving the component
TEXTAREA_LINE_HEIGHT = 23


@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_text_input_variant(page, variant):
    widget = TextInput(name='Name', placeholder='Enter your name here ...', variant=variant)
    serve_component(page, widget)
    expect(page.locator('.text-input')).to_have_count(1)
    if variant == "standard":
        expect(page.locator('.MuiInput-root')).to_have_count(1)
    else:
        expect(page.locator(f'.Mui{variant.capitalize()}Input-root')).to_have_count(1)


def test_text_input_typing(page):
    widget = TextInput(name='Test', placeholder='Type something...')
    serve_component(page, widget)
    
    # Find the input field and type into it
    input_field = page.locator('input').nth(0)
    input_field.click()
    input_field.type('Hello World', delay=50)
    
    # Check that the text appears as we type (value_input)
    expect(input_field).to_have_value('Hello World')
    
    # Check value_input is updated while typing
    wait_until(lambda: widget.value_input == 'Hello World', page)
    
    # But the main value should only be updated when we press Enter
    assert widget.value == ''
    
    # Press Enter to update the value
    input_field.press('Enter')
    wait_until(lambda: widget.value == 'Hello World', page)
    
    # Test that typing more updates the display and value_input but not the value
    input_field.type(' Again', delay=50)
    expect(input_field).to_have_value('Hello World Again')
    wait_until(lambda: widget.value_input == 'Hello World Again', page)
    assert widget.value == 'Hello World'
    
    # Press Enter to update the value
    input_field.press('Enter')
    wait_until(lambda: widget.value == 'Hello World Again', page)


def test_password_show_hide(page):
    widget = PasswordInput(label='Password', placeholder='Enter your password here ...')
    serve_component(page, widget)
    expect(page.locator('.password-input')).to_have_count(1)
    expect(page.locator('input[type="password"]')).to_have_count(1)
    # click to show password
    eye_button = page.locator('button[aria-label="display the password"]')
    eye_button.click()
    # password is displayed
    expect(page.locator('input[type="text"]')).to_have_count(1)


def test_text_area_input(page):
    widget = TextAreaInput(label='Description', placeholder='Enter your description here...', rows=5)
    serve_component(page, widget)
    expect(page.locator('.text-area-input')).to_have_count(1)
    expect(page.locator('textarea[rows="5"]')).to_have_count(1)


def test_text_area_typing(page):
    widget = TextAreaInput(label='Description', placeholder='Type something...')
    serve_component(page, widget)
    
    # Find the textarea and type into it
    textarea = page.locator('textarea').nth(0)
    textarea.click()
    
    # Type text including newlines
    textarea.type('Multiline', delay=50)
    textarea.press('Enter')
    textarea.type('Text', delay=50)
    textarea.press('Enter')
    textarea.type('Test', delay=50)
    
    # Check that the text appears as we type (value_input)
    expect(textarea).to_have_value('Multiline\nText\nTest')
    
    # Check value_input is updated while typing
    wait_until(lambda: widget.value_input == 'Multiline\nText\nTest', page)
    
    # But value should still be the original value (empty string) since we haven't blurred
    assert widget.value == ''
    
    # Click elsewhere to trigger blur
    page.locator('body').click()
    wait_until(lambda: widget.value == 'Multiline\nText\nTest', page)




def test_text_area_auto_grow(page):
    widget = TextAreaInput(auto_grow=True, value="1\n2\n3\n4\n")
    serve_component(page, widget)

    input_area = page.locator('.MuiInputBase-input').nth(0)
    input_area.click()
    input_area.press('Enter')
    input_area.press('Enter')
    input_area.press('Enter')

    # 8 rows
    wait_until(lambda: input_area.bounding_box()['height'] == 8 * TEXTAREA_LINE_HEIGHT, page)


def test_text_area_auto_grow_max_rows(page):
    text_area = TextAreaInput(auto_grow=True, value="1\n2\n3\n4\n", max_rows=7)

    serve_component(page, text_area)

    input_area = page.locator('.MuiInputBase-input').nth(0)
    input_area.click()
    input_area.press('Enter')
    input_area.press('Enter')
    input_area.press('Enter')

    wait_until(lambda: input_area.bounding_box()['height'] == 7 * TEXTAREA_LINE_HEIGHT, page)


def test_text_area_auto_grow_min_rows(page):
    text_area = TextAreaInput(auto_grow=True, value="1\n2\n3\n4\n", rows=3)
    serve_component(page, text_area)

    input_area = page.locator('.MuiInputBase-input').nth(0)
    input_area.click()
    for _ in range(5):
        input_area.press('ArrowDown')
    for _ in range(10):
        input_area.press('Backspace')

    wait_until(lambda: input_area.bounding_box()['height'] == 3 * TEXTAREA_LINE_HEIGHT, page)


def test_text_area_auto_grow_shrink_back_on_new_value(page):
    text_area = TextAreaInput(auto_grow=True, value="1\n2\n3\n4\n", max_rows=5)
    serve_component(page, text_area)

    input_area = page.locator('.MuiInputBase-input').nth(0)
    input_area.click()
    for _ in range(5):
        input_area.press('ArrowDown')
    for _ in range(10):
        input_area.press('Backspace')

    text_area.value = ""
    assert input_area.bounding_box()['height'] == 2 * TEXTAREA_LINE_HEIGHT


def test_checkbox(page):
    widget = Checkbox(label='Works with the tools you know and love', value=True)
    serve_component(page, widget)
    expect(page.locator('.checkbox')).to_have_count(1)


def test_switch(page):
    widget = Switch(label='Works with the tools you know and love', value=True)
    serve_component(page, widget)
    expect(page.locator('.switch')).to_have_count(1)


def test_fileinput(page):
    widget = FileInput(accept='.png,.jpeg', multiple=True)
    serve_component(page, widget)
    expect(page.locator('.file-input')).to_have_count(1)


def test_toggle_icon(page):
    widget = ToggleIcon(icon="thumb-up", active_icon="thumb-down", size="small", description="Like")
    serve_component(page, widget)

    expect(page.locator('.toggle-icon')).to_have_count(1)
    icon = page.locator('.MuiCheckbox-root')
    expect(icon).to_have_text("thumb-up")
    icon.click()
    expect(icon).to_have_text("thumb-down")
