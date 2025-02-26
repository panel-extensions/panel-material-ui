from __future__ import annotations

import param

from ..base import COLORS, MaterialComponent


class Avatar(MaterialComponent):
    """
    The `Avatar` component is used to display profile pictures, user initials, icons,
    or custom images.

    Reference: https://mui.com/material-ui/react-avatar/

    :Example:
    >>> Avatar(object="path/to/image.jpg")
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


class Chip(MaterialComponent):
    """
    A `Chip` can be used to display information, labels, tags, or actions. It can include text,
    an avatar, an icon, or a delete button.

    Reference: https://mui.com/material-ui/react-chip/

    :Example:
    >>> Chip(object="Log Time", icon="clock")
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


class Skeleton(MaterialComponent):
    """
    The `Skeleton` component is used as a placeholder while content is loading.
    It provides a visual indication that data is being fetched, improving perceived performance
    and user experience.

    Reference: https://mui.com/material-ui/react-skeleton/
    """

    variant = param.Selector(objects=["circular", "rectangular", "rounded"], default="rounded")

    height = param.Integer(default=0)

    width = param.Integer(default=0)

    _esm_base = "Skeleton.jsx"
