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

    :Example:

    >>> TextInput(name='Name', placeholder='Enter your name here ...')
    """

    _esm = "TextField.jsx"


class PasswordInput(_TextInputBase):
    """
    The `PasswordInput` widget allows entering any string using a text input box.

    :Example:

    >>> PasswordInput(name='Name', placeholder='Enter your name here ...')
    """

    _esm = "PasswordField.jsx"


class TextAreaInput(_TextInputBase):
    """
    The `TextAreaInput` allows entering any multiline string using a text input
    box.

    Lines are joined with the newline character `\n`.

    Reference: https://panel.holoviz.org/reference/widgets/TextAreaInput.html
    :Example:

    >>> TextAreaInput(
    ...     name='Description', placeholder='Enter your description here...'
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

    This widget is interchangeable with the `Toggle` widget.

    :Example:

    >>> Checkbox(name='Works with the tools you know and love', value=True)
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

    This widget is interchangeable with the `Toggle` widget.

    :Example:

    >>> Switch(name='Works with the tools you know and love', value=True)
    """

    color = param.Selector(objects=["default"] + COLORS, default="primary")

    edge = param.Selector(objects=["start", "end", False], default=False)

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(default=False)

    width = param.Boolean(default=None)

    _esm = "Switch.jsx"


class FileInput(MaterialWidget, _PnFileInput):
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
