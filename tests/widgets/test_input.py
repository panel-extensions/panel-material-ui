import pytest

from panel import config
from datetime import date

from panel_material_ui.widgets import IntInput, FloatInput, DatePicker

@pytest.mark.from_panel
@pytest.mark.xfail(reason='')
def test_int_input(document, comm):
    int_input = IntInput(name='Int input')
    widget = int_input.get_root(document, comm=comm)

    assert widget.name == 'Int input'
    assert widget.step == 1
    assert widget.value == 0

    int_input._process_events({'value': 2})
    assert int_input.value == 2
    int_input._process_events({'value_throttled': 2})
    assert int_input.value_throttled == 2

    int_input.value = 0
    assert widget.value == 0

    # Testing throttled mode
    with config.set(throttled=True):
        int_input._process_events({'value': 1})
        assert int_input.value == 0  # no change
        int_input._process_events({'value_throttled': 1})
        assert int_input.value == 1

        int_input.value = 2
        assert widget.value == 2


@pytest.mark.from_panel
@pytest.mark.xfail(reason='')
def test_float_input(document, comm):
    float_input = FloatInput(value=0.4, name="Float input")
    widget = float_input.get_root(document, comm=comm)

    assert widget.name == 'Float input'
    assert widget.step == 0.1
    assert widget.value == 0.4

    float_input._process_events({'value': 0.2})
    assert float_input.value == 0.2
    float_input._process_events({'value_throttled': 0.2})
    assert float_input.value_throttled == 0.2

    float_input.value = 0.3
    assert widget.value == 0.3

    # Testing throttled mode
    with config.set(throttled=True):
        float_input._process_events({'value': 0.4})
        assert float_input.value == 0.3  # no change
        float_input._process_events({'value_throttled': 0.4})
        assert float_input.value == 0.4

        float_input.value = 0.5
        assert widget.value == 0.5


@pytest.mark.from_panel
def test_date_picker():
    date_picker = DatePicker(name='DatePicker', value=date(2018, 9, 2),
                             start=date(2018, 9, 1), end=date(2018, 9, 10))

    date_picker._process_events({'value': '2018-09-03'})
    assert date_picker.value == date(2018, 9, 3)

    date_picker._process_events({'value': date(2018, 9, 5)})
    assert date_picker.value == date(2018, 9, 5)

    date_picker._process_events({'value': date(2018, 9, 6)})
    assert date_picker.value == date(2018, 9, 6)


@pytest.mark.from_panel
def test_date_picker_options():
    options = [date(2018, 9, 1), date(2018, 9, 2), date(2018, 9, 3)]
    datetime_picker = DatePicker(
        name='DatetimePicker', value=date(2018, 9, 2),
        options=options
    )
    assert datetime_picker.value == date(2018, 9, 2)
    assert datetime_picker.enabled_dates == options
