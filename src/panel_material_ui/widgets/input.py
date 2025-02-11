from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime
from datetime import time as dt_time
from typing import Any

import numpy as np
import param
from bokeh.models.formatters import TickFormatter
from panel.models.reactive_html import DOMEvent
from panel.util import edit_readonly, try_datetime64_to_datetime
from panel.widgets.input import FileInput as _PnFileInput

from ..base import COLORS, ThemedTransform
from .base import MaterialWidget, TooltipTransform


class MaterialInputWidget(MaterialWidget):

    color = param.Selector(objects=COLORS, default="primary")

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    __abstract = True


class _TextInputBase(MaterialInputWidget):

    error_state = param.Boolean(
        default=False,
        doc="""
        Whether to display in error state.""",
    )

    max_length = param.Integer(
        default=5000,
        doc="""
        Max count of characters in the input field.""",
    )

    placeholder = param.String(
        default="",
        doc="""
        Placeholder for empty input field.""",
    )

    value = param.String(default="")

    value_input = param.String(
        default="",
        allow_None=True,
        readonly=True,
        doc="""
        Initial or entered text value updated on every key press.""",
    )

    _constants = {"multiline": False}

    __abstract = True

    @param.depends('value', watch=True, on_init=True)
    def _sync_value_input(self):
        with edit_readonly(self):
            self.value_input = self.value


class TextInput(_TextInputBase):
    """
    The `TextInput` widget allows entering any string using a text input box.

    Reference to the corresponding panel PasswordInput widget:
    https://panel.holoviz.org/reference/widgets/PasswordInput.html

    :Example:

    >>> TextInput(name='Name', placeholder='Enter your name here ...')
    """

    enter_pressed = param.Event(doc="""
        Event when the enter key has been pressed.""")

    _esm_base = "TextField.jsx"

    def _handle_enter(self, event: DOMEvent):
        self.param.trigger('enter_pressed')


class PasswordInput(_TextInputBase):
    """
    The `PasswordInput` widget allows entering any string using an obfuscated text input box.

    Reference to the corresponding panel PasswordInput widget:
    https://panel.holoviz.org/reference/widgets/PasswordInput.html

    :Example:

    >>> PasswordInput(label='Password', placeholder='Enter your password here ...')
    """

    _esm_base = "PasswordField.jsx"


class TextAreaInput(_TextInputBase):
    """
    The `TextAreaInput` allows entering any multiline string using a text input
    box.

    Lines are joined with the newline character `\n`.

    Reference to the corresponding panel TextAreaInput widget:
    https://panel.holoviz.org/reference/widgets/TextAreaInput.html

    :Example:

    >>> TextAreaInput(
    ...     label='Description', placeholder='Enter your description here...'
    ... )
    """

    auto_grow = param.Boolean(
        default=False,
        doc="""
        Whether the text area should automatically grow vertically to
        accommodate the current text.""",
    )

    cols = param.Integer(
        default=20,
        doc="""
        Number of columns in the text input field.""",
    )

    max_rows = param.Integer(
        default=None,
        doc="""
        When combined with auto_grow this determines the maximum number
        of rows the input area can grow.""",
    )

    rows = param.Integer(
        default=2,
        doc="""
        Number of rows in the text input field.""",
    )

    resizable = param.ObjectSelector(
        objects=["both", "width", "height", False],
        doc="""
        Whether the layout is interactively resizable,
        and if so in which dimensions: `width`, `height`, or `both`.
        Can only be set during initialization.""",
    )

    _esm_base = "TextArea.jsx"


class FileInput(MaterialWidget, _PnFileInput):
    """
    The `FileInput` allows the user to upload one or more files to the server.

    It makes the filename, MIME type and (bytes) content available in Python.

    Reference to the corresponding panel FileInput widget:
    https://panel.holoviz.org/reference/widgets/FileInput.html

    :Example:

    >>> FileInput(accept='.png,.jpeg', multiple=True)
    """

    button_type = param.Selector(objects=COLORS, default="primary")

    button_style = param.Selector(objects=["contained", "outlined", "text"], default="contained")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    width = param.Integer(default=None)

    _esm_base = "FileInput.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]

    def __init__(self, **params):
        super().__init__(**params)
        self._buffer = []

    def _handle_msg(self, msg: Any) -> None:
        status = msg["status"]
        if status == "in_progress":
            self._buffer.append(msg)
            return
        elif status == "initializing":
            return
        value, mime_type, filename = [], [], []
        for file_data in self._buffer:
            value.append(file_data["data"])
            filename.append(file_data["filename"])
            mime_type.append(file_data["mime_type"])
        if self.multiple:
            value, filename, mime_type = value[0], filename[0], mime_type[0]
        self.param.update(
            filename=filename,
            mime_type=mime_type,
            value=value,
        )
        self._buffer.clear()


class _NumericInputBase(MaterialInputWidget):

    format = param.ClassSelector(default=None, class_=(str, TickFormatter,), doc="""
        Allows defining a custom format string or bokeh TickFormatter.""")

    placeholder = param.String(default='0', doc="""
        Placeholder for empty input field.""")

    start = param.Parameter(default=None, allow_None=True, doc="""
        Optional minimum allowable value.""")

    end = param.Parameter(default=None, allow_None=True, doc="""
        Optional maximum allowable value.""")

    value = param.Number(default=0, allow_None=True, doc="""
        The current value of the spinner.""")

    __abstract = True


class _IntInputBase(_NumericInputBase):

    value = param.Integer(default=0, allow_None=True, doc="""
        The current value of the spinner.""")

    start = param.Integer(default=None, allow_None=True, doc="""
        Optional minimum allowable value.""")

    end = param.Integer(default=None, allow_None=True, doc="""
        Optional maximum allowable value.""")

    mode = param.String(default='int', constant=True, doc="""
        Define the type of number which can be enter in the input""")

    __abstract = True


class _FloatInputBase(_NumericInputBase):

    value = param.Number(default=0, allow_None=True, doc="""
        The current value of the spinner.""")

    start = param.Number(default=None, allow_None=True, doc="""
        Optional minimum allowable value.""")

    end = param.Number(default=None, allow_None=True, doc="""
        Optional maximum allowable value.""")

    mode = param.String(default='float', constant=True, doc="""
        Define the type of number which can be enter in the input""")

    __abstract = True


class _SpinnerBase(_NumericInputBase):

    page_step_multiplier = param.Integer(default=10, bounds=(0, None), doc="""
        Defines the multiplication factor applied to step when the page up
        and page down keys are pressed.""")

    wheel_wait = param.Integer(default=100, doc="""
        Defines the debounce time in ms before updating `value_throttled` when
        the mouse wheel is used to change the input.""")

    width = param.Integer(default=300, allow_None=True, doc="""
      Width of this component. If sizing_mode is set to stretch
      or scale mode this will merely be used as a suggestion.""")

    _esm_base = "NumberInput.jsx"

    __abstract = True


class IntInput(_SpinnerBase, _IntInputBase):
    """
    The `IntInput` allows selecting an integer value using a spinbox.

    It behaves like a slider except that lower and upper bounds are optional
    and a specific value can be entered. The value can be changed using the
    keyboard (up, down, page up, page down), mouse wheel and arrow buttons.

    Reference: https://panel.holoviz.org/reference/widgets/IntInput.html

    :Example:

    >>> IntInput(name='Value', value=100, start=0, end=1000, step=10)
    """

    step = param.Integer(default=1, doc="""
        The step size.""")

    value_throttled = param.Integer(default=None, constant=True, doc="""
        The current value. Updates only on `<enter>` or when the widget looses focus.""")


class FloatInput(_SpinnerBase, _FloatInputBase):
    """
    The `FloatInput` allows selecting an integer value using a spinbox.

    It behaves like a slider except that lower and upper bounds are optional
    and a specific value can be entered. The value can be changed using the
    keyboard (up, down, page up, page down), mouse wheel and arrow buttons.

    Reference: https://panel.holoviz.org/reference/widgets/IntInput.html

    :Example:

    >>> FloatInput(name='Value', value=100, start=0, end=1000, step=10)
    """

    step = param.Number(default=0.1, doc="""
        The step size.""")

    value_throttled = param.Integer(default=None, constant=True, doc="""
        The current value. Updates only on `<enter>` or when the widget looses focus.""")


class NumberInput(_SpinnerBase):

    def __new__(self, **params):
        param_list = ["value", "start", "stop", "step"]
        if all(isinstance(params.get(p, 0), int) for p in param_list):
            return IntInput(**params)
        else:
            return FloatInput(**params)


class _DatePickerBase(MaterialInputWidget):

    as_numpy_datetime64 = param.Boolean(default=None, doc="""
        Whether to return values as numpy.datetime64. If left unset,
        will be True if value is a numpy.datetime64, else False.""")

    clearable = param.Boolean(default=True, doc="If true, allows the date to be cleared.")

    disabled_dates = param.List(default=None, item_type=(date, str), doc="""
      Dates to make unavailable for selection.""")

    disable_future = param.Boolean(default=False, doc="If true, future dates are disabled.")

    disable_past = param.Boolean(default=False, doc="If true, past dates are disabled.")

    enabled_dates = param.List(default=None, item_type=(date, str), doc="""
      Dates to make available for selection.""")

    end = param.Date(default=None, doc="The maximum selectable date.")

    format = param.String(default='YYYY-MM-DD', doc="The format of the date displayed in the input.")

    open_to = param.Selector(objects=['year', 'month', 'day'], default='day', doc="The default view to open the calendar to.")

    show_today_button = param.Boolean(default=False, doc="If true, shows a button to select today's date.")

    start = param.Date(default=None, doc="The minimum selectable date.")

    value = param.Date(default=None, doc="The selected date.")

    views = param.List(default=['year', 'month', 'day'], doc="The views that are available for the date picker.")

    width = param.Integer(default=300, allow_None=True, doc="""
      Width of this component. If sizing_mode is set to stretch
      or scale mode this will merely be used as a suggestion.""")

    _esm_base = "DatePicker.jsx"

    __abstract = True

    def __init__(self, **params):
        # Since options is the standard for other widgets,
        # it makes sense to also support options here, converting
        # it to enabled_dates
        if 'options' in params:
            options = list(params.pop('options'))
            params['enabled_dates'] = options
        if 'value' in params:
            value = try_datetime64_to_datetime(params['value'])
            if hasattr(value, "date"):
                value = value.date()
            params["value"] = value
        super().__init__(**params)

    @staticmethod
    def _convert_date_to_string(v):
        return v.strftime('%Y-%m-%d')

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        for p in ('start', 'end', 'value'):
            if p not in msg:
                continue
            value = msg[p]
            if isinstance(value, str):
                msg[p] = datetime.date(datetime.strptime(value, '%Y-%m-%d'))
        return msg


class DatePicker(_DatePickerBase):
    """
    The `DatePicker` allows selecting a `date` value using a text box
    and a date-picking utility.

    Reference: https://panel.holoviz.org/reference/widgets/DatePicker.html

    :Example:

    >>> DatePicker(
    ...     value=date(2025,1,1),
    ...     start=date(2025,1,1), end=date(2025,12,31),
    ...     name='Date'
    ... )
    """

    _constants = {'range': True}

    def _handle_onChange(self, event):
        if 'value' not in event.data:
            return
        self.value = event.data['value'].toISOString().split('T')[0]


class DateRangePicker(_DatePickerBase):
    """
    The `DateRangePicker` allows selecting a `date` range using a text box
    and a date-picking utility.

    Reference: https://panel.holoviz.org/reference/widgets/DateRangePicker.html

    :Example:

    >>> DateRangePicker(
    ...     value=(date(2025,1,1), date(2025,1,5)),
    ...     start=date(2025,1,1), end=date(2025,12,31),
    ...     name='Date range'
    ... )
    """

    start = param.CalendarDate(default=None, doc="""
        Inclusive lower bound of the allowed date selection""")

    end = param.CalendarDate(default=None, doc="""
        Inclusive upper bound of the allowed date selection""")

    value = param.DateRange(default=None, doc="""
        The current value""")

    _constants = {'range': True}

    def __init__(self, **params):
        super().__init__(**params)
        self._update_value_bounds()

    @param.depends('start', 'end', watch=True)
    def _update_value_bounds(self):
        self.param.value.bounds = (self.start, self.end)
        self.param.value._validate(self.value)


class _DatetimePickerBase(_DatePickerBase):

    enable_seconds = param.Boolean(default=True, doc="""
      Enable editing of the seconds in the widget.""")

    enable_time = param.Boolean(default=True, doc="""
      Enable editing of the time in the widget.""")

    format = param.String(default='YYYY-MM-DD hh:mm a', doc="The format of the date displayed in the input.")

    military_time = param.Boolean(default=True, doc="""
      Whether to display time in 24 hour format.""")

    open_to = param.Selector(objects=['year', 'month', 'day'], default='day', doc="The default view to open the calendar to.")

    views = param.List(default=['year', 'month', 'day', 'hours', 'minutes'], doc="The views that are available for the date picker.")

    _esm_base = "DateTimePicker.jsx"

    __abstract = True

    def _convert_to_datetime(self, v):
        if v is None:
            return

        if isinstance(v, Iterable) and not isinstance(v, str):
            container_type = type(v)
            return container_type(
                self._convert_to_datetime(vv)
                for vv in v
            )

        v = try_datetime64_to_datetime(v)
        if isinstance(v, datetime):
            return v
        elif isinstance(v, date):
            return datetime(v.year, v.month, v.day)
        elif isinstance(v, str):
            return datetime.strptime(v, r'%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError(f"Could not convert {v} to datetime")

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        if 'value' in msg:
            msg['value'] = self._serialize_value(msg['value'])
        return msg

    def _process_param_change(self, msg):
        msg = super()._process_param_change(msg)
        if 'value' in msg:
            msg['value'] = self._deserialize_value(self._convert_to_datetime(msg['value']))
        if 'start' in msg:
            msg['start'] = self._convert_to_datetime(msg['start'])
        if 'end' in msg:
            msg['end'] = self._convert_to_datetime(msg['end'])
        return msg


class DatetimePicker(_DatetimePickerBase):
    """
    The `DatetimePicker` allows selecting selecting a `datetime` value using a
    textbox and a datetime-picking utility.

    Reference: https://panel.holoviz.org/reference/widgets/DatetimePicker.html

    :Example:

    >>> DatetimePicker(
    ...    value=datetime(2025,1,1,22,0),
    ...    start=date(2025,1,1), end=date(2025,12,31),
    ...    military_time=True, name='Date and time'
    ... )
    """
    mode = param.String('single', constant=True)

    value = param.Date(default=None)

    def _serialize_value(self, value):
        if isinstance(value, str) and value:
            if self.as_numpy_datetime64:
                value = np.datetime64(value)
            else:
                value = datetime.strptime(value, r'%Y-%m-%d %H:%M:%S')
        return value

    def _deserialize_value(self, value):
        if isinstance(value, (datetime, date)):
            value = value.strftime(r'%Y-%m-%d %H:%M:%S')
        return value


class DatetimeRangePicker(_DatetimePickerBase):
    """
    The `DatetimeRangePicker` allows selecting selecting a `datetime` range
    using a text box and a datetime-range-picking utility.

    Reference: https://panel.holoviz.org/reference/widgets/DatetimeRangePicker.html

    :Example:

    >>> DatetimeRangePicker(
    ...    value=(datetime(2025,1,1,22,0), datetime(2025,1,2,22,0)),
    ...    start=date(2025,1,1), end=date(2025,12,31),
    ...    military_time=True, name='Datetime Range'
    ... )
    """

    value = param.DateRange(default=None, doc="""
        The current value""")



class _TimeCommon(MaterialWidget):

    clock = param.Selector(default='12h', objects=['12h', '24h'], doc="""
        Whether to use 12 hour or 24 hour clock.""")

    hour_increment = param.Integer(default=1, bounds=(1, None), doc="""
    Defines the granularity of hour value increments in the UI.
    """)

    minute_increment = param.Integer(default=1, bounds=(1, None), doc="""
    Defines the granularity of minute value increments in the UI.
    """)

    second_increment = param.Integer(default=1, bounds=(1, None), doc="""
    Defines the granularity of second value increments in the UI.
    """)

    seconds = param.Boolean(default=False, doc="""
    Allows to select seconds. By default only hours and minutes are
    selectable, and AM/PM depending on the `clock` option.
    """)

    __abstract = True


class TimePicker(_TimeCommon):
    """
    The `TimePicker` allows selecting a `time` value using a text box
    and a time-picking utility.

    Reference: https://panel.holoviz.org/reference/widgets/TimePicker.html

    :Example:

    >>> TimePicker(
    ...     value="12:59:31", start="09:00:00", end="18:00:00", name="Time"
    ... )
    """

    color = param.Selector(objects=COLORS, default="primary")

    value = param.ClassSelector(default=None, class_=(dt_time, str), doc="""
        The current value""")

    start = param.ClassSelector(default=None, class_=(dt_time, str), doc="""
        Inclusive lower bound of the allowed time selection""")

    end = param.ClassSelector(default=None, class_=(dt_time, str), doc="""
        Inclusive upper bound of the allowed time selection""")

    format = param.String(default='H:i', doc="""
        Formatting specification for the display of the picked date.

        +---+------------------------------------+------------+
        | H | Hours (24 hours)                   | 00 to 23   |
        | h | Hours                              | 1 to 12    |
        | G | Hours, 2 digits with leading zeros | 1 to 12    |
        | i | Minutes                            | 00 to 59   |
        | S | Seconds, 2 digits                  | 00 to 59   |
        | s | Seconds                            | 0, 1 to 59 |
        | K | AM/PM                              | AM or PM   |
        +---+------------------------------------+------------+

        See also https://flatpickr.js.org/formatting/#date-formatting-tokens.
    """)

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm_base = "TimePicker.jsx"


class Checkbox(MaterialWidget):
    """
    The `Checkbox` allows toggling a single condition between `True`/`False`
    states by ticking a checkbox.

    This widget is interchangeable with the `Switch` widget.

    Reference to the corresponding panel Checkbox widget:
    https://panel.holoviz.org/reference/widgets/Checkbox.html

    :Example:

    >>> Checkbox(label='Works with the tools you know and love', value=True)
    """

    color = param.Selector(objects=COLORS, default="primary")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    indeterminate = param.Boolean(default=False)

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(default=False)

    _esm_base = "Checkbox.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]


class Switch(MaterialWidget):
    """
    The `Switch` allows toggling a single condition between `True`/`False`
    states by ticking a checkbox.

    This widget is interchangeable with the `Checkbox` widget.

    Reference to the corresponding panel Switch widget:
    https://panel.holoviz.org/reference/widgets/Switch.html

    :Example:

    >>> Switch(label='Works with the tools you know and love', value=True)
    """

    color = param.Selector(objects=["default"] + COLORS, default="primary")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    edge = param.Selector(objects=["start", "end", False], default=False)

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(default=False)

    width = param.Boolean(default=None)

    _esm_base = "Switch.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]
