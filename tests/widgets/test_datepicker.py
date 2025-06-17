import datetime as dt

import numpy as np
import pandas as pd
import pytest
from panel_material_ui import DatePicker, DatetimePicker


DATES = ["2024-04-01", dt.date(2024, 4, 1), dt.datetime(2024, 4, 1), np.datetime64("2024-04-01"), pd.Timestamp("2024-04-01")]
DATETIMES = ["2024-04-01 00:00:00", "2024-04-01 00:00", dt.date(2024, 4, 1), dt.datetime(2024, 4, 1, 0, 0, 0), np.datetime64("2024-04-01 00:00:00"), pd.Timestamp("2024-04-01 00:00:00")]


@pytest.mark.parametrize('value', DATES)
def test_datepicker_value_parsing(value):
    assert DatePicker(value=value).value == dt.date(2024, 4, 1)

@pytest.mark.parametrize('value', DATES)
def test_datepicker_start_parsing(value):
    assert DatePicker(start=value).start == dt.date(2024, 4, 1)

@pytest.mark.parametrize('value', DATES)
def test_datepicker_end_parsing(value):
    assert DatePicker(end=value).end == dt.date(2024, 4, 1)

@pytest.mark.parametrize('value', DATES)
def test_datepicker_enable_dates(value):
    assert DatePicker(enabled_dates=[value]).enabled_dates == [dt.date(2024, 4, 1)]

@pytest.mark.parametrize('value', DATES)
def test_datepicker_disabled_dates(value):
    assert DatePicker(disabled_dates=[value]).disabled_dates == [dt.date(2024, 4, 1)]

@pytest.mark.parametrize('value', DATETIMES)
def test_datetimepicker_value_parsing(value):
    assert DatetimePicker(value=value).value == dt.datetime(2024, 4, 1, 0, 0, 0)

@pytest.mark.parametrize('value', DATETIMES)
def test_datetimepicker_start_parsing(value):
    assert DatetimePicker(start=value).start == dt.datetime(2024, 4, 1, 0, 0, 0)

@pytest.mark.parametrize('value', DATETIMES)
def test_datetimepicker_end_parsing(value):
    assert DatetimePicker(end=value).end == dt.datetime(2024, 4, 1, 0, 0, 0)

@pytest.mark.parametrize('value', DATES)
def test_datetimepicker_enabled_dates(value):
    assert DatetimePicker(enabled_dates=[value]).enabled_dates == [dt.date(2024, 4, 1)]

@pytest.mark.parametrize('value', DATES)
def test_datetimepicker_disabled_dates(value):
    assert DatetimePicker(disabled_dates=[value]).disabled_dates == [dt.date(2024, 4, 1)]
