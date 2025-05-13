from __future__ import annotations

from collections.abc import Callable
from typing import Any

import param
from panel.links import Callback

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

    size = param.String(default="medium", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""",)

    value = param.Boolean(
        default=False,
        doc="""
        Whether the icon is toggled on or off.""",
    )

    _esm_transforms = [TooltipTransform, ThemedTransform]

    __abstract = True


class ToggleIcon(_ClickableIcon):
    """
    The `ToggleIcon` widget allows toggling a single condition between True/False states. This
    widget is interchangeable with the `Checkbox` and `Switch` widget.

    This widget incorporates a `value` attribute, which alternates between `False` and `True`.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/ToggleIcon.html
    - https://panel.holoviz.org/reference/widgets/ToggleIcon.html
    - https://mui.com/material-ui/react-checkbox/#icon

    :Example:

    >>> ToggleIcon(
    ...     icon="thumb-up", active_icon="thumb-down", size="small", description="Like"
    ... )
    """

    color = param.Selector(objects=COLORS, default="default")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    width = param.Boolean(default=None)

    _esm_base = "ToggleIcon.jsx"


class IconButton(_ClickableIcon, _ButtonBase):
    """
    The `IconButton` widget facilitates event triggering upon button clicks.

    This widget displays a default `icon` initially. Upon being clicked, an `active_icon` appears
    for a specified `toggle_duration`.

    For instance, the `IconButton` can be effectively utilized to implement a feature akin to
    ChatGPT's copy-to-clipboard button.

    The button incorporates a `value` attribute, which alternates between `False` and `True` as the
    click event is processed.

    Furthermore, it includes an `clicks` attribute, enabling subscription to click events for
    further actions or monitoring.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/IconButton.html
    - https://panel.holoviz.org/reference/widgets/ButtonIcon.html
    - https://mui.com/material-ui/api/icon-button/

    :Example:

    >>> button_icon = IconButton(
    ...     icon='favorite',
    ...     active_icon='check',
    ...     description='Copy',
    ...     toggle_duration=2000
    ... )
    """

    clicks = param.Integer(default=0, doc="""
        The number of times the button has been clicked.""")

    edge = param.Selector(objects=["start", "end", False], default=False, doc="""
        Whether the icon should be on the start or end of the button.""")

    toggle_duration = param.Integer(default=75, doc="""
        The number of milliseconds the active_icon should be shown for
        and how long the button should be disabled for.""")

    value = param.Event(doc="Toggles from False to True while the event is being processed.")

    _esm_base = "IconButton.jsx"
    _event = "dom_event"

    def __init__(self, **params):
        click_handler = params.pop('on_click', None)
        super().__init__(**params)
        if click_handler:
            self.on_click(click_handler)

    def _handle_click(self, event):
        self.param.update(clicks=self.clicks + 1, value=True)

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

    def js_on_click(self, args: dict[str, Any] | None = None, code: str = "") -> Callback:
        """
        Allows defining a JS callback to be triggered when the button
        is clicked.

        Parameters
        -----------
        args: dict
          A mapping of objects to make available to the JS callback
        code: str
          The Javascript code to execute when the button is clicked.

        Returns
        -------
        callback: Callback
          The Callback which can be used to disable the callback.
        """
        if args is None:
            args = {}
        return Callback(self, code={'event:'+self._event: code}, args=args)

    def jscallback(self, args: dict[str, Any] | None = None, **callbacks: str) -> Callback:
        """
        Allows defining a Javascript (JS) callback to be triggered when a property
        changes on the source object. The keyword arguments define the
        properties that trigger a callback and the JS code that gets
        executed.

        Parameters
        -----------
        args: dict
          A mapping of objects to make available to the JS callback
        **callbacks: dict
          A mapping between properties on the source model and the code
          to execute when that property changes

        Returns
        -------
        callback: Callback
          The Callback which can be used to disable the callback.
        """
        if args is None:
            args = {}
        for k, v in list(callbacks.items()):
            if k == 'clicks':
                k = 'event:'+self._event
            val = self._rename.get(v, v)
            if val is not None:
                callbacks[k] = val
        return Callback(self, code=callbacks, args=args)


ButtonIcon = IconButton

__all__ = [
    "ButtonIcon",
    "IconButton",
    "ToggleIcon"
]
