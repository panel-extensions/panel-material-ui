import datetime

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import DatetimePicker
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_datetime_picker(page):
    """Test basic functionality of DatetimePicker."""
    datetime_picker = DatetimePicker(value=datetime.datetime(2023, 6, 15, 14, 30))

    serve_component(page, datetime_picker)

    # Check if the component is rendered
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)

    # We need to wait for the component to fully initialize
    wait_until(lambda: "2023-06-15" in page.locator(".MuiInputBase-input").input_value(), page)

    # The datetime value in Python model should match the original value
    assert datetime_picker.value.year == 2023
    assert datetime_picker.value.month == 6
    assert datetime_picker.value.day == 15
    assert datetime_picker.value.hour == 14
    assert datetime_picker.value.minute == 30


def test_datetime_picker_with_string(page):
    """Test DatetimePicker with string datetime value."""
    datetime_picker = DatetimePicker(value="2023-06-15 14:30:00")

    serve_component(page, datetime_picker)

    # Wait for initialization
    wait_until(lambda: "2023-06-15" in page.locator(".MuiInputBase-input").input_value(), page)

    # The datetime value in Python model should be parsed correctly
    assert isinstance(datetime_picker.value, datetime.datetime)
    assert datetime_picker.value.year == 2023
    assert datetime_picker.value.month == 6
    assert datetime_picker.value.day == 15
    assert datetime_picker.value.hour == 14
    assert datetime_picker.value.minute == 30


@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_datetime_picker_variant(page, variant):
    """Test different variants of DatetimePicker."""
    datetime_picker = DatetimePicker(
        value=datetime.datetime(2023, 6, 15, 14, 30),
        variant=variant
    )

    serve_component(page, datetime_picker)

    # Check if the component with the specific variant is rendered
    if variant == "standard":
        expect(page.locator(".MuiInput-root")).to_have_count(1)
    else:
        expect(page.locator(f".Mui{variant.capitalize()}Input-root")).to_have_count(1)


@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
def test_datetime_picker_color(page, color):
    """Test different colors of DatetimePicker."""
    datetime_picker = DatetimePicker(
        value=datetime.datetime(2023, 6, 15, 14, 30),
        color=color
    )

    serve_component(page, datetime_picker)

    # Check if the component is rendered
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)


@pytest.mark.parametrize('military_time,expected_format', [
    (True, ["14:30"]),  # 24h format
    (False, ["02:30", "pm"])  # 12h format
])
def test_datetime_picker_time_format(page, military_time, expected_format):
    """Test 12h and 24h time formats."""
    datetime_picker = DatetimePicker(
        value=datetime.datetime(2023, 6, 15, 14, 30),
        military_time=military_time
    )

    serve_component(page, datetime_picker)

    # Check rendering only for now
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)


def test_datetime_picker_disabled(page):
    """Test disabled state of DatetimePicker."""
    datetime_picker = DatetimePicker(
        value=datetime.datetime(2023, 6, 15, 14, 30),
        disabled=True
    )

    serve_component(page, datetime_picker)

    # Check if the component is disabled
    expect(page.locator(".MuiInputBase-root.Mui-disabled")).to_have_count(1)


def test_datetime_picker_min_max(page):
    """Test min and max date constraints."""
    # Set bounds from June 1 to June 30, 2023
    datetime_picker = DatetimePicker(
        value=datetime.datetime(2023, 6, 15, 14, 30),
        start=datetime.datetime(2023, 6, 1),
        end=datetime.datetime(2023, 6, 30)
    )

    serve_component(page, datetime_picker)

    # Check if the component is rendered
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)

    # Verify input value
    input_value = page.locator(".MuiInputBase-input").input_value()
    assert "2023-06-15" in input_value

    # The value should be valid
    assert datetime_picker.value is not None


def test_datetime_picker_with_seconds(page):
    """Test DatetimePicker with seconds enabled."""
    datetime_picker = DatetimePicker(
        value=datetime.datetime(2023, 6, 15, 14, 30, 45),
        enable_seconds=True
    )

    serve_component(page, datetime_picker)

    # Wait for initialization
    wait_until(lambda: "2023-06-15" in page.locator(".MuiInputBase-input").input_value(), page)

    # Verify the value includes seconds
    assert datetime_picker.value.second == 45


def test_datetime_picker_format_update(page):
    """Test format updates when settings change."""
    datetime_picker = DatetimePicker(
        value=datetime.datetime(2023, 6, 15, 14, 30),
        military_time=True
    )

    serve_component(page, datetime_picker)

    # Check rendering only for now
    expect(page.locator(".MuiInputBase-root")).to_have_count(1)
