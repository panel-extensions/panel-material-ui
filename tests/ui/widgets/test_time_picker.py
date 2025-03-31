import datetime

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import TimePicker
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_time_picker(page):
    """Test basic functionality of TimePicker."""
    time_picker = TimePicker(value="18:08:00")

    serve_component(page, time_picker)

    # Check if the component is rendered
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)

    # Verify the input value matches the expected time format
    input_element = page.locator(".MuiInputBase-input")
    # Should be in 12h format by default with lowercase am/pm
    assert "06:08 pm" in input_element.input_value().lower()

    # Enter a new time value
    input_element.fill("12:30 pm")

    try:
        wait_until(lambda: time_picker.value == datetime.time(12, 30), page)
    except Exception:
        assert time_picker.value == datetime.time(12, 30)

def test_time_picker_with_datetime_time(page):
    """Test TimePicker with datetime.time instance."""
    time_value = datetime.time(12, 59, 30)
    time_picker = TimePicker(value=time_value)

    serve_component(page, time_picker)

    # Verify the input value matches the expected time format
    input_element = page.locator(".MuiInputBase-input")
    # Should display 12:59 pm in 12h format by default with leading zeros
    assert "12:59 pm" in input_element.input_value().lower()

    # The time value in Python model should match the original value
    assert time_picker.value == "12:59:30"


@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_time_picker_variant(page, variant):
    """Test different variants of TimePicker."""
    time_picker = TimePicker(value="18:08:00", variant=variant)

    serve_component(page, time_picker)

    # Check if the component with the specific variant is rendered
    if variant == "standard":
        expect(page.locator(".MuiInput-root")).to_have_count(1)
    else:
        expect(page.locator(f".Mui{variant.capitalize()}Input-root")).to_have_count(1)


@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
def test_time_picker_color(page, color):
    """Test different colors of TimePicker."""
    time_picker = TimePicker(value="18:08:00", color=color)

    serve_component(page, time_picker)

    # Check if the component is rendered
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)


@pytest.mark.parametrize('clock_format,expected_marker', [
    ("12h", ["pm", "am"]),
    ("24h", [])
])
def test_time_picker_clock_format(page, clock_format, expected_marker):
    """Test 12h and 24h clock formats."""
    time_picker = TimePicker(value="18:08:00", clock=clock_format)

    serve_component(page, time_picker)

    # Get the input value
    input_value = page.locator(".MuiInputBase-input").input_value().lower()

    # Check if the format is correct based on the clock setting
    if expected_marker:
        # Should contain am/pm indicator for 12h
        assert any(marker in input_value for marker in expected_marker)
    else:
        # Should not contain am/pm indicator for 24h
        assert all(marker not in input_value for marker in ["am", "pm"])
        # For 24h format, we should see a value like "18:08"
        assert "18:08" in input_value


def test_time_picker_disabled(page):
    """Test disabled state of TimePicker."""
    time_picker = TimePicker(value="18:08:00", disabled=True)

    serve_component(page, time_picker)

    # Check if the component is disabled
    expect(page.locator(".MuiInputBase-root.Mui-disabled")).to_have_count(1)


def test_time_picker_min_max_time(page):
    """Test min and max time constraints."""
    # Set bounds from 9:00 to 18:00
    time_picker = TimePicker(
        value="12:00:00",
        start="09:00:00",
        end="18:00:00"
    )

    serve_component(page, time_picker)

    # Check if the component is rendered
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)

    # Verify input value
    input_value = page.locator(".MuiInputBase-input").input_value().lower()
    assert "12:00" in input_value

    # The time value should be valid
    assert time_picker.value is not None


def test_time_picker_with_seconds(page):
    """Test TimePicker with seconds enabled."""
    time_picker = TimePicker(
        value="18:08:30",
        seconds=True
    )

    serve_component(page, time_picker)

    # Verify the input value includes seconds
    input_element = page.locator(".MuiInputBase-input")
    input_value = input_element.input_value().lower()

    # Format should include seconds
    assert "06:08:30 pm" in input_value or "06:08:30pm" in input_value

    # Verify the value still includes seconds
    assert time_picker.value == "18:08:30"


def test_time_picker_format_synchronization(page):
    """Test that format synchronizes with clock setting."""
    # Start with 12h clock
    time_picker = TimePicker(
        value="18:08:00",
        clock="12h"
    )

    serve_component(page, time_picker)

    # Initially should be in 12h format
    input_value = page.locator(".MuiInputBase-input").input_value().lower()
    assert "pm" in input_value

    # Change to 24h clock
    time_picker.clock = "24h"

    # Wait for the update to apply
    wait_until(lambda: "pm" not in page.locator(".MuiInputBase-input").input_value().lower(), page)

    # Should now be in 24h format
    input_value = page.locator(".MuiInputBase-input").input_value()
    assert "18:08" in input_value
    assert "pm" not in input_value.lower()


def test_time_picker_increments(page):
    """Test hour, minute, and second increments."""
    time_picker = TimePicker(
        value="18:08:00",
        hour_increment=2,
        minute_increment=5,
        second_increment=10,
        seconds=True
    )

    serve_component(page, time_picker)

    # Verify the format shows seconds
    input_value = page.locator(".MuiInputBase-input").input_value().lower()
    assert "06:08:00 pm" in input_value or "06:08:00pm" in input_value
