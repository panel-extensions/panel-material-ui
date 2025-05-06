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

from ..base import COLOR_ALIASES, COLORS, STYLE_ALIASES, LoadingTransform, ThemedTransform
from .base import MaterialWidget, TooltipTransform


class _ButtonLike(MaterialWidget):

    button_style = param.Selector(objects=["contained", "outlined", "text"], default=None, doc="""
        The variant of the component (alias for variant to match Panel's Button API).""")

    button_type = param.Selector(objects=COLORS, default=None, doc="""
        The type of the component (alias for color to match Panel's Button API).""")

    color = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the component.""")

    description = param.String(default=None, doc="""
        The description in the tooltip.""")

    description_delay = param.Integer(default=5000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 500ms.""")

    variant = param.Selector(objects=["contained", "outlined", "text"], default="contained", doc="""
        The variant of the component.""")

    _esm_transforms = [TooltipTransform, ThemedTransform]
    _rename = {"button_style": None, "button_type": None}
    _source_transforms = {"button_style": None, "button_type": None}

    __abstract = True

    @param.depends("button_type", watch=True, on_init=True)
    def _update_color(self):
        if self.button_type:
            self.color = self.button_type

    @param.depends("variant", watch=True, on_init=True)
    def _update_variant(self):
        if self.button_style:
            self.variant = self.button_style

    def _process_param_change(self, params):
        params = super()._process_param_change(params)
        if "color" in params:
            color = params["color"]
            params["color"] = COLOR_ALIASES.get(color, color)
        if "variant" in params:
            variant = params["variant"]
            params["variant"] = STYLE_ALIASES.get(variant, variant)
        # Work around Panel button_style css_classes issue
        if "css_classes" in params:
            params["css_classes"] = [css_cls for css_cls in params["css_classes"] if css_cls is not None]
        return params


class _ButtonBase(_ButtonLike, _PnButtonBase):

    clicks = param.Integer(default=0, bounds=(0, None), doc="Number of clicks.")

    end_icon = param.String(default=None, doc="""
        An icon to render to the right of the button label. Either an SVG or an
        icon name which is loaded from Material Icons.""",
    )

    icon = param.String(default=None, doc="""
        An icon to render to the left of the button label. Either an SVG or an
        icon name which is loaded from Material Icons.""",
    )

    icon_size = param.String(default="1em", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""")

    width = param.Integer(default=None)

    _rename: ClassVar[Mapping[str, str | None]] = {
        "label": "label"
    }

    __abstract = True


class Button(_ButtonBase, _ClickButton):
    """
    The `Button` widget allows triggering events when the button is
    clicked.

    The Button provides a `value` parameter, which will toggle from
    `False` to `True` while the click event is being processed

    It also provides an additional `clicks` parameter, that can be
    watched to subscribe to click events.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Button.html
    - https://panel.holoviz.org/reference/widgets/Button.html
    - https://mui.com/material-ui/react-button/

    :Example:

    >>> Button(label='Click me', icon='caret-right', button_type='primary')
    """

    disable_elevation = param.Boolean(default=False)

    href = param.String(default=None, doc="""
        The URL to navigate to when the button is clicked.""")

    target = param.Selector(default="_self", objects=["_blank", "_parent", "_self", "_top"],
                            doc="Where to open the linked document.")

    size = param.Selector(default="medium", objects=["small", "medium", "large"])

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


class Fab(Button):
    """
    The `Fab` is a so called floating action button that allows triggering events when the button is
    clicked.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Fab.html
    - https://mui.com/material-ui/react-floating-action-button/

    :Example:

    >>> Fab(icon='add')
    """

    icon = param.String(default="add", doc="""
        The icon to display on the button.""")

    size = param.Selector(objects=["small", "medium", "large"], default="medium", doc="""
        The size of the button.""")

    variant = param.Selector(objects=["circular", "extended"], default="circular", doc="""
        The variant of the button.""")

    _esm_base = "Fab.jsx"
    _esm_transforms = [LoadingTransform, TooltipTransform, ThemedTransform]


class Toggle(_ButtonBase):
    """The `Toggle` widget allows toggling a single condition between `True`/`False` states.

    This widget is interchangeable with the `Checkbox` widget.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Toggle.html
    - https://panel.holoviz.org/reference/widgets/Toggle.html
    - https://mui.com/material-ui/react-toggle-button/

    :Example:

    >>> Toggle(label='Toggle', color='success')
    """

    icon_size = param.String(default="1em", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""")

    value = param.Boolean(default=False)

    _esm_base = "ToggleButton.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]


__all__ = [
    "Button",
    "Fab",
    "Toggle"
]
