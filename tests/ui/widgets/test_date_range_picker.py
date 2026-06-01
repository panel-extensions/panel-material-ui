import datetime as dt

import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import DateRangePicker, DatetimeRangePicker

pytestmark = pytest.mark.ui


def test_date_range_picker_initial_value(page):
    widget = DateRangePicker(
        label='Date Range',
        value=(dt.date(2024, 4, 5), dt.date(2024, 4, 15)),
        start=dt.date(2024, 4, 1),
        end=dt.date(2024, 4, 30),
    )
    serve_component(page, widget)

    input_el = page.locator("input")
    assert "2024-04-05" in input_el.input_value()
    assert "2024-04-15" in input_el.input_value()


def test_date_range_picker_select_range(page):
    widget = DateRangePicker(
        label='Date Range',
        start=dt.date(2024, 4, 1),
        end=dt.date(2024, 4, 30),
        value=(dt.date(2024, 4, 1), dt.date(2024, 4, 2)),
    )
    serve_component(page, widget)

    page.locator(".MuiIconButton-root").click()
    page.locator("button.rdp-day_button:has-text('10')").first.click()
    page.locator("button.rdp-day_button:has-text('20')").first.click()

    wait_until(lambda: widget.value == (dt.date(2024, 4, 10), dt.date(2024, 4, 20)), page)


def test_date_range_picker_disabled(page):
    widget = DateRangePicker(
        label='Date Range',
        value=(dt.date(2024, 4, 5), dt.date(2024, 4, 15)),
        disabled=True,
    )
    serve_component(page, widget)

    input_el = page.locator("input")
    assert input_el.is_disabled()


def test_date_range_picker_disabled_dates(page):
    widget = DateRangePicker(
        label='Date Range',
        start=dt.date(2024, 4, 1),
        end=dt.date(2024, 4, 30),
        disabled_dates=[dt.date(2024, 4, i) for i in range(10, 20)],
        value=(dt.date(2024, 4, 1), dt.date(2024, 4, 5)),
    )
    serve_component(page, widget)

    page.locator("input").click()
    page.wait_for_selector("[role='grid']")

    disabled_buttons = page.locator("button[disabled]")
    disabled_texts = [b.inner_text() for b in disabled_buttons.all()]
    for day in range(10, 20):
        assert str(day) in disabled_texts


def test_date_range_picker_value_start_end(page):
    widget = DateRangePicker(
        label='Date Range',
        value=(dt.date(2024, 4, 5), dt.date(2024, 4, 15)),
    )
    serve_component(page, widget)

    assert widget.value_start == dt.date(2024, 4, 5)
    assert widget.value_end == dt.date(2024, 4, 15)


def test_datetime_range_picker_initial_value(page):
    widget = DatetimeRangePicker(
        label='Datetime Range',
        value=(dt.datetime(2024, 4, 5, 9, 0), dt.datetime(2024, 4, 15, 17, 30)),
    )
    serve_component(page, widget)

    input_el = page.locator("input").first
    value = input_el.input_value()
    assert "2024-04-05" in value
    assert "2024-04-15" in value


def test_datetime_range_picker_select_range_with_time(page):
    widget = DatetimeRangePicker(
        label='Datetime Range',
        start=dt.datetime(2024, 4, 1),
        end=dt.datetime(2024, 4, 30),
        value=(dt.datetime(2024, 4, 1, 0, 0), dt.datetime(2024, 4, 2, 23, 59)),
    )
    serve_component(page, widget)

    page.locator("input").first.click()
    page.locator("button.rdp-day_button:has-text('10')").first.click()
    page.locator("button.rdp-day_button:has-text('20')").first.click()

    page.locator("button:has-text('Ok')").click()

    wait_until(lambda: widget.value[0].date() == dt.date(2024, 4, 10), page)
    wait_until(lambda: widget.value[1].date() == dt.date(2024, 4, 20), page)
