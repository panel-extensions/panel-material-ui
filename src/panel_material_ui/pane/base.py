from __future__ import annotations

from typing import Any

import param
from panel.pane.markup import Markdown

from ..base import COLORS, MaterialComponent


class MaterialPaneBase(MaterialComponent):

    object = param.Parameter()

    _rerender_params = []

    __abstract = True

    def __init__(self, object=None, **params):
        super().__init__(object=object, **params)


class Avatar(MaterialPaneBase):
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


class Chip(MaterialPaneBase):
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

    def _handle_click(self, event):
        pass


class Skeleton(MaterialPaneBase):
    """
    The `Skeleton` component is used as a placeholder while content is loading.
    It provides a visual indication that data is being fetched, improving perceived performance
    and user experience.

    :References:

    - https://mui.com/material-ui/react-skeleton/
    """

    variant = param.Selector(
        objects=["circular", "rectangular", "rounded"],
        default="rounded",
        doc="""
        Shape variant of the skeleton placeholder. Options:
        - 'circular': Circular shape, ideal for avatar placeholders
        - 'rectangular': Sharp rectangular corners
        - 'rounded': Rectangular with rounded corners (default)"""
    )

    height = param.Integer(
        default=0,
        doc="""
        Height of the skeleton component in pixels. If 0 or not specified,
        the skeleton will adapt to its content or container."""
    )

    width = param.Integer(
        default=0,
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
