import pytest

from panel import config
from datetime import date

from panel_material_ui.widgets import IntInput, FloatInput, DatePicker
from panel_material_ui.chat import ChatAreaInput

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

def test_datepicker_accepts_strings():
    DatePicker(
        label='Date Picker',
        start="2024-04-01",
        end="2024-04-07",
        value="2024-04-01"
    )


# ChatAreaInput accept parameter validation tests
def test_chat_area_input_valid_accept_formats():
    """Test that valid accept formats don't raise errors."""
    # Valid file extensions
    ChatAreaInput(accept=".csv")
    ChatAreaInput(accept=".csv,.json")
    ChatAreaInput(accept=".pdf,.txt,.xlsx")

    # Valid MIME types
    ChatAreaInput(accept="text/csv")
    ChatAreaInput(accept="application/json")
    ChatAreaInput(accept="image/png,image/jpeg")
    ChatAreaInput(accept="text/csv,application/json")

    # Mixed formats
    ChatAreaInput(accept=".csv,text/plain")
    ChatAreaInput(accept="image/*,.pdf")

    # Wildcards
    ChatAreaInput(accept="image/*")
    ChatAreaInput(accept="text/*,image/*")

    # None should be allowed
    ChatAreaInput(accept=None)

    # Empty string should be allowed
    ChatAreaInput(accept="")


def test_chat_area_input_invalid_file_extensions():
    """Test that file extensions without dots raise appropriate errors."""
    with pytest.raises(ValueError, match="File extension 'csv' should start with a dot"):
        ChatAreaInput(accept="csv")

    with pytest.raises(ValueError, match="File extension 'json' should start with a dot"):
        ChatAreaInput(accept="json")

    with pytest.raises(ValueError, match="File extension 'csv' should start with a dot"):
        ChatAreaInput(accept="csv,txt")


def test_chat_area_input_invalid_mime_types():
    """Test that malformed MIME types raise appropriate errors."""
    # MIME type with dot in subtype
    with pytest.raises(ValueError, match="Invalid MIME type 'text/.csv'. The subtype '.csv' should not start with a dot"):
        ChatAreaInput(accept="text/.csv")

    with pytest.raises(ValueError, match="Invalid MIME type 'application/.json'"):
        ChatAreaInput(accept="application/.json")

    # Malformed MIME types - missing subtype
    with pytest.raises(ValueError, match="Invalid MIME type 'text/'. MIME types should be in format 'type/subtype'"):
        ChatAreaInput(accept="text/")

    # Malformed MIME types - missing type
    with pytest.raises(ValueError, match="Invalid MIME type '/csv'. MIME types should be in format 'type/subtype'"):
        ChatAreaInput(accept="/csv")

    # Too many slashes
    with pytest.raises(ValueError, match="Invalid MIME type 'text/csv/extra'. MIME types should be in format 'type/subtype'"):
        ChatAreaInput(accept="text/csv/extra")


def test_chat_area_input_mixed_valid_invalid():
    """Test that one invalid entry in a list causes the whole thing to fail."""
    with pytest.raises(ValueError, match="File extension 'csv' should start with a dot"):
        ChatAreaInput(accept=".json,csv")

    with pytest.raises(ValueError, match="Invalid MIME type 'text/.pdf'"):
        ChatAreaInput(accept="text/csv,text/.pdf")


def test_chat_area_input_edge_cases():
    """Test edge cases in accept parameter validation."""
    # Whitespace should be handled
    ChatAreaInput(accept=" .csv , .json ")
    ChatAreaInput(accept=" text/csv , application/json ")

    # Empty entries should be skipped
    ChatAreaInput(accept=".csv,,,.json")

    # Long extensions (>10 chars) should not be flagged as missing dot
    ChatAreaInput(accept="verylongextensionname")


def test_chat_area_input_basic_functionality():
    """Test basic ChatAreaInput functionality without accept parameter."""
    chat_input = ChatAreaInput(placeholder="Test placeholder")
    assert chat_input.placeholder == "Test placeholder"
    assert chat_input.accept is None
    assert chat_input.enable_upload is True
    assert chat_input.enter_sends is True
