import time
from datetime import datetime

import numpy as np
import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.widgets import (
    ArrayInput,
    DatetimeRangeInput,
    FloatInput,
    IntInput,
    NumberInput,
    PasswordInput,
    TextAreaInput,
    TextInput,
)

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_text_input_variant(page, variant):
    widget = TextInput(label='Name', placeholder='Enter your name here ...', variant=variant)
    serve_component(page, widget)
    expect(page.locator('.text-input')).to_have_count(1)
    if variant == "standard":
        expect(page.locator('.MuiInput-root')).to_have_count(1)
    else:
        expect(page.locator(f'.Mui{variant.capitalize()}Input-root')).to_have_count(1)

def test_text_input_focus(page):
    widget = TextInput(label='Test', placeholder='Type something...')
    serve_component(page, widget)
    input = page.locator('.MuiInputBase-input')
    expect(input).to_have_count(1)
    widget.focus()
    expect(input).to_be_focused()

def test_text_input_typing(page):
    widget = TextInput(label='Test', placeholder='Type something...')
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

def test_password_input_focus(page):
    widget = PasswordInput(label='Password', placeholder='Enter your password here ...')
    serve_component(page, widget)
    input = page.locator('.MuiInputBase-input')
    expect(input).to_have_count(1)
    widget.focus()
    expect(input).to_be_focused()

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

@pytest.mark.parametrize('widget_type,selector', [
    (TextInput, 'input'), (PasswordInput, 'input'), (TextAreaInput, 'textarea')
])
def test_text_input_server_transform_while_typing(page, widget_type, selector):
    widget = widget_type()

    def upper(event):
        time.sleep(0.03)
        widget.value = event.new.upper()

    widget.param.watch(upper, 'value_input')
    serve_component(page, widget)

    input_field = page.locator(selector).nth(0)
    input_field.click()
    page.keyboard.type('the quick brown fox', delay=10)

    expect(input_field).to_have_value('THE QUICK BROWN FOX')
    wait_until(lambda: widget.value == 'THE QUICK BROWN FOX', page)


def test_text_input_server_update_deferred_during_ime_composition(page):
    widget = TextInput()

    def upper(event):
        widget.value = event.new.upper()

    widget.param.watch(upper, 'value_input')
    serve_component(page, widget)

    input_field = page.locator('input').nth(0)
    input_field.click()
    input_field.dispatch_event('compositionstart', {'data': ''})
    page.keyboard.type('abc')
    wait_until(lambda: widget.value_input == 'ABC', page)
    page.wait_for_timeout(800)
    expect(input_field).to_have_value('abc')

    input_field.dispatch_event('compositionend', {'data': 'abc'})
    expect(input_field).to_have_value('ABC')


def test_text_input_server_update_when_idle(page):
    widget = TextInput()
    serve_component(page, widget)

    input_field = page.locator('input').nth(0)
    input_field.click()
    input_field.type('abc')
    wait_until(lambda: widget.value_input == 'abc', page)
    widget.value = 'xyz'
    expect(input_field).to_have_value('xyz')


def test_float_input_typing(page):
    widget = FloatInput()
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    input_area.click()
    input_area.fill("")
    input_area.type("1.23")
    input_area.press("Enter")
    expect(input_area).to_have_value("1.23")
    wait_until(lambda: widget.value == 1.23, page)

def test_int_input_value_throttled(page):
    widget = IntInput(value=1)
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    input_area.click()
    input_area.fill('42')
    input_area.press('Enter')
    wait_until(lambda: widget.value == 42 and widget.value_throttled == 42, page)

    page.locator('button').last.click()
    wait_until(lambda: widget.value == 43 and widget.value_throttled == 43, page)


def test_float_input_arrow_steps_small_exponential_values(page):
    widget = FloatInput(value=1e-7, step=1e-7)
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    input_area.click()
    page.keyboard.press('ArrowUp')
    page.keyboard.press('ArrowUp')

    wait_until(lambda: widget.value == pytest.approx(3e-7), page)
    input_area.press('Tab')
    page.wait_for_timeout(300)
    assert widget.value == pytest.approx(3e-7)


def test_int_input_blur_without_edit_does_not_commit(page):
    widget = IntInput(value=1)
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    expect(input_area).to_have_value('1')
    widget.value = 5
    expect(input_area).to_have_value('5')

    input_area.click()
    input_area.press('Enter')
    input_area.press('Tab')
    page.wait_for_timeout(500)
    assert widget.value == 5
    assert widget.value_throttled == 1


def test_int_input_blur_flushes_pending_step(page):
    widget = IntInput(value=1, wheel_wait=5000)
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    input_area.click()
    page.keyboard.press('ArrowUp')
    wait_until(lambda: widget.value == 2, page)
    assert widget.value_throttled == 1

    input_area.press('Tab')
    wait_until(lambda: widget.value_throttled == 2, page)


def test_int_input_arrow_steps_from_typed_value(page):
    widget = IntInput(value=3)
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    input_area.click()
    input_area.press('End')
    page.keyboard.press('Backspace')
    page.keyboard.type('5')
    page.keyboard.press('ArrowUp')

    expect(input_area).to_have_value('6')
    wait_until(lambda: widget.value == 6, page)


@pytest.mark.parametrize('typed,expected', [('99', 10), ('-5', 0)])
def test_int_input_typed_value_clamped(page, typed, expected):
    widget = IntInput(value=3, start=0, end=10)
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    input_area.click()
    input_area.fill(typed)
    input_area.press('Enter')

    expect(input_area).to_have_value(str(expected))
    wait_until(lambda: widget.value == expected, page)


def test_number_input_focus(page):
    widget = NumberInput(value=5, start=0, end=10)
    serve_component(page, widget)
    input_element = page.locator('.MuiInputBase-input')
    expect(input_element).to_have_count(1)
    widget.focus()
    expect(input_element).to_be_focused()


def test_array_input_editing(page):
    widget = ArrayInput(value=np.array([1, 2]), max_array_size=2)
    serve_component(page, widget)
    input_field = page.locator('.MuiInputBase-input')
    expect(input_field).to_have_value('[1, 2]')
    input_field.fill('[3, 4]')
    input_field.press('Enter')
    wait_until(lambda: np.array_equal(widget.value, [3, 4]), page)

    widget.value = np.arange(5)
    expect(input_field).to_be_disabled()
    expect(input_field).to_have_value(np.array2string(widget.value, separator=',', threshold=2))


def test_datetime_range_input_editing(page):
    widget = DatetimeRangeInput(value=(datetime(2024, 1, 1), datetime(2024, 2, 1)))
    serve_component(page, widget)
    inputs = page.locator('.MuiInputBase-input')
    expect(inputs).to_have_count(2)
    inputs.nth(0).fill('2024-01-05 00:00:00')
    inputs.nth(0).press('Enter')
    wait_until(lambda: widget.value[0] == datetime(2024, 1, 5), page)


@pytest.mark.parametrize('typed,expected', [('1e-3', 0.001), ('-2.5E2', -250), ('.5e1', 5)])
def test_float_input_typed_exponent(page, typed, expected):
    widget = FloatInput(value=1)
    serve_component(page, widget)

    input_area = page.locator('input').nth(0)
    input_area.click()
    input_area.fill(typed)
    input_area.press('Enter')
    wait_until(lambda: widget.value == expected, page)
