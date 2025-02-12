from __future__ import annotations

from collections.abc import Callable

import param

from ..base import COLORS, ThemedTransform
from .base import MaterialWidget, TooltipTransform
from .button import _ButtonBase


class _ClickableIcon(MaterialWidget):

    active_icon = param.String(
        default="",
        doc="""
        The name of the icon to display when toggled from
        https://mui.com/material-ui/material-icons or an SVG.""",
    )

    icon = param.String(
        default="heart",
        doc="""
        The name of the icon to display from
        https://mui.com/material-ui/material-icons or an SVG.""",
    )

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    value = param.Boolean(
        default=False,
        doc="""
        Whether the icon is toggled on or off.""",
    )

    _esm_transforms = [TooltipTransform, ThemedTransform]

    __abstract = False


class ToggleIcon(_ClickableIcon):
    """
    The `ToggleIcon` widget allows toggling a single condition between True/False states. This
    widget is interchangeable with the `Checkbox` and `Switch` widget.

    This widget incorporates a `value` attribute, which alternates between `False` and `True`.

    :Example:

    >>> ToggleIcon(
    ...     icon="thumb-up", active_icon="thumb-down", size="small", description="Like"
    ... )
    """

    color = param.Selector(objects=COLORS, default="primary")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    width = param.Boolean(default=None)

    _esm_base = "ToggleIcon.jsx"


class ButtonIcon(_ClickableIcon, _ButtonBase):
    """
    The `ButtonIcon` widget facilitates event triggering upon button clicks.

    This widget displays a default `icon` initially. Upon being clicked, an `active_icon` appears
    for a specified `toggle_duration`.

    For instance, the `ButtonIcon` can be effectively utilized to implement a feature akin to
    ChatGPT's copy-to-clipboard button.

    The button incorporates a `value` attribute, which alternates between `False` and `True` as the
    click event is processed.

    Furthermore, it includes an `clicks` attribute, enabling subscription to click events for
    further actions or monitoring.

    :Example:

    >>> button_icon = ButtonIcon(
    ...     icon='favorite',
    ...     active_icon='check',
    ...     description='Copy',
    ...     toggle_duration=2000
    ... )
    """

    clicks = param.Integer(default=0, doc="""
        The number of times the button has been clicked.""")

    edge = param.Selector(objects=["start", "end", False], default=False)

    size = param.String(
        default="1em",
        doc="""
        Size of the icon as a string, e.g. 12px or 1em.""",
    )

    toggle_duration = param.Integer(
        default=75,
        doc="""
        The number of milliseconds the active_icon should be shown for
        and how long the button should be disabled for.""",
    )

    _esm_base = "IconButton.jsx"

    def __init__(self, **params):
        click_handler = params.pop('on_click', None)
        super().__init__(**params)
        if click_handler:
            self.on_click(click_handler)

    def on_click(
        self, callback: Callable[[param.parameterized.Event], None]
    ) -> param.parameterized.Watcher:
        """
        Register a callback to be executed when the button is clicked.

        The callback is given an `Event` argument declaring the number of clicks.

        Arguments
        ---------
        callback: (Callable[[param.parameterized.Event], None])
            The function to run on click events. Must accept a positional `Event` argument

        Returns
        -------
        watcher: param.Parameterized.Watcher
          A `Watcher` that executes the callback when the MenuButton is clicked.
        """
        return self.param.watch(callback, 'clicks', onlychanged=False)
