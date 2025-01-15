from __future__ import annotations

from typing import Any

import param
from panel.models.reactive_html import DOMEvent
from panel.util import edit_readonly
from panel.widgets.input import FileInput as _PnFileInput

from ..base import COLORS
from .base import MaterialWidget


class _TextInputBase(MaterialWidget):
    color = param.Selector(objects=COLORS, default="primary")

    description = param.String(
        default=None,
        doc="""
        An HTML string describing the function of this component.""",
    )

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

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

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

    Some missing features (if any) when comparing with the corresponding
    panel TextInput widget [panel.widgets.TextInput](https://panel.holoviz.org/reference/widgets/TextInput.html):
    - Missing features: enter_pressed

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

    indeterminate = param.Boolean(default=False)

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(default=False)

    _esm_base = "Checkbox.jsx"


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

    edge = param.Selector(objects=["start", "end", False], default=False)

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(default=False)

    width = param.Boolean(default=None)

    _esm_base = "Switch.jsx"


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

    width = param.Integer(default=None)

    _esm_base = "FileInput.jsx"

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
