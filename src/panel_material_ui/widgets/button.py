from __future__ import annotations

import typing as t
from collections.abc import Awaitable, Callable

import param
from panel.widgets.button import _ButtonBase as _PnButtonBase
from panel.widgets.button import _ClickButton

from ..base import COLOR_ALIASES, COLORS, STYLE_ALIASES, ColorType, LoadingTransform, ThemedTransform, TooltipTransform
from .base import MaterialWidget


class _ButtonLike(MaterialWidget):
    """
    Abstract base class for Material UI button-like widgets.
    """

    button_style: t.Literal["contained", "outlined", "text"] | None = param.Selector(objects=["contained", "outlined", "text"], default=None, precedence=-1, doc="""
        The variant of the component (alias for variant to match Panel's Button API).""")  # type: ignore[assignment]

    button_type: ColorType | None = param.Selector(
        objects=COLORS, default=None, precedence=-1, doc="""
        The type of the component (alias for color to match Panel's Button API)."""
    )  # type: ignore[assignment]

    color: ColorType = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the component.""")  # type: ignore[assignment]

    description = param.String(default=None, doc="""
        The description in the tooltip.""")  # type: ignore[assignment]

    description_delay = param.Integer(default=500, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 500ms.""")

    _esm_transforms = [TooltipTransform, ThemedTransform]
    _rename = {"button_style": None, "button_type": None, "color": "color", "variant": "variant"}
    _source_transforms = {"button_style": None, "button_type": None, "attached": None}

    __abstract = True

    @param.depends("button_type", watch=True, on_init=True)
    def _update_color(self):
        if self.button_type:
            self.color = self.button_type

    def _process_param_change(self, params):
        icon_size = params.pop("icon_size", None)
        params = super()._process_param_change(params)
        if icon_size is not None:
            params["icon_size"] = icon_size
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
    """
    Abstract base class for Material UI button widgets.
    """

    clicks = param.Integer(default=0, bounds=(0, None), doc="Number of clicks.")

    disable_elevation = param.Boolean(default=False, doc="Removes the button's box-shadow for a flat appearance.")

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

    size: t.Literal["small", "medium", "large"] = param.Selector(
        default="medium", objects=["small", "medium", "large"], doc="The size of the button."
    )  # type: ignore[assignment]

    variant: t.Literal["contained", "outlined", "text"] = param.Selector(objects=["contained", "outlined", "text"], default="contained", doc="""
        The variant of the component.""")  # type: ignore[assignment]

    width = param.Integer(default=None, doc="Width of the button in pixels.")

    _rename: t.ClassVar[dict[str, str | None]] = {
        "color": "color", "label": "label", "variant": "variant"
    }

    __abstract = True

    @param.depends("variant", watch=True, on_init=True)
    def _update_variant(self):
        if self.button_style:
            self.variant = self.button_style

    def _process_param_change(self, params):
        variant = params.pop("variant", None)
        props = super()._process_param_change(params)
        if variant is not None:
            props['variant'] = variant
        return props


class Button(_ButtonBase, _ClickButton):
    """
    The `Button` widget allows triggering events when the button is clicked.

    The Button provides a `value` parameter, which will toggle from
    `False` to `True` while the click event is being processed.

    It also provides an additional `clicks` parameter, that can be
    watched to subscribe to click events.

    :References:
    - https://panel-material-ui.holoviz.org/reference/widgets/Button.html
    - https://panel.holoviz.org/reference/widgets/Button.html
    - https://mui.com/material-ui/react-button/

    :Example:
    >>> Button(label='Click me', icon='caret-right', button_type='primary')
    """

    href = param.String(default=None, doc="""
        The URL to navigate to when the button is clicked.""")

    target: t.Literal["_blank", "_parent", "_self", "_top"] = param.Selector(default="_self", objects=["_blank", "_parent", "_self", "_top"],
                            doc="Where to open the linked document.")  # type: ignore[assignment]

    value = param.Event(doc="Toggles from False to True while the event is being processed.")

    _esm_base = "Button.jsx"
    _event = "dom_event"

    def __init__(self, **params):
        click_handler = params.pop("on_click", None)
        js_click_code = params.pop("js_on_click", None)

        super().__init__(**params)
        if click_handler:
            self.on_click(click_handler)
        if js_click_code:
            self.js_on_click(code=js_click_code)

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
    The `Fab` is a floating action button that allows triggering events when the button is clicked.

    :References:
    - https://panel-material-ui.holoviz.org/reference/widgets/Fab.html
    - https://mui.com/material-ui/react-floating-action-button/

    :Example:
    >>> Fab(icon='add')
    """

    button_style: t.Literal["circular", "extended"] | None = param.Selector(objects=["circular", "extended"], default=None, precedence=-1, doc="""
        The variant of the component (alias for variant to match Panel's Button API).""")  # type: ignore[assignment]

    icon = param.String(default="add", allow_None=True, doc="""
        The icon to display on the button.""")

    icon_size = param.String(default="1.5em", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""")

    size: t.Literal["small", "medium", "large"] = param.Selector(objects=["small", "medium", "large"], default="medium", doc="""
        The size of the button.""")  # type: ignore[assignment]

    variant: t.Literal["circular", "extended"] = param.Selector(objects=["circular", "extended"], default="circular", doc="""
        The variant of the button.""")  # type: ignore[assignment]

    _esm_base = "Fab.jsx"


class Toggle(_ButtonBase):
    """
    The `Toggle` widget allows toggling a single condition between True/False states.

    :References:
    - https://panel-material-ui.holoviz.org/reference/widgets/Toggle.html
    - https://panel.holoviz.org/reference/widgets/Toggle.html
    - https://mui.com/material-ui/react-toggle-button/

    :Example:
    >>> Toggle(label='Enable feature')
    """

    icon_size = param.String(default="1.8em", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""")

    value = param.Boolean(default=False)

    _esm_base = "ToggleButton.jsx"
    _esm_transforms = [LoadingTransform, TooltipTransform, ThemedTransform]


class Chip(_ButtonLike, _ClickButton):
    """
    A `Chip` can be used to display information, labels, tags, or actions.
    It can include text, an icon, or a delete button.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Chip.html
    - https://mui.com/material-ui/react-chip/

    :Example:
    >>> Chip(label="Log Time", icon="clock")
    """

    clicks = param.Integer(default=0, bounds=(0, None), doc="Number of clicks.")

    disabled = param.Boolean(
        default=False,
        doc="Disables the Chip component, making it opaque and disabling click events."
    )

    width = param.Integer(default=None, bounds=(0, None), allow_None=True, doc="Width of the widget.")

    icon = param.String(
        default=None,
        doc="""
        Name of the icon to display in the chip. Should be a valid Material UI icon name
        (e.g., 'favorite', 'delete', 'add'). The icon appears before the chip label.""",
    )

    size: t.Literal["small", "medium"] = param.Selector(
        objects=["small", "medium"],
        default="medium",
        doc="""
        Size of the chip component. Options:
        - 'small': Compact size for dense layouts
        - 'medium': Standard size (default)"""
    )  # type: ignore[assignment]

    variant: t.Literal["filled", "outlined"] = param.Selector(
        objects=["filled", "outlined"],
        default="filled",
        doc="""
        Visual style variant of the chip. Options:
        - 'filled': Solid background color (default)
        - 'outlined': Transparent background with colored border"""
    )  # type: ignore[assignment]

    object = param.Parameter(precedence=-1)

    _esm_base = "Chip.jsx"
    _event = "dom_event"
    _rename: t.ClassVar[dict[str, str | None]] = {
        "color": "color", "label": "label", "variant": "variant", "object": None
    }

    def __init__(self, label=None, **params):
        if 'object' in params:
            import warnings
            warnings.warn(
                "Chip's 'object' parameter is deprecated, use 'label' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            params['label'] = params.pop('object')
        if label is not None:
            params['object'] = params['label'] = label
        click_handler = params.pop("on_click", None)
        js_click_code = params.pop("js_on_click", None)
        super().__init__(**params)
        if click_handler:
            self.on_click(click_handler)
        if js_click_code:
            self.js_on_click(code=js_click_code)

    def on_click(self, callback: Callable[[param.parameterized.Event], None | Awaitable[None]]) -> param.parameterized.Watcher:
        """
        Register a callback to be executed when the Chip is clicked.

        Arguments
        ---------
        callback:
            The function to run on click events. Must accept a positional `Event` argument.

        Returns
        -------
        watcher: param.Parameterized.Watcher
          A `Watcher` that executes the callback when the Chip is clicked.
        """
        return self.param.watch(callback, "clicks", onlychanged=False)

    def _handle_click(self, event):
        self.param.update(clicks=self.clicks + 1)


__all__ = [
    "Button",
    "Chip",
    "Fab",
    "Toggle"
]
