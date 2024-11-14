from __future__ import annotations

import param

from ..base import COLORS
from .base import MaterialWidget


class ToggleIcon(MaterialWidget):
    """
    The `ToggleIcon` widget allows toggling a single condition between True/False states. This
    widget is interchangeable with the `Checkbox` and `Toggle` widget.

    This widget incorporates a `value` attribute, which alternates between `False` and `True`.

    :Example:

    >>> ToggleIcon(
    ...     icon="thumb-up", active_icon="thumb-down", size="4em", description="Like"
    ... )
    """

    active_icon = param.String(
        default="",
        doc="""
        The name of the icon to display when toggled from
        [tabler-icons.io](https://tabler-icons.io)/ or an SVG.""",
    )

    color = param.Selector(objects=COLORS, default="primary")

    icon = param.String(
        default="heart",
        doc="""
        The name of the icon to display from
        [tabler-icons.io](https://tabler-icons.io)/ or an SVG.""",
    )

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(
        default=False,
        doc="""
        Whether the icon is toggled on or off.""",
    )

    width = param.Boolean(default=None)

    _esm = "ToggleIcon.jsx"

    _stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons"]
