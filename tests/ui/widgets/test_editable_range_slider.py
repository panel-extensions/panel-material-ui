import pytest
import math

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import EditableRangeSlider, EditableIntRangeSlider
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

def test_editable_range_slider_basic(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=math.pi,
        value=(math.pi/4, math.pi/2),
        step=0.01
    )
    serve_component(page, widget)

    expect(page.locator(".MuiSlider-root")).to_have_count(1)
    expect(page.locator("input[type='text']")).to_have_count(2)

    inputs = page.locator("input[type='text']")
    expect(inputs.nth(0)).to_have_value(str(round(math.pi/4, 2)))
    expect(inputs.nth(1)).to_have_value(str(round(math.pi/2, 2)))

def test_editable_range_slider_input_validation(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=10,
        fixed_start=0,
        fixed_end=10,
        value=(2, 8),
        step=0.1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")

    # Test invalid input (non-numeric)
    inputs.nth(0).fill("abc")
    inputs.nth(0).blur()
    expect(inputs.nth(0)).to_have_value("2")  # Should revert to previous valid value

    # Test out of bounds input
    inputs.nth(0).fill("15")  # Above end
    inputs.nth(0).blur()
    expect(inputs.nth(0)).to_have_value("8")  # Should clamp to end

    inputs.nth(0).fill("2")  # Above end
    inputs.nth(0).blur()
    inputs.nth(1).fill("-5")  # Below start
    inputs.nth(1).blur()
    expect(inputs.nth(1)).to_have_value("2")  # Should clamp to start

def test_editable_range_slider_fixed_bounds(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        fixed_start=1,
        fixed_end=9,
        step=0.1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")

    # Test fixed bounds
    inputs.nth(0).fill("0")  # Below fixed_start
    inputs.nth(0).blur()
    expect(inputs.nth(0)).to_have_value("1")  # Should clamp to fixed_start

    inputs.nth(1).fill("10")  # Above fixed_end
    inputs.nth(1).blur()
    expect(inputs.nth(1)).to_have_value("9")  # Should clamp to fixed_end

def test_editable_range_slider_formatting(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=1000,
        value=(100, 900),
        format='0.0a'  # Format as abbreviated numbers
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")
    expect(inputs.nth(0)).to_have_value("100.0")
    expect(inputs.nth(1)).to_have_value("900.0")

def test_editable_range_slider_keyboard(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=0.1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")

    # Test arrow keys
    inputs.nth(0).focus()
    inputs.nth(0).press("ArrowUp")
    expect(inputs.nth(0)).to_have_value("2.1")  # Should increment by step

    inputs.nth(0).press("ArrowDown")
    expect(inputs.nth(0)).to_have_value("2")  # Should decrement by step

    # Test Enter key
    inputs.nth(0).fill("3.5")
    inputs.nth(0).press("Enter")
    expect(inputs.nth(0)).to_have_value("3.50")  # Should commit value on Enter

def test_editable_int_range_slider_basic(page):
    widget = EditableIntRangeSlider(
        name='Int Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=1
    )
    serve_component(page, widget)

    # Test initial state
    expect(page.locator(".MuiSlider-root")).to_have_count(1)
    expect(page.locator("input[type='text']")).to_have_count(2)

    # Test initial values in input fields
    inputs = page.locator("input[type='text']")
    expect(inputs.nth(0)).to_have_value("2")
    expect(inputs.nth(1)).to_have_value("8")

def test_editable_int_range_slider_float_handling(page):
    widget = EditableIntRangeSlider(
        name='Int Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")

    # Test float input
    inputs.nth(0).fill("3.5")
    inputs.nth(0).blur()
    expect(inputs.nth(0)).to_have_value("4")  # Should round to integer

    # Test step behavior
    inputs.nth(0).focus()
    inputs.nth(0).press("ArrowUp")
    expect(inputs.nth(0)).to_have_value("5")  # Should increment by integer step

    inputs.nth(0).press("ArrowDown")
    expect(inputs.nth(0)).to_have_value("4")  # Should decrement by integer step

def test_editable_int_range_slider_fixed_bounds(page):
    widget = EditableIntRangeSlider(
        name='Int Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        fixed_start=1,
        fixed_end=9,
        step=1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")

    # Test fixed bounds with integer values
    inputs.nth(0).fill("0")  # Below fixed_start
    inputs.nth(0).blur()
    expect(inputs.nth(0)).to_have_value("1")  # Should clamp to fixed_start

    inputs.nth(1).fill("10")  # Above fixed_end
    inputs.nth(1).blur()
    expect(inputs.nth(1)).to_have_value("9")  # Should clamp to fixed_end

def test_editable_range_slider_increment_decrement_buttons(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=0.1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")

    # Test increment button
    page.locator("button:has(svg[data-testid='AddIcon'])").first.click()
    expect(inputs.nth(0)).to_have_value("2.10")  # Should increment by step

    # Test decrement button
    page.locator("button:has(svg[data-testid='RemoveIcon'])").first.click()
    expect(inputs.nth(0)).to_have_value("2")  # Should decrement by step

    # Test increment button on second input
    page.locator("button:has(svg[data-testid='AddIcon'])").nth(1).click()
    expect(inputs.nth(1)).to_have_value("8.10")  # Should increment by step

    # Test decrement button on second input
    page.locator("button:has(svg[data-testid='RemoveIcon'])").nth(1).click()
    expect(inputs.nth(1)).to_have_value("8")  # Should decrement by step

def test_editable_range_slider_slider_interaction(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=0.1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")
    slider = page.locator(".MuiSlider-thumb")

    # Test moving first thumb
    slider.first.drag_to(page.locator(".MuiSlider-rail"), target_position={"x": 90, "y": 0}, force=True)
    expect(inputs.nth(0)).to_have_value("3")  # Should update input value

    # Test moving second thumb
    slider.nth(1).drag_to(page.locator(".MuiSlider-rail"), target_position={"x": 210, "y": 0}, force=True)
    expect(inputs.nth(1)).to_have_value("7")  # Should update input value

    # Test that thumbs can't cross each other
    slider.first.drag_to(page.locator(".MuiSlider-rail"), target_position={"x": 250, "y": 0}, force=True)
    expect(inputs.nth(0)).to_have_value("7")  # Should be limited by second thumb

def test_editable_int_range_slider_increment_decrement_buttons(page):
    widget = EditableIntRangeSlider(
        name='Int Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")

    # Test increment button
    page.locator("button:has(svg[data-testid='AddIcon'])").first.click()
    expect(inputs.nth(0)).to_have_value("3")  # Should increment by integer step

    # Test decrement button
    page.locator("button:has(svg[data-testid='RemoveIcon'])").first.click()
    expect(inputs.nth(0)).to_have_value("2")  # Should decrement by integer step

    # Test increment button on second input
    page.locator("button:has(svg[data-testid='AddIcon'])").nth(1).click()
    expect(inputs.nth(1)).to_have_value("9")  # Should increment by integer step

    # Test decrement button on second input
    page.locator("button:has(svg[data-testid='RemoveIcon'])").nth(1).click()
    expect(inputs.nth(1)).to_have_value("8")  # Should decrement by integer step

def test_editable_int_range_slider_slider_interaction(page):
    widget = EditableIntRangeSlider(
        name='Int Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")
    slider = page.locator(".MuiSlider-thumb")

    # Test moving first thumb
    slider.first.drag_to(page.locator(".MuiSlider-rail"), target_position={"x": 90, "y": 0}, force=True)
    expect(inputs.nth(0)).to_have_value("3")  # Should update input value with integer

    # Test moving second thumb
    slider.nth(1).drag_to(page.locator(".MuiSlider-rail"), target_position={"x": 210, "y": 0}, force=True)
    expect(inputs.nth(1)).to_have_value("7")  # Should update input value with integer

    # Test that thumbs can't cross each other
    slider.first.drag_to(page.locator(".MuiSlider-rail"), target_position={"x": 250, "y": 0}, force=True)
    expect(inputs.nth(0)).to_have_value("7")  # Should be limited by second thumb

def test_editable_range_slider_sync_input_slider(page):
    widget = EditableRangeSlider(
        name='Range Slider',
        start=0,
        end=10,
        value=(2, 8),
        step=0.1
    )
    serve_component(page, widget)

    inputs = page.locator("input[type='text']")
    slider = page.locator(".MuiSlider-thumb")

    # Test input updates slider position
    inputs.nth(0).fill("3.5")
    inputs.nth(0).press("Enter")
    thumb_moved = slider.first.evaluate("el => el.getBoundingClientRect().x > 0")
    assert thumb_moved

    # Test slider updates input
    slider.first.drag_to(page.locator(".MuiSlider-rail"), target_position={"x": 40, "y": 0})
    expect(inputs.nth(0)).to_have_value("1.30")  # Should update input value

    # Test both inputs and thumbs stay in sync
    inputs.nth(1).fill("6.5")
    inputs.nth(1).press("Enter")
    x = slider.first.evaluate("el => el.getBoundingClientRect().x")
    assert slider.nth(1).evaluate(f"el => el.getBoundingClientRect().x > {x}")
