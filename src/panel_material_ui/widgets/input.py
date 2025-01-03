from __future__ import annotations

from typing import Any

import param
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
        doc="""
        Initial or entered text value updated on every key press.""",
    )

    _constants = {"multiline": False}

    __abstract = True


class TextInput(_TextInputBase):
    """
    The `TextInput` widget allows entering any string using a text input box.

    Some missing and extra features (if any) when comparing with the corresponding
    panel TextInput widget [panel.widgets.TextInput](https://panel.holoviz.org/reference/widgets/TextInput.html):
    - Missing features: enter_pressed
    - Extra features: color, error_state, label, on_event, on_msg, theme, variant

    :Example:

    >>> TextInput(name='Name', placeholder='Enter your name here ...')
    """

    _esm = "TextField.jsx"


class PasswordInput(_TextInputBase):
    """
    The `PasswordInput` widget allows entering any string using an obfuscated text input box.

    Some missing and extra features (if any) when comparing with the corresponding
    panel PasswordInput widget [panel.widgets.PasswordInput](https://panel.holoviz.org/reference/widgets/PasswordInput.html):
    - No missing features
    - Extra features: color, error_state, label, on_event, on_msg, theme, variant

    :Example:

    >>> PasswordInput(label='Password', placeholder='Enter your password here ...')
    """

    _esm = "PasswordField.jsx"


class TextAreaInput(_TextInputBase):
    """
    The `TextAreaInput` allows entering any multiline string using a text input
    box.

    Lines are joined with the newline character `\n`.

    Some missing and extra features (if any) when comparing with the corresponding
    panel TextAreaInput widget [panel.widgets.TextAreaInput](https://panel.holoviz.org/reference/widgets/TextAreaInput.html):
    - No missing features
    - Extra features: color, error_state, label, on_event, on_msg, theme, variant

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

    _esm = "TextArea.jsx"


class Checkbox(MaterialWidget):
    """
    The `Checkbox` allows toggling a single condition between `True`/`False`
    states by ticking a checkbox.

    This widget is interchangeable with the `Switch` widget.

    Some missing and extra features (if any) when comparing with the corresponding
    panel Checkbox widget [panel.widgets.Checkbox](https://panel.holoviz.org/reference/widgets/Checkbox.html):
    - No missing features
    - Extra features: color, description, indeterminate, label, on_event, on_msg, size, theme

    :Example:

    >>> Checkbox(label='Works with the tools you know and love', value=True)
    """

    color = param.Selector(objects=COLORS, default="primary")

    indeterminate = param.Boolean(default=False)

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(default=False)

    _esm = "Checkbox.jsx"


class Switch(MaterialWidget):
    """
    The `Switch` allows toggling a single condition between `True`/`False`
    states by ticking a checkbox.

    This widget is interchangeable with the `Checkbox` widget.

    Some missing and extra features (if any) when comparing with the corresponding
    panel Switch widget [panel.widgets.Switch](https://panel.holoviz.org/reference/widgets/Switch.html):
    - No missing features
    - Extra features: color, description, edge, label, on_event, on_msg, size, theme

    :Example:

    >>> Switch(label='Works with the tools you know and love', value=True)
    """

    color = param.Selector(objects=["default"] + COLORS, default="primary")

    edge = param.Selector(objects=["start", "end", False], default=False)

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(default=False)

    width = param.Boolean(default=None)

    _esm = "Switch.jsx"


class FileInput(MaterialWidget, _PnFileInput):
    """
    The `FileInput` allows the user to upload one or more files to the server.

    It makes the filename, MIME type and (bytes) content available in Python.

    Some missing and extra features (if any) when comparing with the corresponding
    panel FileInput widget [panel.widgets.FileInput](https://panel.holoviz.org/reference/widgets/FileInput.html):
    - No missing features
    - Extra features: button_style, button_type, label, on_event, on_msg, theme

    :Example:

    >>> FileInput(accept='.png,.jpeg', multiple=True)
    """

    button_type = param.Selector(objects=COLORS, default="primary")

    button_style = param.Selector(objects=["contained", "outlined", "text"], default="contained")

    width = param.Integer(default=None)

    _esm = "FileInput.jsx"

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
