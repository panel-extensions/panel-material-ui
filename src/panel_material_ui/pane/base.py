from __future__ import annotations

from collections.abc import Callable
from typing import Any

import param
from panel.links import Callback
from panel.pane import HoloViews, Markdown
from panel.viewable import Child

from ..base import COLORS, MaterialComponent, ThemedTransform, TooltipTransform
from ..widgets import DatetimeInput, DiscreteSlider, EditableFloatSlider, EditableIntSlider, FloatSlider, IntSlider, Select

HoloViews.default_widgets = dict(
    HoloViews.default_widgets,
    date=DatetimeInput,
    discrete=Select,
    discrete_numeric=DiscreteSlider,
    float=(FloatSlider, EditableFloatSlider),
    int=(IntSlider, EditableIntSlider)
)

class MaterialPaneBase(MaterialComponent):

    object = param.Parameter(doc="The object to be rendered by the pane.")

    _rerender_params = []

    __abstract = True

    def __init__(self, object=None, **params):
        super().__init__(object=object, **params)


class ClickablePaneBase(MaterialPaneBase):

    clicks = param.Integer(default=0, doc="""
        The number of times the object has been clicked.""")

    _event = "dom_event"

    __abstract = True

    def __init__(self, object=None, **params):
        click_handler = params.pop("on_click", None)
        js_click_code = params.pop("js_on_click", None)

        super().__init__(object=object, **params)
        if click_handler:
            self.on_click(click_handler)
        if js_click_code:
            self.js_on_click(code=js_click_code)

    def _handle_click(self, event):
        self.param.update(clicks=self.clicks + 1)

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


class Badge(MaterialComponent):
    """
    The `Badge` generates a small badge to the top-right (by default)
    of its child element. Badges are commonly used to display
    notification counts, status indicators, or short labels overlaid
    on icons, avatars, or buttons.

    :References:

    - https://panel-material-ui.holoviz.org/reference/panes/Badge.html
    - https://mui.com/material-ui/react-badge/

    :Example:

    >>> Badge(IconButton(icon="mail"), badge_content=4, color="primary")
    """

    anchor_origin = param.Dict(default=None, doc="""
        The anchor position of the badge. Accepts a dictionary with
        keys 'vertical' ('top' or 'bottom') and 'horizontal'
        ('left' or 'right').""")

    badge_content = param.Parameter(default=0, doc="""
        The content rendered within the badge. Typically an integer
        count but can be a short string.""")

    color = param.Selector(default="primary", objects=COLORS, doc="""
        The color of the badge.""")

    max = param.Integer(default=99, bounds=(0, None), doc="""
        Maximum count to display. Values above this show as
        'max+' (e.g. '99+').""")

    object = Child(doc="""
        The child component to wrap with the badge.""")

    offset = param.NumericTuple(default=(0, -4), length=2, doc="""
        The (x, y) pixel offset of the badge from its anchor point on
        the object. Positive x shifts the badge right, positive y down.""")

    overlap = param.Selector(default="rectangular", objects=["rectangular", "circular"], doc="""
        Wrapped shape the badge should overlap.""")

    show_zero = param.Boolean(default=False, doc="""
        Whether to display the badge when badge_content is zero.""")

    variant = param.Selector(default="standard", objects=["dot", "standard"], doc="""
        The variant of the badge. Use 'dot' for a small dot
        indicator without content.""")

    _esm_base = "Badge.jsx"

    def __init__(self, object=None, **params):
        if object is not None:
            params["object"] = object
        # When the user doesn't set the Badge's own margin it inherits the
        # child's margin, so wrapping in a Badge is transparent to layout (the
        # child's margin is zeroed in the frontend so the badge still hugs the
        # child's edge). An explicit Badge margin always wins.
        margin_explicit = "margin" in params
        super().__init__(**params)
        self._margin_explicit = margin_explicit
        self._child_margin_watcher = None
        self._sync_child_margin()
        self.param.watch(self._sync_child_margin, "object")

    def _sync_child_margin(self, *_):
        if self._child_margin_watcher is not None:
            # On an object swap self.object already points at the new child, so
            # unwatch via the stored reference rather than self.object.
            watcher, previous = self._child_margin_watcher
            previous.param.unwatch(watcher)
            self._child_margin_watcher = None
        if self._margin_explicit:
            return
        obj = self.object
        if not isinstance(obj, param.Parameterized) or "margin" not in obj.param:
            return
        self.margin = obj.margin
        watcher = obj.param.watch(lambda *_: setattr(self, "margin", obj.margin), "margin")
        self._child_margin_watcher = (watcher, obj)


class Avatar(ClickablePaneBase):
    """
    The `Avatar` component displays profile pictures, user initials, or icons
    in a compact, circular or square format. Avatars are commonly used throughout
    user interfaces to represent users, brands, or entities in a visually
    consistent manner.

    The component supports multiple content types including images, text initials,
    and icons, with automatic fallback handling when images fail to load.

    :References:

    - https://panel-material-ui.holoviz.org/reference/panes/Avatar.html
    - https://mui.com/material-ui/react-avatar/

    :Example:

    >>> # Image avatar
    >>> Avatar("https://example.com/profile.jpg", alt_text="User Profile")

    >>> # Text avatar with custom styling
    >>> Avatar("JD", color="#2196f3", variant="square")

    >>> # Small avatar for compact layouts
    >>> Avatar("AB", size="small", variant="rounded")
    """

    alt_text = param.String(
        default=None,
        doc="""
        Alternative text to add to the image tag. The alt text is shown when a
        user cannot load or display the image and is used for accessibility.""",
    )

    color = param.Color(
        doc="""
        Background color for text and icon avatars. Accepts any valid CSS color value
        (e.g., '#ff0000', 'red', 'rgb(255,0,0)'). Only applies to text/icon avatars,
        not image avatars."""
    )

    object = param.String(
        default="",
        doc="""
        The content to display in the avatar. Can be an image URL/path for image avatars,
        or text content (like initials) for text avatars."""
    )

    size = param.Selector(
        objects=["small", "medium", "large"],
        default="medium",
        doc="""
        Size of the avatar component. Options:
        - 'small': 24x24 pixels
        - 'medium': 40x40 pixels
        - 'large': 56x56 pixels"""
    )

    variant = param.Selector(
        objects=["rounded", "square"],
        default="rounded",
        doc="""
        Shape variant of the avatar. Options:
        - 'rounded': Circular shape with rounded corners (default)
        - 'square': Square shape with sharp corners"""
    )

    _esm_base = "Avatar.jsx"


class Chip(ClickablePaneBase, TooltipTransform):
    """
    A `Chip` can be used to display information, labels, tags, or actions. It can include text,
    an avatar, an icon, or a delete button.

    :References:

    - https://mui.com/material-ui/react-chip/

    :Example:
    >>> Chip("Log Time", icon="clock")
    """

    color = param.Selector(
        objects=COLORS,
        default="primary",
        doc="""
        Color theme of the chip. Available options include standard Material UI colors
        like 'primary', 'secondary', 'default', 'error', 'info', 'success', 'warning'."""
    )

    description = param.String(default="", doc="Tooltip text to display when hovering over the widget.")

    description_delay = param.Integer(default=500, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 500ms.""")

    disabled = param.Boolean(
        default=False,
        doc="Disables the Chip component, making it opaque and disabling click events."
    )

    icon = param.String(
        default=None,
        doc="""
        Name of the icon to display in the chip. Should be a valid Material UI icon name
        (e.g., 'favorite', 'delete', 'add'). The icon appears before the chip label.""",
    )

    object = param.String(
        default="",
        doc="""
        The text content/label to display in the chip."""
    )

    size = param.Selector(
        objects=["small", "medium"],
        default="medium",
        doc="""
        Size of the chip component. Options:
        - 'small': Compact size for dense layouts
        - 'medium': Standard size (default)"""
    )

    variant = param.Selector(
        objects=["filled", "outlined"],
        default="filled",
        doc="""
        Visual style variant of the chip. Options:
        - 'filled': Solid background color (default)
        - 'outlined': Transparent background with colored border"""
    )

    _esm_base = "Chip.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]



class Skeleton(MaterialPaneBase):
    """
    The `Skeleton` component is used as a placeholder while content is loading.
    It provides a visual indication that data is being fetched, improving perceived performance
    and user experience.

    :References:

    - https://mui.com/material-ui/react-skeleton/
    """

    animation = param.Selector(
        default="pulse",
        objects=["pulse", "wave", None],
        doc="The animation. If None the animation effect is disabled."
    )

    color = param.String(doc="Color defined as a Mui color or valid CSS color.")

    variant = param.Selector(
        objects=["text", "circular", "rectangular", "rounded"],
        default="text",
        doc="""
        Shape variant of the skeleton placeholder. Options:
        - 'circular': Circular shape, ideal for avatar placeholders
        - 'rectangular': Sharp rectangular corners
        - 'rounded': Rectangular with rounded corners (default)"""
    )

    height = param.Integer(
        default=0,
        bounds=(0, None),
        doc="""
        Height of the skeleton component in pixels. If 0 or not specified,
        the skeleton will adapt to its content or container."""
    )

    width = param.Integer(
        default=0,
        bounds=(0, None),
        doc="""
        Width of the skeleton component in pixels. If 0 or not specified,
        the skeleton will adapt to its content or container."""
    )

    _esm_base = "Skeleton.jsx"


class Typography(MaterialPaneBase, Markdown):
    """
    The `Typography` component is used to display text with different styles and weights.

    :References:

    - https://mui.com/material-ui/react-typography/
    """

    color = param.String(
        default=None,
        doc="""
        Color of the text. Can be a Material UI theme color (e.g., 'primary', 'secondary',
        'error', 'warning', 'info', 'success') or any valid CSS color value."""
    )

    variant = param.String(
        default=None,
        doc="""
        Typography variant that defines the text styling. Common options include:
        - Headers: 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        - Body text: 'body1', 'body2'
        - Other: 'subtitle1', 'subtitle2', 'caption', 'overline'"""
    )

    _esm_base = "Typography.jsx"
    _rename = {"object": "object"}

    @classmethod
    def applies(cls, obj: Any) -> float | bool | None:
        if hasattr(obj, '_repr_markdown_'):
            return 0.29
        elif isinstance(obj, str):
            return 0.09
        else:
            return False
