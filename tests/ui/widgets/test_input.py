import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import TextInput, PasswordInput
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


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

@pytest.mark.from_panel
def test_textinput_enter_pressed(page):
    text_input = TextInput()
    clicks = [0]

    def on_enter(event):
        clicks[0] += 1

    text_input.param.watch(on_enter, "enter_pressed")
    serve_component(page, text_input)

    # Find the input field and type into it
    input_area = page.locator('input').nth(0)
    input_area.click()
    input_area.press('Enter')
    wait_until(lambda: clicks[0] == 1)
    input_area.press("Enter")
    wait_until(lambda: clicks[0] == 2)

def test_textinput_max_length(page):
    widget = TextInput(max_length=2)
    serve_component(page, widget)

    # Find the input field and type into it
    input_area = page.locator('input').nth(0)
    input_area.click()
    # type more but only first max_length characters are allowed
    input_area.type("123")
    expect(input_area).to_have_value("12")
    wait_until(lambda: widget.value_input == "12", page)

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

def test_password_max_length(page):
    widget = PasswordInput(max_length=2)
    serve_component(page, widget)

    # Find the input field and type into it
    input_area = page.locator('input').nth(0)
    input_area.click()
    # type more but only first max_length characters are allowed
    input_area.type("123")
    expect(input_area).to_have_value("12")
    wait_until(lambda: widget.value_input == "12", page)
