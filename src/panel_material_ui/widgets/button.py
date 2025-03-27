from __future__ import annotations

from typing import (
    Awaitable,
    Callable,
    ClassVar,
    Mapping,
)

import param
from panel.widgets.button import _ButtonBase as _PnButtonBase
from panel.widgets.button import _ClickButton

from ..base import COLOR_ALIASES, COLORS, ThemedTransform
from .base import MaterialWidget, TooltipTransform


class _ButtonBase(MaterialWidget, _PnButtonBase):

    button_style = param.Selector(objects=["contained", "outlined", "text"], default="contained")

    button_type = param.Selector(objects=COLORS, default="default")

    clicks = param.Integer(default=0, bounds=(0, None), doc="Number of clicks.")

    description = param.String(default=None, doc="""
        The description in the tooltip.""")

    description_delay = param.Integer(default=1000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 1000ms.""")

    icon = param.String(
        default=None,
        doc="""
        An icon to render to the left of the button label. Either an SVG or an
        icon name which is loaded from Material Icons.""",
    )

    width = param.Integer(default=None)

    _esm_transforms = [TooltipTransform, ThemedTransform]
    _rename: ClassVar[Mapping[str, str | None]] = {
        "label": "label",
        "button_style": "button_style",
        "button_type": "button_type"
    }

    __abstract = True

    def _process_param_change(self, params):
        button_style = params.pop("button_style", None)
        if "button_type" in params:
            button_type = params["button_type"]
            params["button_type"] = COLOR_ALIASES.get(button_type, button_type)
        params = MaterialWidget._process_param_change(self, params)
        if button_style:
            params["button_style"] = button_style
        return params


class Button(_ButtonBase, _ClickButton):
    """
    The `Button` widget allows triggering events when the button is
    clicked.

    The Button provides a `value` parameter, which will toggle from
    `False` to `True` while the click event is being processed

    It also provides an additional `clicks` parameter, that can be
    watched to subscribe to click events.

    References:
    - https://panel.holoviz.org/reference/widgets/Button.html
    - https://mui.com/material-ui/react-button/

    :Example:

    >>> Button(name='Click me', icon='caret-right', button_type='primary')
    """

    icon_size = param.String(
        default="1em",
        doc="""
        Size of the icon as a string, e.g. 12px or 1em.""",
    )

    value = param.Event(doc="Toggles from False to True while the event is being processed.")

    _esm_base = "Button.jsx"
    _event = "dom_event"

    def __init__(self, **params):
        click_handler = params.pop("on_click", None)
        super().__init__(**params)
        if click_handler:
            self.on_click(click_handler)

    def on_click(self, callback: Callable[[param.parameterized.Event], None | Awaitable[None]]) -> param.parameterized.Watcher:
        """
        Register a callback to be executed when the `Button` is clicked.

        The callback is given an `Event` argument declaring the number of clicks

        Example
        -------

        >>> button = pn.widgets.Button(name='Click me')
        >>> def handle_click(event):
        ...    print("I was clicked!")
        >>> button.on_click(handle_click)

        Arguments
        ---------
        callback:
            The function to run on click events. Must accept a positional `Event` argument. Can
            be a sync or async function

        Returns
        -------
        watcher: param.Parameterized.Watcher
          A `Watcher` that executes the callback when the button is clicked.
        """
        return self.param.watch(callback, "clicks", onlychanged=False)

    def _handle_click(self, event):
        self.param.update(clicks=self.clicks + 1, value=True)


class Toggle(_ButtonBase):
    """The `Toggle` widget allows toggling a single condition between `True`/`False` states.

    This widget is interchangeable with the `Checkbox` widget.

    References:
    - https://panel.holoviz.org/reference/widgets/Toggle.html
    - https://mui.com/material-ui/react-toggle-button/

    :Example:

    >>> Toggle(name='Toggle', button_type='success')
    """

    button_style = param.Selector(objects=["contained", "outlined", "text"], default="contained", doc="""
        The button style, either 'solid' or 'outline'. As of today (March 27th, 2025) the
        `button_style` property does not work (see https://github.com/mui/material-ui/issues/34238).""")

    icon_size = param.String(default="1em", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""")

    value = param.Boolean(default=False)

    _esm_base = "ToggleButton.jsx"

__all__ = [
    "Button",
    "Toggle"
]
