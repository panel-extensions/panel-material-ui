from __future__ import annotations

from typing import Callable

import param
from panel.models.reactive_html import DOMEvent

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


class Breadcrumbs(MaterialComponent):
    """
    The `Breadcrumbs` component is used to show the navigation path of a user within an application.
    It improves usability by allowing users to track their location and navigate back easily.

    Reference: https://mui.com/material-ui/react-breadcrumbs/
    """

    color = param.Selector(objects=COLORS, default="primary")

    items = param.List(default=[], doc=(
        "List of breadcrumb items. Each item may be a string or an object with keys: "
        "'label' (required) and 'href' (optional)."
    ))

    separator = param.String(default=None, doc="The separator displayed between breadcrumb items.")

    _esm_base = "Breadcrumbs.jsx"


class List(MaterialComponent):
    """
    The `List` component is used to display a structured group of items, such as menus,
    navigation links, or settings.

    Reference: https://mui.com/material-ui/react-list/
    """

    active = param.Integer(default=None, doc="""
        Last clicked list item.""")

    items = param.List(default=[], doc=(
        "List of items to display. Each item may be a string or an object with properties: "
        "'label' (required), 'icon' (optional), 'avatar' (optional), and 'secondary' (optional)."
    ))

    _esm_base = "List.jsx"

    def __init__(self, **params):
        click_handler = params.pop('on_click', None)
        super().__init__(**params)
        self._on_click_callbacks = []
        if click_handler:
            self.on_click(click_handler)

    def _handle_click(self, event):
        self.active = event.index
        for fn in self._on_click_callbacks:
            try:
                fn(event)
            except Exception as e:
                print(f'List on_click handler errored: {e}')  # noqa

    def on_click(self, callback: Callable[[DOMEvent], None]):
        """
        Register a callback to be executed when a list item
        is clicked.

        Parameters
        ----------
        callback: (callable)
            The callback to run on click events.
        """
        self._on_click_callbacks.append(callback)

    def remove_on_click(self, callback: Callable[[DOMEvent], None]):
        """
        Remove a previously added click handler.

        Parameters
        ----------
        callback: (callable)
            The callback to run on edit events.
        """
        self._on_click_callbacks.remove(callback)
