from __future__ import annotations

import typing as t

import param
from panel.viewable import Child

from ..base import COLORS, ColorType, MaterialComponent


class Wrapper(MaterialComponent):
    """
    Base class for wrapper components that decorate a single child
    element with additional visual or behavioral embellishments.
    """

    object = Child(doc="""
        The child component to wrap.""")

    __abstract = True

    def __init__(self, object=None, **params):
        if object is not None:
            params["object"] = object
        super().__init__(**params)


class Transition(Wrapper):
    """
    The `Transition` wraps a child component with a transition effect
    that plays when the child enters or exits. Supports multiple
    animation variants including fade, grow, slide, zoom, and collapse.

    :References:

    - https://panel-material-ui.holoviz.org/reference/wrappers/Transition.html
    - https://mui.com/material-ui/transitions/

    :Example:

    >>> Transition(Button(label="Hello"), variant="fade", active=True)
    """

    active = param.Boolean(default=True, doc="""
        Whether the child is shown (with transition). Set to False
        to animate the child out, True to animate it in.""")

    duration = param.Integer(default=None, bounds=(0, None), doc="""
        The duration of the transition in milliseconds. When None,
        the duration is automatically calculated based on the
        element's size.""")

    orientation: t.Literal['vertical', 'horizontal'] = param.Selector(
        default="vertical", objects=["vertical", "horizontal"], doc="""
        The orientation of the collapse transition. Only applies
        when variant is 'collapse'.""")  # type: ignore[assignment]

    placement: t.Literal['down', 'left', 'right', 'up'] = param.Selector(
        default="left",
        objects=["down", "left", "right", "up"],
        doc="""
        The direction the child slides in from. Only applies
        when variant is 'slide'.""")  # type: ignore[assignment]

    variant: t.Literal['collapse', 'fade', 'grow', 'slide', 'zoom'] = param.Selector(
        default="fade",
        objects=["collapse", "fade", "grow", "slide", "zoom"],
        doc="""
        The type of transition animation to apply.""")  # type: ignore[assignment]

    _esm_base = "Transition.jsx"


class Badge(Wrapper):
    """
    The `Badge` generates a small badge to the top-right (by default)
    of its child element. Badges are commonly used to display
    notification counts, status indicators, or short labels overlaid
    on icons, avatars, or buttons.

    :References:

    - https://panel-material-ui.holoviz.org/reference/wrappers/Badge.html
    - https://mui.com/material-ui/react-badge/

    :Example:

    >>> Badge(IconButton(icon="mail"), content=4, color="primary")
    """

    content = param.Parameter(default=0, doc="""
        The content rendered within the badge. Typically an integer
        count but can be a short string.""")

    color: ColorType = param.Selector(default="primary", objects=COLORS, doc="""
        The color of the badge.""")  # type: ignore[assignment]

    max = param.Integer(default=99, bounds=(0, None), doc="""
        Maximum count to display. Values above this show as
        'max+' (e.g. '99+').""")

    offset = param.XYCoordinates(default=None, doc="""
        The (x, y) pixel offset of the badge from its anchor point on
        the object. Positive x shifts the badge right, positive y down.""")

    overlap: t.Literal['rectangular', 'circular'] = param.Selector(default="rectangular", objects=["rectangular", "circular"], doc="""
        Wrapped shape the badge should overlap.""")  # type: ignore[assignment]

    placement: t.Literal['top-right', 'top-left', 'bottom-right', 'bottom-left'] = param.Selector(
        default="top-right",
        objects=["top-right", "top-left", "bottom-right", "bottom-left"],
        doc="""
        The placement of the badge relative to the child element.""")  # type: ignore[assignment]

    show_zero = param.Boolean(default=False, doc="""
        Whether to display the badge when content is zero.""")

    variant: t.Literal['dot', 'standard'] = param.Selector(default="standard", objects=["dot", "standard"], doc="""
        The variant of the badge. Use 'dot' for a small dot
        indicator without content.""")  # type: ignore[assignment]

    _esm_base = "Badge.jsx"

    def __init__(self, object=None, **params):
        if object is not None:
            params["object"] = object
        margin_explicit = "margin" in params
        super().__init__(**params)
        self._margin_explicit = margin_explicit
        self._child_margin_watcher = None
        self._sync_child_margin()
        self.param.watch(self._sync_child_margin, "object")

    def _sync_child_margin(self, *_):
        if self._child_margin_watcher is not None:
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


class Skeleton(Wrapper):
    """
    The `Skeleton` wraps a child component and displays an animated
    placeholder in its place while loading. When `active` is True the
    skeleton is shown; when False the child is rendered normally.

    :References:

    - https://panel-material-ui.holoviz.org/reference/wrappers/Skeleton.html
    - https://mui.com/material-ui/react-skeleton/

    :Example:

    >>> Skeleton(Card(...), active=True, variant="rounded")
    """

    active = param.Boolean(default=False, doc="""
        Whether to show the child content. When False the skeleton
        placeholder is rendered; when True the child is displayed
        normally.""")

    animation: t.Literal['pulse', 'wave'] | None = param.Selector(
        default="pulse", objects=["pulse", "wave", None], doc="""
        The animation effect for the skeleton. Use None to disable.""")  # type: ignore[assignment]

    variant: t.Literal['text', 'circular', 'rectangular', 'rounded'] = param.Selector(
        default="rounded",
        objects=["text", "circular", "rectangular", "rounded"],
        doc="""
        Shape variant of the skeleton placeholder.""")  # type: ignore[assignment]

    _esm_base = "Skeleton.jsx"


class Tooltip(Wrapper):
    """
    The `Tooltip` displays informative text when users hover over, focus
    on, or tap a child element. It wraps a single child component and
    shows a configurable tooltip label.

    :References:

    - https://panel-material-ui.holoviz.org/reference/wrappers/Tooltip.html
    - https://mui.com/material-ui/react-tooltip/

    :Example:

    >>> Tooltip(Button(label="Delete"), title="Remove this item")
    """

    arrow = param.Boolean(default=False, doc="""
        Whether the tooltip has an arrow indicating the element it
        refers to.""")

    describe_child = param.Boolean(default=False, doc="""
        Whether the tooltip acts as an accessible description rather
        than a label. Use when the child already has a visible label
        and the tooltip provides supplementary information.""")

    enter_delay = param.Integer(default=100, bounds=(0, None), doc="""
        The number of milliseconds to wait before showing the tooltip.
        This can help avoid tooltips appearing on quick mouse passes.""")

    follow_cursor = param.Boolean(default=False, doc="""
        Whether the tooltip follows the cursor position.""")

    leave_delay = param.Integer(default=0, bounds=(0, None), doc="""
        The number of milliseconds to wait before hiding the tooltip.""")

    open = param.Boolean(default=None, allow_None=True, doc="""
        Explicitly control whether the tooltip is open. When None,
        the tooltip is managed automatically on hover/focus. Set to
        True or False for programmatic control.""")

    placement: t.Literal[
        'bottom-end', 'bottom-start', 'bottom', 'left-end', 'left-start',
        'left', 'right-end', 'right-start', 'right', 'top-end', 'top-start', 'top'
    ] = param.Selector(
        default="right",
        objects=[
            "bottom-end", "bottom-start", "bottom",
            "left-end", "left-start", "left",
            "right-end", "right-start", "right",
            "top-end", "top-start", "top",
        ],
        doc="""
        The placement of the tooltip relative to the child element.""")  # type: ignore[assignment]

    title = param.String(default="", doc="""
        The text to display inside the tooltip.""")

    _esm_base = "Tooltip.jsx"
