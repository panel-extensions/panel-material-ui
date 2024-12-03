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

from ..base import COLORS
from .base import MaterialWidget


class _ButtonBase(MaterialWidget, _PnButtonBase):
    button_type = param.Selector(objects=COLORS, default="primary")

    clicks = param.Integer(default=0, bounds=(0, None), doc="Number of clicks.")

    icon = param.String(
        default=None,
        doc="""
        An icon to render to the left of the button label. Either an SVG or an
        icon name which is loaded from Material Icons.""",
    )

    width = param.Integer(default=None)

    _stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons"]

    __abstract = True

    def _process_param_change(self, params):
        icon = params.pop("icon", None)
        label = params.pop("label", None)
        props = MaterialWidget._process_param_change(self, params)
        props.pop("tooltip", None)
        props.pop("tooltip_delay", None)
        if icon:
            props["icon"] = icon
        if label:
            props["label"] = label
        return props


class Button(_ButtonBase, _ClickButton):
    """
    The `Button` widget allows triggering events when the button is
    clicked.

    The Button provides a `value` parameter, which will toggle from
    `False` to `True` while the click event is being processed

    It also provides an additional `clicks` parameter, that can be
    watched to subscribe to click events.

    Some missing and extra features (if any) when comparing with the corresponding
    panel Button widget [panel.widgets.Button](https://panel.holoviz.org/reference/widgets/Button.html):
    - Missing features: description_delay
    - Extra features: label, on_event, on_msg, tooltip (work in progress), theme

    :Example:

    >>> Button(name='Click me', icon='caret-right', button_type='primary')
    """

    button_style = param.Selector(objects=["contained", "outlined", "text"], default="contained")

    icon_size = param.String(
        default="1em",
        doc="""
        Size of the icon as a string, e.g. 12px or 1em.""",
    )

    tooltip = param.Parameter(precedence=-1)

    value = param.Event(doc="Toggles from False to True while the event is being processed.")

    _esm = "Button.jsx"

    _rename: ClassVar[Mapping[str, str | None]] = {"label": "label", "button_style": "button_style"}

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

    Some missing and extra features (if any) when comparing with the corresponding
    panel Toggle widget [panel.widgets.Toggle](https://panel.holoviz.org/reference/widgets/Toggle.html):
    - No missing features
    - Extra features: clicks, description, label, on_event, on_msg, theme


    :Example:

    >>> Toggle(name='Toggle', button_type='success')
    """

    icon_size = param.String(
        default="1em",
        doc="""
        Size of the icon as a string, e.g. 12px or 1em.""",
    )

    value = param.Boolean(default=False)

    _esm = "ToggleButton.jsx"


class ButtonIcon(_ButtonBase):
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

    Some missing and extra features (if any) when comparing with the corresponding
    panel ButtonIcon widget [panel.widgets.ButtonIcon](https://panel.holoviz.org/reference/widgets/ButtonIcon.html):
    - Missing features: description_delay, js_on_click, on_click
    - Extra features: button_style, button_type, edge, label, on_event, on_msg, theme

    :Example:

    >>> button_icon = ButtonIcon(
    ...     icon='favorite',
    ...     active_icon='check',
    ...     description='Copy',
    ...     toggle_duration=2000
    ... )
    """

    active_icon = param.String(
        default="",
        doc="""
        The name of the icon to display when toggled from
        [tabler-icons.io](https://tabler-icons.io)/ or an SVG.""",
    )

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

    _esm = "IconButton.jsx"
