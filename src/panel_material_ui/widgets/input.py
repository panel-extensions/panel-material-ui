from __future__ import annotations

import inspect
from collections.abc import Iterable
from datetime import date, datetime, timezone
from datetime import time as dt_time
from logging import getLogger
from typing import TYPE_CHECKING, Any

import numpy as np
import panel as pn
import param
from bokeh.models.formatters import NumeralTickFormatter, TickFormatter
from panel.models.reactive_html import DOMEvent
from panel.util import edit_readonly, try_datetime64_to_datetime
from panel.widgets.input import DatetimeInput as _PnDatetimeInput
from panel.widgets.input import FileInput as _PnFileInput
from panel.widgets.input import LiteralInput as _PnLiteralInput

from .._param import Date, DateList, Datetime
from ..base import COLORS, LoadingTransform, ThemedTransform
from ._mime import MIME_TYPES, NoConverter
from .base import MaterialWidget, TooltipTransform
from .button import _ButtonBase

if TYPE_CHECKING:
    from bokeh.document import Document

logger = getLogger(__name__)


class MaterialInputWidget(MaterialWidget):

    color = param.Selector(objects=COLORS, default="primary", doc="""
        The color variant of the input.""")

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined", doc="""
        The variant of the input.""")

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

    size = param.Selector(objects=["small", "medium"], default="medium")

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

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/TextInput.html
    - https://panel.holoviz.org/reference/widgets/TextInput.html
    - https://mui.com/material-ui/react-text-field/

    :Example:

    >>> TextInput(label='Name', placeholder='Enter your name here ...')
    """

    enter_pressed = param.Event(doc="""
        Event when the enter key has been pressed.""")

    _esm_base = "TextField.jsx"

    def _handle_enter(self, event: DOMEvent):
        self.param.trigger('enter_pressed')


class PasswordInput(_TextInputBase):
    """
    The `PasswordInput` widget allows entering any string using an obfuscated text input box.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/PasswordInput.html
    - https://panel.holoviz.org/reference/widgets/PasswordInput.html
    - https://mui.com/material-ui/react-text-field/#input-adornments

    :Example:

    >>> PasswordInput(label='Password', placeholder='Enter your password here ...')
    """

    enter_pressed = param.Event(doc="""
        Event when the enter key has been pressed.""")

    _esm_base = "PasswordField.jsx"

    def _handle_enter(self, event: DOMEvent):
        self.param.trigger('enter_pressed')


class TextAreaInput(_TextInputBase):
    """
    The `TextAreaInput` allows entering any multiline string using a text input
    box.

    Lines are joined with the newline character `\n`.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/TextAreaInput.html
    - https://panel.holoviz.org/reference/widgets/TextAreaInput.html
    - https://mui.com/material-ui/react-text-field/

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


class MissingFileChunkError(RuntimeError):
    """Exception raised when a chunk is missing during file upload processing."""


class FileInput(_ButtonBase, _PnFileInput):
    """
    The `FileInput` allows the user to upload one or more files to the server.

    It makes the filename, MIME type and (bytes) content available in Python.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/FileInput.html
    - https://panel.holoviz.org/reference/widgets/FileInput.html
    - https://mui.com/material-ui/react-button/#file-upload

    :Example:

    >>> FileInput(accept='.png,.jpeg', multiple=True)
    """

    chunk_size = param.Integer(default=10_485_760, bounds=(1, None), doc="""
        Maximum size (in bytes) of each chunk for chunked file uploads.
        Defaults to 10 MB. Files will be uploaded in chunks of this size to
        avoid WebSocket message size limitations.""")

    max_file_size = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum size (in bytes) for individual files. If specified, files
        larger than this limit will be rejected on the frontend before upload.""")

    max_total_file_size = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum total size (in bytes) for all files combined. If specified,
        uploads will be rejected if the total size exceeds this limit.""")

    width = param.Integer(default=None)

    _esm_base = "FileInput.jsx"
    _source_transforms = {
        'filename': None,
        'value': "'data:' + source.mime_type + ';base64,' + value"
    }

    _mime_types = MIME_TYPES

    def __init__(self, **params):
        super().__init__(**params)
        self._buffer = []
        self._file_buffer = {}  # Buffer for chunked file uploads
        self._object = None

    def _handle_msg(self, msg: Any) -> None:
        status = msg["status"]
        if status == "upload_event":
            self._process_chunk(msg)
            return
        elif status == "initializing":
            return
        elif status == "finished":
            try:
                self._flush_buffer()
                self._send_msg({"status": "finished"})
            except Exception as e:
                logger.exception(str(e))
                self._send_msg({"status": "error", "error": str(e)})
        else:
            raise ValueError(f"Unknown status: {status}")

    def _process_chunk(self, msg: dict) -> None:
        """Process a single chunk of a chunked file upload."""
        name = msg["name"]
        chunk = msg["chunk"]
        total_chunks = msg["total_chunks"]
        mime_type = msg["type"]

        data = msg["data"]
        data = bytes(data)

        if name not in self._file_buffer:
            self._file_buffer[name] = {
                "chunks": {},
                "total_chunks": total_chunks,
                "mime_type": mime_type,
                "filename": name
            }

        self._file_buffer[name]["chunks"][chunk] = data

        # Check if all chunks are received for this file
        if len(self._file_buffer[name]["chunks"]) == total_chunks:
            # Reassemble the file
            file_data = b""
            for i in range(1, total_chunks + 1):  # Chunks are 1-indexed
                file_data += self._file_buffer[name]["chunks"][i]

            self._buffer.append({
                "value": file_data,
                "filename": name,
                "mime_type": mime_type
            })

            del self._file_buffer[name]

    def _flush_buffer(self):
        value, mime_type, filename = [], [], []
        for file_data in self._buffer:
            value.append(file_data["value"])
            filename.append(file_data["filename"])
            mime_type.append(file_data["mime_type"])
        if value:
            if not (self.multiple or self.directory):
                value, filename, mime_type = value[0], filename[0], mime_type[0]
        else:
            value, filename, mime_type = None, None, None
        self.param.update(
            filename=filename,
            mime_type=mime_type,
            value=value,
        )
        self._buffer.clear()

    def save(self, filename):
        """
        Saves the uploaded FileInput data object(s) to file(s) or
        BytesIO object(s).

        Parameters
        ----------
        filename (str or list[str]): File path or file-like object
        """
        _PnFileInput.save(self, filename)

    def clear(self):
        """
        Clear the file(s) in the FileInput widget
        """
        self.param.update(value=None, filename=None, mime_type=None)

    @param.depends('value', 'filename', 'mime_type', watch=True)
    def _reset_object(self):
        self._object = None

    @classmethod
    def _single_object(cls, value: bytes, filename: str, mime_type: str):
        """
        Create a single viewable Python object from the uploaded file.

        Parameters
        ----------
        value : bytes
            The file content as bytes.
        filename : str
            The name of the uploaded file.
        mime_type : str
            The MIME type of the uploaded file.

        Returns
        -------
        Panel component
            A viewable Python object or Panel component for the uploaded file.
        """
        if mime_type in cls._mime_types:
            config = cls._mime_types[mime_type]
            if "converter" in config:
                to_object_func = config['converter']
                try:
                    return to_object_func(value)
                except Exception as exc:
                    return exc

        msg = f"No specific converter available for '{filename}' of mime type '{mime_type}'."
        return NoConverter(msg)

    @param.depends('value', 'filename', 'mime_type')
    def object(self):
        """Returns the currently uploaded file(s) as a viewable Python object or list of viewable Python objects.

        For example an uploaded CSV file will return a Pandas DataFrame, an uploaded MP3 file will return the path to a temporary file etc.
        """
        if not self._object:
            value = self.value
            filename = self.filename
            mime_type = self.mime_type
            if not value:
                self._object = value
            elif not isinstance(value, list):
                self._object = self._single_object(value, filename, mime_type)
            else:
                self._object = [self._single_object(v, f, m) for v, f, m in zip(value, filename, mime_type, strict=False)]
        return self._object

    @classmethod
    def _single_view(cls, object, filename, mime_type, **kwargs):
        """
        Create a Panel component to view a single uploaded file.

        Parameters
        ----------
        value : bytes
            The file content as bytes.
        filename : str
            The name of the uploaded file.
        mime_type : str
            The MIME type of the uploaded file.
        **kwargs
            Additional layout keyword arguments passed to the Panel component.

        Returns
        -------
        Panel component
            A Tabulator widget for CSV files, or a Markdown pane with an error message
            for unsupported file types.
        """
        kwargs["name"] = filename
        view = pn.panel

        if isinstance(object, Exception):
            from panel_material_ui.layout import Alert
            view = Alert
            kwargs["severity"] = "error"
            kwargs["margin"] = 10
            object = str(object)
        elif mime_type in cls._mime_types:
            config = cls._mime_types[mime_type]
            if "view" in config:
                view = config['view']
            if "view_kwargs" in config:
                kwargs.update(config['view_kwargs'])

        if inspect.isclass(view) and issubclass(view, pn.widgets.Widget):
            return view(value=object, **kwargs)
        return view(object, **kwargs)

    def _list_view(self, value, filename, mime_type, object_if_no_value, layout, **kwargs):
        """
        Create a Panel layout to view multiple uploaded files or handle empty state.

        Parameters
        ----------
        value : list or bytes or None
            The file content(s). Can be a list of bytes for multiple files,
            bytes for a single file, or None for no files.
        filename : list or str or None
            The filename(s) corresponding to the uploaded files.
        mime_type : list or str or None
            The MIME type(s) corresponding to the uploaded files.
        object_if_no_value : Panel component, optional
            Component to display when no files are uploaded.
        layout : Panel layout class
            The layout class to use for organizing multiple file views.
        **kwargs
            Additional layout keyword arguments passed to the layout component.

        Returns
        -------
        Panel component
            A layout containing file views, the object_if_no_value component,
            or an invisible layout if no files and no object_if_no_value is provided.
        """
        if not value:
            if object_if_no_value is not None:
                return object_if_no_value
            return layout(visible=False)
        if not isinstance(value, list):
            return self._single_view(self.object(), filename=self.filename, mime_type=self.mime_type, **kwargs)

        single_view_sizing_mode="stretch_both"
        if hasattr(layout, "dynamic") and "dynamic" not in kwargs:
            kwargs['dynamic'] = True
        return layout(
            *[
                self._single_view(object=o, filename=f, mime_type=m, sizing_mode=single_view_sizing_mode)
                for o, f, m in zip(self.object(), self.filename, self.mime_type, strict=True)], **kwargs
        )

    def view(self, *, object_if_no_value=None, layout=None, **kwargs):
        """
        Create a bound Panel component for viewing the uploaded file(s).

        This method creates a view of the currently uploaded file(s). It updates
        when the uploaded file value changes.

        Parameters
        ----------
        object_if_no_value : Displayble Python object, optional
            Object to display when no files are uploaded. If None,
            an invisible layout will be shown when no files are present.
        layout : Panel layout class, optional
            The layout class to use for organizing multiple file views.
            If None, defaults to panel_material_ui.Tabs.
        **kwargs
            Additional keyword arguments passed to the layout component.

        Returns
        -------
        Panel bound function
            A Panel bind object that reactively updates the file view
            when the FileInput parameters change.

        Examples
        --------
        >>> file_input = FileInput()
        >>> file_view = file_input.view(layout=pmui.Column)
        >>> # The view will automatically update when files are uploaded
        """
        if not layout:
            from panel_material_ui.layout import Tabs
            layout = Tabs
        return param.bind(
            self._list_view,
            value=self.param.value,
            filename=self.param.filename,
            mime_type=self.param.mime_type,
            object_if_no_value=object_if_no_value,
            layout=layout,
            **kwargs
        )


class _NumericInputBase(MaterialInputWidget):

    format = param.ClassSelector(default=None, class_=(str, TickFormatter,), doc="""
        Allows defining a custom format string or bokeh TickFormatter.""")

    placeholder = param.String(default='0', doc="""
        Placeholder for empty input field.""")

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    start = param.Parameter(default=None, allow_None=True, doc="""
        Optional minimum allowable value.""")

    end = param.Parameter(default=None, allow_None=True, doc="""
        Optional maximum allowable value.""")

    value = param.Number(default=0, allow_None=True, doc="""
        The current value of the spinner.""")

    __abstract = True

    def __init__(self, **params):
        if 'value' not in params:
            value = params.get('start', self.value)
            if value is not None:
                params['value'] = value
        if 'value' in params and 'value_throttled' in self.param:
            params['value_throttled'] = params['value']
        super().__init__(**params)

    def _get_properties(self, doc: Document):
        props = super()._get_properties(doc)
        if props['data'].format is None:
            props['data'].format = NumeralTickFormatter(format='0,0' if self.mode == 'int' else '0,0.0[000]')
        return props

    def _process_param_change(self, params):
        if 'format' in params and isinstance(params['format'], str):
            params['format'] = NumeralTickFormatter(format=params['format'])
        return super()._process_param_change(params)


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

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/IntInput.html
    - https://panel.holoviz.org/reference/widgets/IntInput.html
    - https://mui.com/material-ui/react-text-field/#input-adornments

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

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/FloatInput.html
    - https://panel.holoviz.org/reference/widgets/FloatInput.html

    :Example:

    >>> FloatInput(label='Value', value=100, start=0, end=1000, step=10)
    """

    step = param.Number(default=0.1, doc="""
        The step size.""")

    value_throttled = param.Number(default=None, constant=True, doc="""
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

    clearable = param.Boolean(default=False, doc="If True, allows the date to be cleared.")

    disabled_dates = DateList(default=None, doc="""
      Dates to make unavailable for selection.""")

    disable_future = param.Boolean(default=False, doc="If true, future dates are disabled.")

    disable_past = param.Boolean(default=False, doc="If true, past dates are disabled.")

    enabled_dates = DateList(default=None, doc="""
      Dates to make available for selection.""")

    end = Date(default=None, doc="The maximum selectable date.")

    format = param.String(default='YYYY-MM-DD', doc="Format of the date when rendered in the input(s). Defaults to localized format based on the used views.")

    open_to = param.Selector(objects=['year', 'month', 'day'], default='day', doc="The default view to open the calendar to.")

    start = Date(default=None, doc="The minimum selectable date.")

    value = Date(default=None, doc="The selected date.")

    views = param.List(default=['year', 'day'], doc="The views that are available for the date picker.")

    width = param.Integer(default=300, allow_None=True, doc="""
      Width of this component. If sizing_mode is set to stretch
      or scale mode this will merely be used as a suggestion.""")

    _esm_base = "DateTimePicker.jsx"

    _constants = {'range': False, 'time': False}

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
            elif isinstance(value, float):
                msg[p] = datetime.fromtimestamp(value / 1000, tz=timezone.utc).date()
        return msg


class DatePicker(_DatePickerBase):
    """
    The `DatePicker` allows selecting a `date` value using a text box
    and a date-picking utility.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/DatePicker.html
    - https://panel.holoviz.org/reference/widgets/DatePicker.html
    - https://mui.com/x/react-date-pickers/date-picker/

    :Example:

    >>> DatePicker(
    ...     value=date(2025,1,1),
    ...     start=date(2025,1,1), end=date(2025,12,31),
    ...     name='Date'
    ... )
    """

    _constants = {'range': False, 'time': False}

    value = Date(default=None, doc="""
        The current value. Can be a datetime object or a string in ISO format.""")

    def _serialize_value(self, value):
        """Convert value for sending to JavaScript."""
        if isinstance(value, str) and value:
            try:
                if self.as_numpy_datetime64:
                    return np.datetime64(value)
                else:
                    return self._parse_datetime_string(value)
            except ValueError:
                return None
        return value


class _DatetimePickerBase(_DatePickerBase):
    """Base class for DatetimePicker components."""

    enable_seconds = param.Boolean(default=True, doc="""
      Enable editing of the seconds in the widget.""")

    enable_time = param.Boolean(default=True, doc="""
      Enable editing of the time in the widget.""")

    format = param.String(default=None, doc="""
        Format to display the datetime. Use custom format string based on dayjs.
        If None, will be set automatically based on military_time setting.
        For 12-hour: 'YYYY-MM-DD hh:mm a'
        For 24-hour: 'YYYY-MM-DD HH:mm'
        Add ':ss' to include seconds.""")

    military_time = param.Boolean(default=True, doc="""
      Whether to display time in 24 hour format.""")

    open_to = param.Selector(objects=['year', 'month', 'day', 'hours', 'minutes'], default=None, doc="""
      The default view to open the calendar to.""")

    views = param.List(default=['year', 'month', 'day', 'hours', 'minutes'], doc="""
      The views that are available for the date picker.""")

    _constants = {'range': False, 'time': True}

    __abstract = True

    def __init__(self, **params):
        # Preserve original value
        original_value = None
        if 'value' in params:
            original_value = params['value']

        # Handle value as string - we want to preserve the datetime object
        if 'value' in params and isinstance(params['value'], str):
            params['value'] = self._parse_datetime_string(params['value'])

        super().__init__(**params)

        # Override any date-only conversion that might have happened in parent class
        if original_value is not None and isinstance(original_value, (datetime, str)) and hasattr(self, 'value'):
            if isinstance(original_value, str):
                self.value = self._parse_datetime_string(original_value)
            elif isinstance(original_value, datetime):
                self.value = original_value

        # Set default format based on military_time
        if self.format is None:
            self._update_format_from_settings()

    @param.depends('military_time', 'enable_seconds', watch=True)
    def _update_format_from_settings(self):
        """Update format based on clock and seconds settings."""
        if self.military_time:
            self.format = 'YYYY-MM-DD HH:mm' + (':ss' if self.enable_seconds else '')
        else:
            self.format = 'YYYY-MM-DD hh:mm' + (':ss' if self.enable_seconds else '') + ' a'

    @staticmethod
    def _parse_datetime_string(value_str):
        """Convert datetime string to datetime object."""
        if not value_str:
            return None

        formats = [
            '%Y-%m-%d %H:%M:%S',  # 2023-01-01 14:30:00
            '%Y-%m-%d %H:%M',     # 2023-01-01 14:30
            '%Y-%m-%dT%H:%M:%S',  # 2023-01-01T14:30:00
            '%Y-%m-%dT%H:%M'      # 2023-01-01T14:30
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value_str, fmt)
            except ValueError:
                continue

        # If we can't parse it as datetime, try date only
        try:
            return datetime.strptime(value_str, '%Y-%m-%d')
        except ValueError as exc:
            raise ValueError(f"Could not parse '{value_str}' as a datetime") from exc

    def _convert_to_datetime(self, v):
        if v is None:
            return None

        if isinstance(v, Iterable) and not isinstance(v, str):
            container_type = type(v)
            return container_type(
                self._convert_to_datetime(vv)
                for vv in v
            )

        # Handle string conversion
        if isinstance(v, str):
            return self._parse_datetime_string(v)

        # Handle other types
        v = try_datetime64_to_datetime(v)
        if isinstance(v, datetime):
            return v
        elif isinstance(v, date):
            # Convert date to datetime
            return datetime(v.year, v.month, v.day)
        else:
            raise ValueError(f"Could not convert {v} to datetime")

    def _process_property_change(self, msg):
        """Process incoming values from JavaScript.

        IMPORTANT: We completely override the parent method to avoid
        the date-only parsing that causes problems with datetime strings.
        """
        # Get the parent's parent method (MaterialWidget._process_property_change)
        # to avoid _DatePickerBase's implementation which only handles dates
        msg = MaterialWidget._process_property_change(self, msg)

        # Handle our datetime parameters
        for p in ('start', 'end', 'value'):
            if p not in msg:
                continue

            value = msg[p]
            if isinstance(value, str):
                try:
                    # Parse as datetime with time component
                    msg[p] = self._parse_datetime_string(value)
                except ValueError:
                    # If parsing fails, keep the original value
                    pass

        return msg

    def _process_param_change(self, msg):
        """Process outgoing values to JavaScript."""
        # Only handle our specific parameters, let parent class handle the rest
        # This avoids the date-only conversion in the parent class
        our_params = {}
        for p in ('value', 'start', 'end'):
            if p in msg:
                our_params[p] = msg.pop(p)

        # Let parent handle the remaining parameters
        msg = super()._process_param_change(msg)

        # Now handle our parameters
        for p, v in our_params.items():
            if v is not None:
                # Convert to datetime if needed
                dt_value = self._convert_to_datetime(v)
                if dt_value is not None:
                    # Format as string for JavaScript
                    msg[p] = dt_value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    msg[p] = None

        return msg


class DatetimePicker(_DatetimePickerBase):
    """
    The `DatetimePicker` allows selecting selecting a `datetime` value using a
    textbox and a datetime-picking utility.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/DatetimePicker.html
    - https://panel.holoviz.org/reference/widgets/DatetimePicker.html
    - https://mui.com/x/react-date-pickers/date-time-picker/

    :Example:

    >>> DatetimePicker(
    ...    value=datetime(2025,1,1,22,0),
    ...    start=date(2025,1,1), end=date(2025,12,31),
    ...    military_time=True, name='Date and time'
    ... )

    Also supports string values:

    >>> DatetimePicker(
    ...    value="2025-01-01 22:00:00",
    ...    military_time=True, name='Date and time'
    ... )
    """

    end = Datetime(default=None, doc="The maximum selectable datetime.")

    start = Datetime(default=None, doc="The minimum selectable datetime.")

    value = Datetime(default=None, doc="""
        The current value. Can be a datetime object or a string in ISO format.""")

    _source_transforms = {
        "value": None, "start": None, "end": None
    }

    def _serialize_value(self, value):
        """Convert value for sending to JavaScript."""
        if isinstance(value, str) and value:
            try:
                if self.as_numpy_datetime64:
                    return np.datetime64(value)
                else:
                    return self._parse_datetime_string(value)
            except ValueError:
                return None
        return value



class _TimeCommon(MaterialWidget):

    clock = param.Selector(default='12h', objects=['12h', '24h'], doc="""
        Whether to use 12 hour or 24 hour clock.""")

    hour_increment = param.Integer(default=1, bounds=(1, None), doc="""
        Defines the granularity of hour value increments in the UI.""")

    minute_increment = param.Integer(default=1, bounds=(1, None), doc="""
        Defines the granularity of minute value increments in the UI.""")

    second_increment = param.Integer(default=1, bounds=(1, None), doc="""
        Defines the granularity of second value increments in the UI.""")

    seconds = param.Boolean(default=False, doc="""
        Allows to select seconds. By default only hours and minutes are
        selectable, and AM/PM depending on the `clock` option.""")

    __abstract = True


class TimePicker(_TimeCommon):
    """
    The `TimePicker` allows selecting a `time` value using a text box
    and a time-picking utility.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/TimePicker.html
    - https://panel.holoviz.org/reference/widgets/TimePicker.html
    - https://mui.com/x/react-date-pickers/time-picker/

    :Example:

    >>> TimePicker(
    ...     value=time(12, 59, 31), start="09:00:00", end="18:00:00", label="Time"
    ... )
    """

    color = param.Selector(objects=COLORS, default="primary")

    value = param.ClassSelector(default=None, class_=(dt_time, str), doc="""
        The current value""")

    start = param.ClassSelector(default=None, class_=(dt_time, str), doc="""
        Inclusive lower bound of the allowed time selection""")

    end = param.ClassSelector(default=None, class_=(dt_time, str), doc="""
        Inclusive upper bound of the allowed time selection""")

    format = param.String(default=None, doc="""
        Format to display the time. Use 'HH:mm:ss' to include seconds.
        For 12-hour clock, use 'hh:mm a'. See dayjs formatting options.
        If None, will be automatically set based on clock and seconds settings.

        +----+------------------------------------+------------+
        | H  | Hours                              | 0 to 23    |
        | HH | Hours, 2-digits                    | 00 to 23   |
        | h  | Hours, 12-hour clock               | 1 to 12    |
        | hh | Hours, 12-hour clock, 2-digits     | 1 to 12    |
        | m  | Minutes                            | 0 to 59    |
        | mm | Minutes                            | 00 to 59   |
        | s  | Seconds                            | 0, 1 to 59 |
        | ss | Seconds                            | 00 to 59   |
        | a  | am/pm, lower-case                  | am or pm   |
        | A  | AM/PM, upper-cas                   | AM or PM   |
        +----+------------------------------------+------------+

    """)

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm_base = "TimePicker.jsx"

    def __init__(self, **params):
        # Convert time objects to appropriate string format if needed
        for attr in ['value', 'start', 'end']:
            if attr in params and isinstance(params[attr], dt_time):
                params[attr] = params[attr].strftime('%H:%M:%S')

        super().__init__(**params)

        # Set initial format based on clock and seconds if not explicitly provided
        if self.format is None:
            self._update_format_from_settings()

    @param.depends('clock', 'seconds', watch=True)
    def _update_format_from_settings(self):
        """Update the time format based on clock and seconds settings."""
        if self.clock == '12h':
            self.format = 'hh:mm a' if not self.seconds else 'hh:mm:ss a'
        else:  # 24h
            self.format = 'HH:mm' if not self.seconds else 'HH:mm:ss'

    def _process_param_change(self, msg):
        msg = super()._process_param_change(msg)
        if 'value' in msg and isinstance(msg['value'], dt_time):
            msg['value'] = msg['value'].strftime('%H:%M:%S')
        if 'start' in msg and isinstance(msg['start'], dt_time):
            msg['start'] = msg['start'].strftime('%H:%M:%S')
        if 'end' in msg and isinstance(msg['end'], dt_time):
            msg['end'] = msg['end'].strftime('%H:%M:%S')
        if 'format' in msg and msg['format'] is not None:
            msg['format'] = msg['format'].replace('K', 'A').replace('G', 'HH').replace('i', 'mm')
        return msg

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        # Convert string time values to datetime.time objects
        if 'value' in msg:
            time_str = msg['value']
            if time_str and isinstance(time_str, str):
                time_parts = time_str.split(':')
                if len(time_parts) >= 2:
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])
                    seconds = int(time_parts[2]) if len(time_parts) > 2 else 0
                    msg['value'] = dt_time(hours, minutes, seconds)
        return msg


class Checkbox(MaterialWidget):
    """
    The `Checkbox` allows toggling a single condition between `True`/`False`
    states by ticking a checkbox.

    This widget is interchangeable with the `Switch` widget.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Checkbox.html
    - https://panel.holoviz.org/reference/widgets/Checkbox.html
    - https://mui.com/material-ui/react-checkbox/

    :Example:

    >>> Checkbox(label='Works with the tools you know and love', value=True)
    """

    color = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the checkbox.""")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    indeterminate = param.Boolean(default=False, doc="""
        Whether the checkbox can be in an indeterminate state. The indeterminate state
        may only be set in Python.""")

    size = param.Selector(objects=["small", "medium", "large"], default="medium", doc="""
        The size of the checkbox.""")

    value = param.Boolean(default=False)

    width = param.Integer(default=None)

    _esm_base = "Checkbox.jsx"
    _esm_transforms = [TooltipTransform, LoadingTransform, ThemedTransform]

    def __init__(self, **params):
        is_indeterminate = 'indeterminate' in params and 'value' in params and params['value'] is None
        if is_indeterminate:
            params.pop('value')
        super().__init__(**params)
        if is_indeterminate:
            self.value = None

    def _process_param_change(self, params):
        props = super()._process_param_change(params)
        if 'value' in props and self.indeterminate:
            is_none = props['value'] is None
            props['indeterminate'] = is_none
            if is_none:
                del props['value']
        return props

    @param.depends('indeterminate', watch=True, on_init=True)
    def _set_allow_none(self):
        self.param.value.allow_None = self.indeterminate


class Switch(MaterialWidget):
    """
    The `Switch` allows toggling a single condition between `True`/`False`
    states by ticking a checkbox.

    This widget is interchangeable with the `Checkbox` widget.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Switch.html
    - https://panel.holoviz.org/reference/widgets/Switch.html
    - https://mui.com/material-ui/react-switch/

    :Example:

    >>> Switch(label='Works with the tools you know and love', value=True)
    """

    color = param.Selector(objects=COLORS, default="primary")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    edge = param.Selector(objects=["start", "end", False], default=False)

    size = param.Selector(objects=["small", "medium"], default="medium")

    value = param.Boolean(default=False)

    width = param.Boolean(default=None)

    _esm_base = "Switch.jsx"
    _esm_transforms = [LoadingTransform, TooltipTransform, ThemedTransform]


class ColorPicker(MaterialWidget):
    """
    The `ColorPicker` allows selecting a color value using a color picker utility.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/ColorPicker.html
    - https://panel.holoviz.org/reference/widgets/ColorPicker.html
    - https://viclafouch.github.io/mui-color-input/

    :Example:

    >>> pmui.ColorPicker(name='Color Picker', value='#99ef78')
    """

    alpha = param.Boolean(default=False, doc="Whether to display input controls for a color's alpha (transparency) channel.")

    color = param.Selector(objects=COLORS, default="primary", doc="The accent color of the color picker when active or focused.")

    format = param.Selector(objects=["hex", "rgb", "rgba", "hsl", "hsv"], default="hex", doc="""
        The format of the color value.
        - `hex`: The hex color value.
        - `rgb`: The rgb color value.
        - `rgba`: The rgba color value.
        - `hsl`: The hsl color value.
        - `hsv`: The hsv color value.""")

    size = param.Selector(objects=["small", "medium", "large"], default="medium", doc="The visual size of the input field")

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined", doc="The visual style variant of the input field")

    value = param.String(default=None, doc="The current color value.")

    _esm_base = "ColorPicker.jsx"


class LiteralInput(TextInput, _PnLiteralInput):
    """
    The `LiteralInput` allows entering any string using a text input box.

    :References:

    - https://panel.holoviz.org/reference/widgets/LiteralInput.html
    """

    value = param.Parameter()

    value_input = param.Parameter()

    def _process_param_change(self, msg):
        msg = super()._process_param_change(msg)
        if self._state:
            msg["error_state"] = True
        else:
            msg["error_state"] = False
        if "value" in msg:
            msg["value_input"] = msg.pop("value")
        if "title" in msg:
            msg["label"] = msg.pop("title")
        return msg


class DatetimeInput(TextInput, _PnDatetimeInput):
    """
    The `DatetimeInput` allows entering a datetime value using a text input box.
    """

    value = param.ClassSelector(default=None, class_=(datetime, date, str), doc="""
        The current value. Can be a datetime object or a string in ISO format.""")

    value_input = param.ClassSelector(default=None, class_=(datetime, date, str), doc="""
        The current value. Can be a datetime object or a string in ISO format.""")

    _source_transforms = {
        "value": None, "value_input": None, "start": None, "end": None
    }

    def _process_param_change(self, msg):
        msg = super()._process_param_change(msg)
        if self._state:
            msg["error_state"] = True
        else:
            msg["error_state"] = False
        if "value" in msg:
            msg["value_input"] = msg.pop("value")
        if "title" in msg:
            msg["label"] = msg.pop("title")
        return msg


class DictInput(LiteralInput):
    """
    The `DictInput` allows entering a dictionary value using a text input box.
    """

    type = param.ClassSelector(default=dict, class_=type, readonly=True, doc="The type of the value.")

    value = param.Parameter(default={})


class ListInput(LiteralInput):
    """
    The `ListInput` allows entering a list value using a text input box.
    """

    type = param.ClassSelector(default=list, class_=type, readonly=True, doc="The type of the value.")

    value = param.Parameter(default=[])


class TupleInput(LiteralInput):
    """
    The `TupleInput` allows entering a tuple value using a text input box.
    """

    type = param.ClassSelector(default=tuple, class_=type, readonly=True, doc="The type of the value.")

    value = param.Parameter(default=())


__all__ = [
    "TextInput",
    "PasswordInput",
    "TextAreaInput",
    "FileInput",
    "IntInput",
    "FloatInput",
    "NumberInput",
    "DatePicker",
    "DatetimePicker",
    "TimePicker",
    "Checkbox",
    "Switch",
    "ColorPicker",
    "LiteralInput",
    "DatetimeInput",
    "DictInput",
    "ListInput",
    "TupleInput"
]
