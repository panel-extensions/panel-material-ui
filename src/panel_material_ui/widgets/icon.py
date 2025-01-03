from __future__ import annotations

import param

from ..base import COLORS
from .base import MaterialWidget


class ToggleIcon(MaterialWidget):
    """
    The `ToggleIcon` widget allows toggling a single condition between True/False states. This
    widget is interchangeable with the `Checkbox` and `Switch` widget.

    This widget incorporates a `value` attribute, which alternates between `False` and `True`.

    Some missing and extra features (if any) when comparing with the corresponding
    panel ToggleIcon widget [panel.widgets.ToggleIcon](https://panel.holoviz.org/reference/widgets/ToggleIcon.html):
    - Missing features: description_delay
    - Extra features: color, label, on_event, on_msg, theme

    :Example:

    >>> ToggleIcon(
    ...     icon="thumb-up", active_icon="thumb-down", size="small", description="Like"
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
