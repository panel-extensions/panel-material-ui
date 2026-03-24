from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    ClassVar,
    Iterable,
)

import param
from bokeh.models import Spacer as BkSpacer
from panel._param import Margin
from panel.io.resources import CDN_DIST
from panel.layout.base import (
    _SCROLL_MAPPING,
    ListLike,
    NamedListLike,
    SizingModeMixin,
)
from panel.pane import panel
from panel.util import edit_readonly, isIn, param_name
from panel.viewable import Child, Children, Viewable

from ..base import COLORS, MaterialComponent
from ..widgets import ToggleIcon

if TYPE_CHECKING:
    from bokeh.document import Document
    from bokeh.model import Model
    from bokeh.models.ui.ui_element import UIElement
    from pyviz_comms import Comm


class MaterialLayout(MaterialComponent, SizingModeMixin):

    margin = Margin(default=0, doc="The margin of the layout.")

    __abstract = True

    _source_transforms = {"objects": None}

    def __init__(self, *objects, **params):
        if objects:
            params["objects"] = objects
        super().__init__(**params)

    def _get_model(
        self, doc: Document, root: Model | None = None,
        parent: Model | None = None, comm: Comm | None = None
    ) -> Model:
        model = super()._get_model(doc, root, parent, comm)
        props = dict(model.properties_with_values())
        props["sizing_mode"] = self.sizing_mode
        sizing_mode = self._compute_sizing_mode(model.data.objects, props)
        model.update(**sizing_mode)
        return model


class MaterialListLike(MaterialLayout, ListLike):

    scroll = param.Selector(
        default=False,
        objects=[False, True, "both-auto", "y-auto", "x-auto", "both", "x", "y"],
        doc="""Whether to add scrollbars if the content overflows the size
        of the container. If "both-auto", will only add scrollbars if
        the content overflows in either directions. If "x-auto" or "y-auto",
        will only add scrollbars if the content overflows in the
        respective direction. If "both", will always add scrollbars.
        If "x" or "y", will always add scrollbars in the respective
        direction. If False, overflowing content will be clipped.
        If True, will only add scrollbars in the direction of the container,
        (e.g. Column: vertical, Row: horizontal).""")

    _stylesheets: ClassVar[list[str]] = [f'{CDN_DIST}css/listpanel.css']

    __abstract = True

    def _process_param_change(self, params: dict[str, Any]) -> dict[str, Any]:
        if (scroll := params.get('scroll')):
            css_classes = params.get('css_classes', self.css_classes)
            if scroll in _SCROLL_MAPPING:
                scroll_class = _SCROLL_MAPPING[scroll]
            elif self._direction:
                scroll_class = f'scrollable-{self._direction}'
            else:
                scroll_class = 'scrollable'
            params['css_classes'] = css_classes + [scroll_class]
        return super()._process_param_change(params)


class MaterialNamedListLike(MaterialLayout, NamedListLike):

    _names = param.List(default=[])

    _headers = Children()

    __abstract = True

    def __init__(self, *items: list[Any | tuple[str, Any]], **params: Any):
        if 'objects' in params:
            if items:
                raise ValueError(
                    f'{type(self).__name__} objects should be supplied either '
                    'as positional arguments or as a keyword, not both.'
                )
            items = params.pop('objects')
        MaterialLayout.__init__(self, objects=[i[1] if isinstance(i, tuple) else i for i in items], **params)
        params['objects'], headers, names = self._to_objects_and_names(items)
        self._names = names
        self._headers = headers
        self._panels: defaultdict[str, dict[int, Viewable]] = defaultdict(dict)
        self.param.watch(self._update_names, 'objects')
        # ALERT: Ensure that name update happens first, should be
        #        replaced by watch precedence support in param
        self.param.watchers['objects']['value'].reverse()

    @param.depends("objects", watch=True)
    def _trigger_names(self):
        self.param.trigger("_names", "_headers")

    def _to_object_and_name(self, item):
        if isinstance(item, tuple):
            name, item = item
        else:
            name = getattr(item, 'name', None)
        if isinstance(name, Viewable):
            header = name
            name = None
            pane = panel(item)
        else:
            header = None
            pane = item if isinstance(item, Viewable) else panel(item, name=name)
            name = param_name(pane.name) if name is None else name
        return pane, header, name

    def _to_objects_and_names(self, items):
        if items:
            objs, headers, names = (list(i) for i in zip(*(self._to_object_and_name(item) for item in items), strict=False))
        else:
            objs, headers, names = [], [], []
        if self._param__private.initialized:
            return objs, headers, names
        return objs, names

    def __setitem__(self, index, panes):
        new_objects = list(self)
        if isinstance(index, slice):
            new_objects[index], self._headers[index], self._names[index] = self._to_objects_and_names(panes)
        else:
            new_objects[index], self._headers[index], self._names[index] = self._to_object_and_name(panes)
        self.objects = new_objects

    def append(self, pane: Any) -> None:
        """
        Appends an object to the tabs.

        Parameters
        ----------
        obj (object): Panel component to add as a tab.
        """
        new_object, new_header, new_name = self._to_object_and_name(pane)
        new_objects = list(self)
        new_objects.append(new_object)
        self._names.append(new_name)
        self._headers.append(new_header)
        self.objects = new_objects

    def clear(self) -> None:
        """
        Clears the tabs.
        """
        self._names = []
        self._headers = []
        self.objects = []

    def extend(self, panes: Iterable[Any]) -> None:
        """
        Extends the the tabs with a list.

        Parameters
        ----------
        objects (list): List of panel components to add as tabs.
        """
        new_objects, new_headers, new_names = self._to_objects_and_names(panes)
        objects = list(self)
        objects.extend(new_objects)
        self._names.extend(new_names)
        self._headers.extend(new_headers)
        self.objects = objects

    def insert(self, index: int, pane: Any) -> None:
        """
        Inserts an object in the tabs at the specified index.

        Parameters
        ----------
        index (int): Index at which to insert the object.
        object (object): Panel components to insert as tabs.
        """
        new_object, new_header, new_name = self._to_object_and_name(pane)
        new_objects = list(self.objects)
        new_objects.insert(index, new_object)
        self._headers.insert(index, new_header)
        self._names.insert(index, new_name)
        self.objects = new_objects

    def pop(self, index: int = -1) -> Viewable:
        """
        Pops an item from the tabs by index.

        Parameters
        ----------
        index (int): The index of the item to pop from the tabs.
        """
        new_objects = list(self)
        obj = new_objects.pop(index)
        self._names.pop(index)
        self._headers.pop(index)
        self.objects = new_objects
        return obj

    def remove(self, pane: Viewable) -> None:
        """
        Removes an object from the tabs.

        Parameters
        ----------
        obj (object): The object to remove from the tabs.
        """
        new_objects = list(self)
        if pane in new_objects:
            index = new_objects.index(pane)
            new_objects.remove(pane)
            self._names.pop(index)
            self._headers.pop(index)
            self.objects = new_objects
        else:
            raise ValueError(f'{pane!r} is not in list')

    def reverse(self) -> None:
        """
        Reverses the tabs.
        """
        new_objects = list(self)
        new_objects.reverse()
        self._names.reverse()
        self._headers.reverse()
        self.objects = new_objects


class Column(MaterialListLike):
    """
    The `Column` layout arranges its contents vertically.
    """

    auto_scroll_limit = param.Integer(bounds=(0, None), doc="""
        Max pixel distance from the latest object in the Column to
        activate automatic scrolling upon update. Setting to 0
        disables auto-scrolling.""")

    scroll_button_threshold = param.Integer(bounds=(0, None), doc="""
        Min pixel distance from the latest object in the Column to
        display the scroll button. Setting to 0
        disables the scroll button.""")

    scroll_position = param.Integer(default=0, doc="""
        Current scroll position of the Column. Setting this value
        will update the scroll position of the Column. Setting to
        0 will scroll to the top.""")

    scroll_index = param.Integer(default=None, allow_None=True, doc="""
        Index of the object to scroll to. Setting this value will
        scroll the Column to the object at the given index.""")

    view_latest = param.Boolean(default=False, doc="""
        Whether to scroll to the latest object on init. If not
        enabled the view will be on the first object.""")

    scroll_button_click = param.Event(doc="""
        Triggered when the scroll-to-latest button is clicked.""")

    _event = "dom_event"
    _rename = {"scroll_button_click": None}

    _esm_base = "Box.jsx"
    _constants = {"direction": "column", "loading_inset": 0}

    def __init__(self, *objects, **params):
        click_handler = params.pop("on_click", None)
        super().__init__(*objects, **params)
        if click_handler:
            self.on_click(click_handler)

    def _handle_click(self, event=None):
        self.param.trigger("scroll_button_click")

    def on_click(self, callback: Callable[[param.parameterized.Event], None | Awaitable[None]]) -> param.parameterized.Watcher:
        """
        Register a callback invoked when the scroll-to-latest button is clicked.
        """
        return self.param.watch(callback, "scroll_button_click", onlychanged=False)

    def scroll_to(self, index: int):
        """
        Scrolls to the child at the provided index.

        Parameters
        ----------
        index: int
            Index of the child object to scroll to.
        """
        self._send_msg({"type": "scroll_to", "index": index})


class Feed(Column):
    """
    The `Feed` layout is a buffered `Column` optimized for long, dynamic lists.
    """

    load_buffer = param.Integer(default=10, bounds=(0, None), doc="""
        The number of objects loaded on each side of the visible objects.
        When scrolled halfway into the buffer, the feed will automatically
        load additional objects while unloading objects on the opposite side.""")

    scroll = param.Selector(
        default="y",
        objects=[False, True, "both-auto", "y-auto", "x-auto", "both", "x", "y"],
        doc="""Whether to add scrollbars if the content overflows the size
        of the container. If "both-auto", will only add scrollbars if
        the content overflows in either directions. If "x-auto" or "y-auto",
        will only add scrollbars if the content overflows in the
        respective direction. If "both", will always add scrollbars.
        If "x" or "y", will always add scrollbars in the respective
        direction. If False, overflowing content will be clipped.
        If True, will only add scrollbars in the direction of the container,
        (e.g. Column: vertical, Row: horizontal).""")

    visible_children = param.List(default=[], item_type=str, doc="""
        Internal list of currently visible frontend child model ids.""")

    visible_range = param.Range(readonly=True, doc="""
        Read-only upper and lower bounds of the currently visible feed objects.
        This range is automatically updated based on scrolling.""")

    _esm_base = "Feed.jsx"
    _rename: ClassVar[Mapping[str, str | None]] = {
        **Column._rename, "load_buffer": None, "visible_range": None,
    }

    def __init__(self, *objects, **params):
        for height_param in ("height", "min_height", "max_height"):
            if height_param in params:
                break
        else:
            # Set a default height to ensure a bounded scroll viewport.
            params["height"] = 300

        super().__init__(*objects, **params)
        self._last_synced: tuple[int, int] | None = None
        self.param.watch(self._trigger_view_latest, "objects")

    @param.depends("visible_range", "load_buffer", watch=True)
    def _trigger_get_objects(self):
        if self.visible_range is None or self._last_synced is None:
            return

        # visible start, end / synced start, end
        vs, ve = self.visible_range
        ss, se = self._last_synced
        half_buffer = self.load_buffer // 2

        top_trigger = (vs - ss) < half_buffer
        bottom_trigger = (se - ve) < half_buffer
        invalid_trigger = (
            # Prevent being trapped with too few rendered children.
            ve - vs < self.load_buffer and
            ve - vs < len(self.objects)
        )
        if top_trigger or bottom_trigger or invalid_trigger:
            self.param.trigger("objects")

    def _trigger_view_latest(self, event):
        if (
            event.type == "triggered" or not self.view_latest or
            not event.new or event.new[-1] in event.old
        ):
            return
        self.scroll_to_latest()

    @property
    def _synced_range(self) -> tuple[int, int]:
        n = len(self.objects)
        if self.visible_range:
            return (
                max(self.visible_range[0] - self.load_buffer, 0),
                min(self.visible_range[-1] + self.load_buffer, n),
            )
        if self.view_latest:
            return (max(n - self.load_buffer * 2, 0), n)
        return (0, min(self.load_buffer, n))

    def _process_property_change(self, msg):
        if "visible_children" in msg:
            visible = msg["visible_children"]
            for model, _ in self._models.values():
                refs = [c.ref["id"] for c in getattr(model.data, "objects", [])]
                if visible and visible[0] in refs:
                    indexes = sorted(refs.index(v) for v in visible if v in refs)
                    break
            else:
                return super()._process_property_change(msg)

            offset = self._last_synced[0] if self._last_synced is not None else self._synced_range[0]
            n = len(self.objects)
            visible_range = [
                max(offset + indexes[0], 0),
                min(offset + indexes[-1] + 1, n),
            ]
            if visible_range[0] >= visible_range[1]:
                visible_range[0] = max(visible_range[1] - self.load_buffer, 0)
            with edit_readonly(self):
                self.visible_range = tuple(visible_range)
        return super()._process_property_change(msg)

    def _process_param_change(self, msg):
        msg.pop("visible_range", None)
        return super()._process_param_change(msg)

    def _get_child_model(
        self, child: Viewable, doc: Document, root: Model, parent: Model,
        comm: Comm | None
    ) -> tuple[list[UIElement] | UIElement | None, list[UIElement]]:
        if child is not self.objects:
            return super()._get_child_model(child, doc, root, parent, comm)

        # If no previously visible objects are visible now, reset the visible range.
        events = self._in_process__events.get(doc, {})
        if (
            self._last_synced and
            "visible_range" not in events and
            not any(isIn(obj, self.objects) for obj in child[slice(*self._last_synced)])
        ):
            with edit_readonly(self):
                self.visible_range = None

        from panel.pane.base import RerenderError
        new_models, old_models = [], []
        self._last_synced = self._synced_range

        current_objects = list(self.objects)
        ref = root.ref["id"]
        for i in range(*self._last_synced):
            pane = current_objects[i]
            if ref in pane._models:
                child, _ = pane._models[root.ref["id"]]
                old_models.append(child)
            else:
                try:
                    child = pane._get_model(doc, root, parent, comm)
                except RerenderError as e:
                    if e.layout is not None and e.layout is not self:
                        raise e
                    e.layout = None
                    return self._get_child_model(current_objects[:i], doc, root, parent, comm)
            new_models.append(child)
        return new_models, old_models

    def _process_event(self, event=None) -> None:
        """
        Process a scroll-button click event by forcing range to latest window.
        """
        if not self.visible_range:
            return

        # Need to get all the way to the bottom rather than the center
        # of the buffer zone.
        load_buffer = self.load_buffer
        with param.discard_events(self):
            self.load_buffer = 1

        n = len(self.objects)
        n_visible = self.visible_range[-1] - self.visible_range[0]
        with edit_readonly(self):
            # plus one to center on the last object
            self.visible_range = (min(max(n - n_visible + 1, 0), n), n)

        with param.discard_events(self):
            self.load_buffer = load_buffer

    def _handle_click(self, event=None):
        self._process_event()
        super()._handle_click(event)

    def _handle_msg(self, msg: dict[str, Any]) -> None:
        if msg.get("type") == "request_latest":
            self.scroll_to_latest(scroll_limit=msg.get("scroll_limit"))

    def scroll_to_latest(self, scroll_limit: float | None = None) -> None:
        """
        Scrolls the Feed to the latest entry.
        """
        rerender = bool(self._last_synced and self._last_synced[-1] < len(self.objects))
        if rerender:
            self._process_event()
        self._send_msg({"type": "scroll_latest", "rerender": rerender, "scroll_limit": scroll_limit})


class Row(MaterialListLike):
    """
    The `Row` layout arranges its contents horizontally.
    """

    _esm_base = "Box.jsx"
    _constants = {"direction": "row", "loading_inset": 0}


class FlexBox(MaterialListLike):
    """
    The `FlexBox` layout arranges its contents in a flex container.
    """

    align_content = param.Selector(default='flex-start', objects=[
        'normal', 'flex-start', 'flex-end', 'center', 'space-between',
        'space-around', 'space-evenly', 'stretch', 'start', 'end',
        'baseline', 'first baseline', 'last baseline'], doc="""
        Defines how a flex container's lines align when there is extra
        space in the cross-axis.""")

    align_items = param.Selector(default='flex-start', objects=[
        'stretch', 'flex-start', 'flex-end', 'center', 'baseline',
        'first baseline', 'last baseline', 'start', 'end',
        'self-start', 'self-end'], doc="""
        Defines the default behavior for how flex items are laid
        out along the cross axis on the current line.""")

    flex_direction = param.Selector(default='row', objects=[
        'row', 'row-reverse', 'column', 'column-reverse'], doc="""
        This establishes the main-axis, thus defining the direction
        flex items are placed in the flex container.""")

    flex_wrap = param.Selector(default='wrap', objects=[
        'nowrap', 'wrap', 'wrap-reverse'], doc="""
        Whether and how to wrap items in the flex container.""")

    gap = param.String(default='', doc="""
        Defines the spacing between flex items, supporting various units (px, em, rem, %, vw/vh).""")

    justify_content = param.Selector(default='flex-start', objects=[
        'flex-start', 'flex-end', 'center', 'space-between', 'space-around',
        'space-evenly', 'start', 'end', 'left', 'right'], doc="""
        Defines the alignment along the main axis.""")

    _esm_base = "Box.jsx"
    _constants = {"direction": "flex"}


class PaperMixin(param.Parameterized):
    """
    Baseclass adding Paper parameters to a layout.
    """

    elevation = param.Integer(default=1, bounds=(0, None), doc="Elevation of the paper surface.")

    raised = param.Boolean(default=True, doc="Whether the layout is raised visually.")

    square = param.Boolean(default=False, doc="Whether to disable rounded corners.")

    variant = param.Selector(objects=["elevation", "outlined"], default="elevation", doc="Variant style of the paper surface.")

    _abstract = True


class Paper(MaterialListLike, PaperMixin):
    """
    Paper implements a container for displaying content on an elevated surface.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Paper.html
    - https://mui.com/material-ui/react-paper/

    :Example:
    >>> Paper(name="Paper", objects=[1, 2, 3], elevation=10, width=200, height=200)
    """

    direction = param.Selector(objects=["row", "column", "column-reverse", "row-reverse"], default="column", doc="Direction of content arrangement in the paper.")

    _esm_base = "Paper.jsx"


class Container(MaterialListLike):
    """
    The `Container` layout centers your content horizontally. It's the most basic layout element.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Container.html
    - https://mui.com/material-ui/react-container/

    :Example:

    >>> Container(some_widget, some_pane, some_python_object, title='Container')
    """

    disable_gutters = param.Boolean(default=False, doc="""
        If `True`, the container will not have gutters.""")

    fixed = param.Boolean(default=False, doc="""
        Set the max-width to match the min-width of the current breakpoint.
        This is useful if you'd prefer to design for a fixed set of sizes
        instead of trying to accommodate a fully fluid viewport.""")

    sizing_mode = param.Selector(default='stretch_width')

    width_option = param.Selector(objects=["xs", "sm", "md", "lg", "xl", False], default="lg", doc="Width option for the container.")

    _esm_base = "Container.jsx"


class Grid(MaterialListLike):
    """
    The `Grid` layout is a two-dimensional layout that allows arranging items in a grid.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Grid.html
    - https://mui.com/material-ui/react-grid/

    :Example:

    >>> Grid(some_widget, some_pane, some_python_object, title='Grid')
    """

    container = param.Boolean(default=False, doc="""
        Whether the grid should be a container.""")

    columns = param.ClassSelector(default=12, class_=(int, dict), doc="""
        The number of columns to display in the grid.""")

    column_spacing = param.Number(default=None, doc="""
        The spacing between the columns in the grid. Overrides the `spacing` parameter.""")

    direction = param.Selector(objects=["row", "column", "column-reverse", "row-reverse"], default="row", doc="Direction of grid arrangement.")

    row_spacing = param.Number(default=None, doc="""
        The spacing between the rows in the grid. Overrides the `spacing` parameter.""")

    size = param.ClassSelector(default=None, class_=(int, str, dict), doc="""
        The size of the grid. Overrides the `columns` parameter.""")

    spacing = param.Number(default=0, doc="""
        The spacing between the columns and rows in the grid.""")

    _esm_base = "Grid.jsx"


class Card(MaterialNamedListLike, PaperMixin):
    """
    A `Card` layout allows arranging multiple panel objects in a
    collapsible, vertical container with a header bar.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Card.html
    - https://panel.holoviz.org/reference/layouts/Card.html
    - https://mui.com/material-ui/react-card/

    :Example:

    >>> Card(some_widget, some_pane, some_python_object, title='Card')
    """

    collapsed = param.Boolean(default=False, doc="""
        Whether the contents of the Card are collapsed.""")

    collapsible = param.Boolean(default=True, doc="""
        Whether the Card should be expandable and collapsible.""")

    header = Child(doc="""
        A Panel component to display in the header bar of the Card.
        Will override the given title if defined.""")

    header_background = param.Color(doc="""
        The background color of the Card header.""")

    header_color = param.Color(doc="""
        The text color of the Card header.""")

    header_css_classes = param.List(doc="""
        List of CSS classes to apply to CardHeader component.""")

    hide_header = param.Boolean(default=False, doc="Whether to hide the card header.")

    outlined = param.Boolean(default=True, doc="Whether the card is outlined.")

    title = param.String(doc="""
        A title to be displayed in the Card header, will be overridden
        by the header if defined.""")

    title_css_classes = param.List(doc="""
        List of CSS classes to apply to CardTitle component.""")

    title_variant = param.String(default="h3", doc="""
        The text variant of the Card header title.""")

    _direction = "vertical"
    _esm_base = "Card.jsx"

    _rename = {"objects": "objects", "title": "title", "header": "header"}

    def select(self, selector: type | Callable[[Viewable], bool] | None = None) -> list[Viewable]:
        return ([] if self.header is None else self.header.select(selector)) + super().select(selector)


class Details(MaterialNamedListLike, PaperMixin):
    """
    A `Details` layout allows arranging multiple panel objects in a
    compact, collapsible container with three expansion states:
    collapsed, expanded (with scrollable area), and fully expanded.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Details.html

    :Example:

    >>> Details(some_widget, some_pane, some_python_object, title='Details')
    """

    collapsed = param.Boolean(default=True, doc="""
        Whether the contents of the Details are collapsed.""")

    fully_expanded = param.Boolean(default=False, doc="""
        Whether the Details are fully expanded (no scrollable area).
        Only applies when collapsed is False.""")

    header = Child(doc="""
        A Panel component to display in the header bar of the Details.
        Will override the given title if defined.""")

    header_background = param.Color(doc="""
        The background color of the Details header.""")

    header_color = param.Color(doc="""
        The text color of the Details header.""")

    header_css_classes = param.List(doc="""
        List of CSS classes to apply to DetailsHeader component.""")

    hide_header = param.Boolean(default=False, doc="Whether to hide the details header.")

    outlined = param.Boolean(default=True, doc="Whether the details is outlined.")

    scrollable_height = param.Integer(default=150, allow_None=True, doc="""
        Height of the scrollable area before it is fully expanded.""")

    title = param.String(doc="""
        A title to be displayed in the Details header, will be overridden
        by the header if defined.""")

    title_css_classes = param.List(doc="""
        List of CSS classes to apply to DetailsTitle component.""")

    _direction = "vertical"
    _esm_base = "Details.jsx"

    _rename = {"objects": "objects", "title": "title", "header": "header"}

    def select(self, selector: type | Callable[[Viewable], bool] | None = None) -> list[Viewable]:
        return ([] if self.header is None else self.header.select(selector)) + super().select(selector)


class Accordion(MaterialNamedListLike, PaperMixin):
    """
    The `Accordion` layout is a type of `Card` layout that allows switching
    between multiple objects by clicking on the corresponding card header.

    The labels for each card will default to the `name` parameter of the card's
    contents, but may also be defined explicitly as part of a tuple.

    `Accordion` has a list-like API that allows
    interactively updating and modifying the cards using the methods `append`,
    `extend`, `clear`, `insert`, `pop`, `remove` and `__setitem__`.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Accordion.html
    - https://panel.holoviz.org/reference/layouts/Accordion.html
    - https://mui.com/material-ui/react-accordion/

    :Example:

    >>> Accordion(("Card 1", "Card 1 objects"), ("Card 2", "Card 2 objects"))
    """

    active_header_color = param.Color(doc="""
        The text color of the active Card header.""")

    active_header_background = param.Color(doc="""
        The background color of the active Card header.""")

    active = param.List(default=[], doc="""
        List of indexes of active cards.""")

    disabled = param.List(default=[], doc="""
        List of indexes of disabled cards.""")

    disable_gutters = param.Boolean(default=False, doc="""
        Whether to disable margins between expanded sections.""")

    header_background = param.Color(doc="""
        The background color of the Card header.""")

    header_color = param.Color(doc="""
        The text color of the Card header.""")

    title_variant = param.String(default="h3", doc="""
        The text variant of the Accordion header titles.""")

    toggle = param.Boolean(default=False, doc="""
        Whether to toggle between active cards or allow multiple cards""")

    _esm_base = "Accordion.jsx"

    def __init__(self, *objects, **params):
        if "objects" not in params:
            params["objects"] = objects
        super().__init__(**params)


class Tabs(MaterialNamedListLike):
    """
    The `Tabs` layout allows switching between multiple objects by clicking
    on the corresponding tab header.

    Tab labels may be defined explicitly as part of a tuple or will be
    inferred from the `name` parameter of the tab's contents.

    Like `Accordion`, `Tabs` has a list-like API with methods to
    `append`, `extend`, `clear`, `insert`, `pop`, `remove` and `__setitem__`,
    which make it possible to interactively update and modify the tabs.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Tabs.html
    - https://panel.holoviz.org/reference/layouts/Tabs.html
    - https://mui.com/material-ui/react-tabs/

    :Example:

    >>> Tabs(("Tab 1", "Tab 1 objects"), ("Tab 2", "Card 2 objects"))

    """
    active = param.Integer(default=0, bounds=(0, None), doc="""
        Index of the currently displayed objects.""")

    closable = param.Boolean(default=False, doc="""
        Whether to display an icon to allow closing and thereby
        removing a tab.""")

    centered = param.Boolean(default=False, doc="""
        Whether the tabs should be centered.""")

    color = param.Selector(default="primary", objects=COLORS, doc="Color of the tabs component.")

    disabled = param.List(default=[], item_type=int, doc="""
        List of indexes of disabled tabs.""")

    dynamic = param.Boolean(default=False, doc="""
        Whether the tab contents should be rendered dynamically,
        i.e. only when the tab is active.""")

    tabs_location = param.ObjectSelector(
        default="above",
        objects=["above", "below", "left", "right"],
        doc="""
        The location of the tabs relative to the tab contents.""",
    )

    wrapped = param.Boolean(default=False, doc="""
        Whether the tab labels should be wrapped.""")

    _direction = "vertical"
    _esm_base = "Tabs.jsx"

    def __init__(self, *objects, **params):
        if "objects" not in params:
            params["objects"] = objects
        super().__init__(**params)

    @param.depends("active", watch=True)
    def _trigger_children(self):
        self.param.trigger("objects")

    def _get_child_model(self, child, doc, root, parent, comm):
        ref = root.ref["id"]
        models, old_models = [], []
        for i, sv in enumerate(child):
            if self.dynamic and i != self.active:
                model = BkSpacer()
            elif ref in sv._models:
                model = sv._models[ref][0]
                old_models.append(model)
            else:
                model = sv._get_model(doc, root, parent, comm)
            models.append(model)
        return models, old_models

    def _process_close(self, ref, attr, old, new):
        """
        Handle closed tabs.
        """
        model, _ = self._models.get(ref, (None, None))
        if model:
            try:
                inds = [old.index(tab) for tab in new]
            except Exception:
                return old, None
            old = self.objects
            new = [old[i] for i in inds]
        return old, new

    def _comm_change(self, doc, ref, comm, subpath, attr, old, new):
        if attr in self._changing.get(ref, []):
            self._changing[ref].remove(attr)
            return
        if attr == 'objects':
            old, new = self._process_close(ref, attr, old, new)
            if new is None:
                return
        super()._comm_change(doc, ref, comm, subpath, attr, old, new)

    def _server_change(self, doc, ref, subpath, attr, old, new):
        if attr in self._changing.get(ref, []):
            self._changing[ref].remove(attr)
            return
        if attr == 'objects':
            old, new = self._process_close(ref, attr, old, new)
            if new is None:
                return
        super()._server_change(doc, ref, subpath, attr, old, new)


class Divider(MaterialListLike):
    """
    A `Divider` draws a horizontal rule (a `<hr>` tag in HTML) to separate
    multiple components in a layout.

    :References:

    - https://panel.holoviz.org/reference/layouts/Divider.html
    - https://mui.com/material-ui/react-divider/

    :Example:

    >>> Divider(sizing_mode="stretch_width")
    """

    orientation = param.Selector(objects=["horizontal", "vertical"], default="horizontal", doc="Orientation of the divider.")

    variant = param.Selector(objects=["fullWidth", "inset", "middle"], default="fullWidth", doc="Variant style of the divider.")

    _esm_base = "Divider.jsx"


class Alert(MaterialListLike):
    """
    An `Alert` displays messages, such as warnings, errors, success messages,
    or informational updates. It provides a visually distinct way to inform users about
    the system's status.

    :References:

    - https://panel-material-ui.holoviz.org/reference/global/Notifications.html
    - https://mui.com/material-ui/react-alert/

    :Example:

    >>> Alert(title="This is an alert")
    """

    alert_type = param.Selector(objects=COLORS, default="primary", doc="""
        The type of the alert.""")

    closed = param.Boolean(default=False, doc="""
        Whether the alert is closed.""")

    closeable = param.Boolean(default=False, doc="""
        Whether the alert is closeable.""")

    severity = param.Selector(objects=["error", "warning", "info", "success"], default="success", doc="""
        The severity of the alert.""")

    object = param.String(default="", doc="""
        The object to display in the alert.""")

    title = param.String(default=None, doc="""
        The title of the alert.""")

    variant = param.Selector(default="outlined", objects=["filled", "outlined"], doc="""
        The variant of the alert.""")

    _esm_base = "Alert.jsx"


class Backdrop(MaterialListLike):
    """
    The `Backdrop` component can be used to create a semi-transparent overlay over the application's UI.
    It is often used to focus attention on a specific part of the interface,
    such as during loading states or while a modal dialog is open.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Backdrop.html
    - https://mui.com/material-ui/react-backdrop/

    :Example:
    >>> close = Button(on_click=lambda _: backdrop.param.update(open=False), label='Close')  # type: ignore
    >>> backdrop = Backdrop(LoadingIndicator(), close)
    >>> button = Button(on_click=lambda _: backdrop.param.update(open=True), label=f'Open {Backdrop.name}')
    >>> pn.Column(button, backdrop).servable()
    """

    open = param.Boolean(default=False, doc="""
        Whether the backdrop is open.""")

    _esm_base = "Backdrop.jsx"


class Dialog(MaterialListLike):
    """
    The `Dialog` can be used to display important content in a modal-like overlay that requires
    user interaction. It is often used for tasks such as confirmations, forms, or displaying
    additional information.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Dialog.html
    - https://mui.com/material-ui/react-dialog/

    :Example:
    >>> close = Button(on_click=lambda _: dialog.param.update(open=False), label='Close')  # type: ignore
    >>> dialog = Dialog("This is a modal", close)
    >>> button = Button(on_click=lambda _: dialog.param.update(open=True), label=f'Open {Dialog.name}')
    >>> pn.Column(button, dialog).servable()
    """

    close_on_click = param.Boolean(default=False, doc="""
        Close when clicking outside the Dialog area.""")

    full_screen = param.Boolean(default=False, doc="""
        Whether the dialog should be full screen.""")

    open = param.Boolean(default=False, doc="""
        Whether the dialog is open.""")

    title = param.String(default="", doc="""
        The title of the dialog.""")

    title_variant = param.String(default="h3", doc="""
        The text variant of the Dialog title.""")

    scroll = param.Selector(objects=["body", "paper"], default="paper", doc="""
        Whether the dialog should scroll the content or the paper.""")

    show_close_button = param.Boolean(default=False, doc="""
        Whether to show the close button.""")

    width_option = param.Selector(objects=["xs", "sm", "md", "lg", "xl", False], default="sm", doc="""
        The width of the dialog.""")

    _esm_base = "Dialog.jsx"


class Drawer(MaterialListLike):
    """
    The `Drawer` component can be used to display important content in a modal-like overlay that requires
    user interaction. It is often used for tasks such as confirmations, forms, or displaying
    additional information.

    :References:

    - https://panel-material-ui.holoviz.org/reference/layouts/Drawer.html
    - https://mui.com/material-ui/react-drawer/

    :Example:
    >>> drawer = Drawer("This is a drawer")
    >>> button = Button(on_click=lambda _: drawer.param.update(open=True), label='Open Drawer')
    >>> pn.Column(button, drawer).servable()
    """

    anchor = param.Selector(default="left", objects=["left", "right", "top", "bottom"], doc="Anchor position for the drawer.")

    size = param.Integer(default=250, doc="""
        The width (for left/right anchors) or height (for top/bottom anchors) of the drawer.""")

    open = param.Boolean(default=False, doc="""
        Whether the drawer is open.""")

    variant = param.Selector(default="temporary", objects=["permanent", "persistent", "temporary"], doc="Variant style of the drawer.")

    _esm_base = "Drawer.jsx"

    @param.depends("variant", watch=True, on_init=True)
    def _force_zero_dimensions(self):
        if self.variant == "temporary":
            self.param.update(width=0, height=0, sizing_mode="fixed")

    def create_toggle(
        self,
        icon: str = "menu",
        active_icon: str = "menu_open_icon",
        **params
    ):
        """
        Create a ToggleIcon for the drawer.

        Parameters
        ----------
        icon: str
            The icon to display when the drawer is closed.
        active_icon: str
            The icon to display when the drawer is open.

        Returns
        -------
        toggle: ToggleIcon
            A ToggleIcon component that can be used to toggle the drawer.
        """

        toggle = ToggleIcon(icon=icon, active_icon=active_icon, value=self.open, **params)
        toggle.jslink(self, value='open', bidirectional=True)
        return toggle


class Popup(MaterialListLike):
    """
    The `Popup` component displays content in an anchored overlay that
    requires user interaction. It is commonly used for contextual
    menus, confirmations, forms, or any UI element that should appear
    relative to another component or screen position.

    Reference: https://mui.com/material-ui/react-menu/
    """

    anchor_origin = param.Dict(default={"horizontal": "right", "vertical": "bottom" })

    anchor_position = param.XYCoordinates(default=None)

    close_on_click = param.Boolean(default=True, doc="""
        Close when clicking outside the Popup area.""")

    enforce_focus = param.Boolean(default=True, doc="""
        Whether to enforce focus on the Popup while it is open.""")

    hide_backdrop = param.Boolean(default=False, doc="""
        Whether to hide the backdrop when the Popup is open.""")

    elevation = param.Integer(default=1, bounds=(0, None), doc="Elevation of the paper surface.")

    open = param.Boolean(default=False, doc="Whether the pop-up is open.")

    transform_origin = param.Dict(default=None)

    _esm_base = "Popup.jsx"



__all__ = [
    "Accordion",
    "Alert",
    "Backdrop",
    "Card",
    "Column",
    "Container",
    "Details",
    "Dialog",
    "Divider",
    "Drawer",
    "Feed",
    "FlexBox",
    "Grid",
    "Paper",
    "Popup",
    "Row",
    "Tabs",
]
