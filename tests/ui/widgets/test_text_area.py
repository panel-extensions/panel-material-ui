import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import TextAreaInput
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

# observe when serving the component
TEXTAREA_LINE_HEIGHT = 23


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

@pytest.mark.from_panel
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

@pytest.mark.from_panel
def test_text_area_auto_grow_max_rows(page):
    text_area = TextAreaInput(auto_grow=True, value="1\n2\n3\n4\n", max_rows=7)

    serve_component(page, text_area)

    input_area = page.locator('.MuiInputBase-input').nth(0)
    input_area.click()
    input_area.press('Enter')
    input_area.press('Enter')
    input_area.press('Enter')

    wait_until(lambda: input_area.bounding_box()['height'] == 7 * TEXTAREA_LINE_HEIGHT, page)

@pytest.mark.from_panel
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

@pytest.mark.from_panel
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

def test_text_area_max_length(page):
    widget = TextAreaInput(max_length=2)
    serve_component(page, widget)

    # Find the input field and type into it
    input_area = page.locator('.MuiInputBase-input').nth(0)
    input_area.click()
    # type more but only first max_length characters are allowed
    input_area.type("123")
    expect(input_area).to_have_value("12")
    wait_until(lambda: widget.value_input == "12", page)
