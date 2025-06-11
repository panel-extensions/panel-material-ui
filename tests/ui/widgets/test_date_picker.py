import datetime as dt

import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import DatePicker

pytestmark = pytest.mark.ui


def test_datepicker_enabled_dates(page):
    widget = DatePicker(
        name='Date Picker',
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
    buttons = page.locator('.MuiPickersDay-root').all()

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
        name='Date Picker',
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
    buttons = page.locator('.MuiPickersDay-root').all()

    enabled_buttons = []
    for button in buttons:
        is_disabled = button.get_attribute("disabled") is not None or button.evaluate(
            "el => el.classList.contains('Mui-disabled')")
        if not is_disabled:
            value = button.inner_text()  # Get the button's displayed text (date)
            enabled_buttons.append(value)

    # only enabled dates within the start to end range are selectable
    assert enabled_buttons == ['18', '19', '20']
