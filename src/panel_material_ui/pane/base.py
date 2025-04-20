from __future__ import annotations

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

    Reference: https://mui.com/material-ui/react-avatar/

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

    Reference: https://mui.com/material-ui/react-chip/

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

    Reference: https://mui.com/material-ui/react-skeleton/
    """

    variant = param.Selector(objects=["circular", "rectangular", "rounded"], default="rounded")

    height = param.Integer(default=0)

    width = param.Integer(default=0)

    _esm_base = "Skeleton.jsx"


class Typography(MaterialPaneBase, Markdown):
    """
    The `Typography` component is used to display text with different styles and weights.

    Reference: https://mui.com/material-ui/react-typography/
    """

    variant = param.String(default=None, doc="The typography variant, e.g. h1, h2, body1.")

    _esm_base = "Typography.jsx"
    _rename = {"object": "object"}

class Timeline(MaterialPaneBase):
    """Material‑UI **Timeline** component for Panel.

    References:

    - https://mui.com/material-ui/react-timeline/

    Example:

    >>> config = [
    ...     {"content_title": "Eat", "content": "Because you need strength", "opposite": "08:30", "color": "grey",   "variant": "filled", "icon": "fastfood"},
    ...     {"content_title": "Code", "content": "Because it's awesome!", "opposite": "09:00", "color": "primary", "variant": "filled", "icon": "laptop_mac"},
    ...     {"content_title": "Sleep", "content": "Because you need rest", "opposite": "09:30", "color": "secondary",   "variant": "outlined", "icon": "hotel"},
    ...     {"content_title": "Repeat", "content": "Because this is the life you love!", "opposite": "11:00", "color": "success",      "variant": "filled", "icon": "repeat"},
    ... ]
    >>> Timeline(object=config, width=600)
    """  # noqa: E501
    object = param.List(default=[], doc="""
      A list of dictionaries, each mapping directly onto a `TimelineItem` row.
      Supported keys:

      | key            | type            | default   | description                                      |
      |----------------|-----------------|-----------|--------------------------------------------------|
      | **content_title** | str          | *None*    | Header shown in `TimelineContent`.               |
      | **content**    | str             | *None*    | Body shown in `TimelineContent`.                 |
      | **opposite_title** | str         | *None*    | Header for `TimelineOppositeContent`             |
      | **opposite**   | str             | *None*    | Body for `TimelineOppositeContent`               |
      | **color**      | str             | primary   | Color prop for `TimelineDot`.                    |
      | **variant**    | str             | filled    | Variant prop for `TimelineDot` (filled/outlined).|
      | **icon**       | str             | *None     | Name of icon for `Icon` inside `TimelineDot`.    |
    """)

    position = param.Selector(default="right", objects=[
      'alternate-reverse',
      'alternate',
      'left',
      'right',
    ], doc="""The position of the content/ opposite content.""")

    _esm_base = "Timeline.jsx"
