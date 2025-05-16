from __future__ import annotations

from typing import Any

import param
from panel.pane.markup import Markdown

from ..base import COLORS, MaterialComponent


class MaterialPaneBase(MaterialComponent):

    object = param.Parameter()

    __abstract = True

    def __init__(self, object=None, **params):
        super().__init__(object=object, **params)


class Avatar(MaterialPaneBase):
    """
    The `Avatar` component is used to display profile pictures, user initials, icons,
    or custom images.

    :References:

    - https://mui.com/material-ui/react-avatar/

    :Example:
    >>> Avatar("path/to/image.jpg")
    """

    alt_text = param.String(
        default=None,
        doc="""
        alt text to add to the image tag. The alt text is shown when a
        user cannot load or display the image.""",
    )

    color = param.Color()

    object = param.String(default="")

    size = param.Selector(objects=["small", "medium"], default="medium")

    variant = param.Selector(objects=["rounded", "square"], default="rounded")

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

    color = param.Selector(objects=COLORS, default="primary")

    icon = param.String(
        default=None,
        doc="""
        The name of the icon to display.""",
    )

    object = param.String(default="")

    size = param.Selector(objects=["small", "medium"], default="medium")

    variant = param.Selector(objects=["filled", "outlined"], default="filled")

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

    variant = param.Selector(objects=["circular", "rectangular", "rounded"], default="rounded")

    height = param.Integer(default=0)

    width = param.Integer(default=0)

    _esm_base = "Skeleton.jsx"


class Typography(MaterialPaneBase, Markdown):
    """
    The `Typography` component is used to display text with different styles and weights.

    :References:

    - https://mui.com/material-ui/react-typography/
    """

    variant = param.String(default=None, doc="The typography variant, e.g. h1, h2, body1.")

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
