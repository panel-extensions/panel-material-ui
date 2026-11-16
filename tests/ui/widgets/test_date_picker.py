import datetime as dt

import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Column
from panel_material_ui.widgets import (
    DatePicker,
    DateRangePicker,
    DatetimePicker,
    DatetimeRangePicker,
    TextInput,
    TimePicker,
)
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_datepicker_enabled_dates(page):
    widget = DatePicker(
        label='Date Picker',
        start=dt.date(2024, 4, 1),
        end=dt.date(2024, 4, 20),
        enabled_dates=[
            dt.date(2024, 4, 1),
            dt.date(2024, 4, 2),
            dt.date(2024, 4, 20),
            dt.date(2024, 4, 21),
        ]
    )
    serve_component(page, widget)

    # click the datepicker icon to show dates to select
    icon = page.locator(".MuiIconButton-root")
    icon.click()
    # Select all buttons in the date picker
    buttons = page.locator('.MuiPickerDay-root').all()

    enabled_buttons = []
    for button in buttons:
        is_disabled = button.get_attribute("disabled") is not None or button.evaluate(
            "el => el.classList.contains('Mui-disabled')")
        if not is_disabled:
            value = button.inner_text()  # Get the button's displayed text (date)
            enabled_buttons.append(value)

    # only enabled dates within the start to end range are selectable
    assert enabled_buttons == ['1', '2', '20']


def test_datepicker_disabled_dates(page):
    widget = DatePicker(
        label='Date Picker',
        start=dt.date(2024, 4, 1),
        end=dt.date(2024, 4, 20),
        disabled_dates=[
            dt.date(2024, 4, i) for i in range(1, 18)
        ]
    )
    serve_component(page, widget)

    # click the datepicker icon to show dates to select
    icon = page.locator(".MuiIconButton-root")
    icon.click()
    # Select all buttons in the date picker
    buttons = page.locator('.MuiPickerDay-root').all()

    enabled_buttons = []
    for button in buttons:
        is_disabled = button.get_attribute("disabled") is not None or button.evaluate(
            "el => el.classList.contains('Mui-disabled')")
        if not is_disabled:
            value = button.inner_text()  # Get the button's displayed text (date)
            enabled_buttons.append(value)

    # only enabled dates within the start to end range are selectable
    assert enabled_buttons == ['18', '19', '20']


def test_datepicker_clearable_propagates_none(page):
    widget = DatePicker(value=dt.date(2026, 5, 1), clearable=True)
    serve_component(page, widget)

    page.locator(".MuiPickersInputBase-root").hover()
    page.locator("button[title='Clear']").click()

    wait_until(lambda: widget.value is None, page)


def test_datepicker_clearable_manual_delete_propagates_none(page):
    widget = DatePicker(value=dt.date(2026, 5, 1), clearable=True)
    serve_component(page, widget)

    input_el = page.locator(".MuiPickersInputBase-root")
    input_el.click()
    page.keyboard.press("Control+a")
    page.keyboard.press("Delete")
    input_el.press("Tab")

    wait_until(lambda: widget.value is None, page)


def test_datepicker_clearable_partial_edit_does_not_clear(page):
    # Regression test: editing a single date section (e.g. typing into the
    # year) while other sections are still unset must not wipe the whole
    # value, even when clearable=True.
    widget = DatePicker(value=dt.date(2026, 8, 13), clearable=True)
    serve_component(page, widget)

    input_el = page.locator(".MuiPickersInputBase-input")
    wait_until(lambda: "2026-08-13" in input_el.input_value(), page)

    year_section = page.locator("span[aria-label='Year']")
    year_section.click()
    page.keyboard.press("2")

    assert widget.value == dt.date(2026, 8, 13)
    assert "08-13" in input_el.input_value()

    page.keyboard.press("Tab")

    assert widget.value == dt.date(2026, 8, 13)


def test_datepicker_edit_single_section_commits(page):
    widget = DatePicker(value=dt.date(2026, 8, 13), clearable=True)
    serve_component(page, widget)

    input_el = page.locator(".MuiPickersInputBase-input")
    wait_until(lambda: "2026-08-13" in input_el.input_value(), page)

    year_section = page.locator("span[aria-label='Year']")
    year_section.click()
    page.keyboard.type("2030")
    input_el.press("Tab")

    wait_until(lambda: widget.value == dt.date(2030, 8, 13), page)


def test_datepicker_repick_after_server_reset(page):
    widget = DatePicker(value=dt.date(2024, 1, 10))
    seen = []

    def reject(event):
        seen.append(event.new)
        if event.new == dt.date(2024, 1, 15):
            widget.value = dt.date(2024, 1, 10)

    widget.param.watch(reject, 'value')
    serve_component(page, widget)

    input_el = page.locator(".MuiPickersInputBase-input")
    for attempt in range(1, 3):
        page.locator('button[aria-label^="Choose date"]').click()
        page.locator('button[role="gridcell"]:text-is("15")').click()
        wait_until(lambda: seen.count(dt.date(2024, 1, 15)) == attempt, page)
        wait_until(lambda: "2024-01-10" in input_el.input_value(), page)
    assert widget.value == dt.date(2024, 1, 10)


@pytest.mark.parametrize('size', ['medium', 'large'])
@pytest.mark.parametrize('widget_type', [
    DatePicker, DatetimePicker, TimePicker, DateRangePicker, DatetimeRangePicker
])
def test_date_time_pickers_stretch_width(page, widget_type, size):
    reference = TextInput(label='Reference', sizing_mode='stretch_width', size=size)
    picker = widget_type(label='Picker', sizing_mode='stretch_width', size=size)
    serve_component(page, Column(reference, picker, width=600))

    fields = page.locator('.MuiFormControl-root')
    expect(fields).to_have_count(2)

    def widths():
        return [fields.nth(i).bounding_box()['width'] for i in range(2)]

    wait_until(lambda: widths()[0] > 500, page)
    ref_width, picker_width = widths()
    assert picker_width == pytest.approx(ref_width, abs=1)


@pytest.mark.parametrize('widget_type', [DatePicker, DatetimePicker, TimePicker])
def test_date_time_pickers_apply_sx(page, widget_type):
    picker = widget_type(label='Picker', sx={'backgroundColor': 'rgb(255, 0, 0)'})
    serve_component(page, picker)

    expect(page.locator('.MuiFormControl-root')).to_have_css('background-color', 'rgb(255, 0, 0)')
