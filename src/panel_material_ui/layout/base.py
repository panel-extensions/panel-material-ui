from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import param
from bokeh.models import Spacer as BkSpacer
from panel._param import Margin
from panel.layout.base import ListLike, NamedListLike, SizingModeMixin
from panel.viewable import Child

from ..base import COLORS, MaterialComponent
from ..widgets import ToggleIcon

if TYPE_CHECKING:
    from bokeh.document import Document
    from bokeh.model import Model
    from panel.viewable import Viewable
    from pyviz_comms import Comm


class MaterialLayout(MaterialComponent, SizingModeMixin):

    margin = Margin(default=0, doc="The margin of the layout.")

    __abstract = True

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

    __abstract = True


class MaterialNamedListLike(MaterialLayout, NamedListLike):

    _names = param.List(default=[])

    __abstract = True

    @param.depends("objects", watch=True)
    def _trigger_names(self):
        self.param.trigger("_names")


class Column(MaterialListLike):
    """
    The `Column` layout arranges its contents vertically.
    """

    _esm_base = "Box.jsx"
    _constants = {"direction": "column"}


class Row(MaterialListLike):
    """
    The `Row` layout arranges its contents horizontally.
    """

    _esm_base = "Box.jsx"
    _constants = {"direction": "row"}


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

    elevation = param.Integer(default=1, bounds=(0, None))

    raised = param.Boolean(default=True, doc="Whether the layout is raised visually.")

    square = param.Boolean(default=False, doc="Whether to disable rounded corners.")

    variant = param.Selector(objects=["elevation", "outlined"], default="elevation")

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

    direction = param.Selector(objects=["row", "column", "column-reverse", "row-reverse"], default="column")

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

    width_option = param.Selector(objects=["xs", "sm", "md", "lg", "xl", False], default="lg")

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

    direction = param.Selector(objects=["row", "column", "column-reverse", "row-reverse"], default="row")

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

    hide_header = param.Boolean(default=False)

    outlined = param.Boolean(default=True)

    title = param.String(doc="""
        A title to be displayed in the Card header, will be overridden
        by the header if defined.""")

    title_css_classes = param.List(doc="""
        List of CSS classes to apply to CardTitle component.""")

    _direction = "vertical"
    _esm_base = "Card.jsx"

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

    color = param.Selector(default="primary", objects=["default", "primary", "secondary"])

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
        model, _ = self._models.get(ref)
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

    orientation = param.Selector(default="horizontal", objects=["horizontal", "vertical"])

    variant = param.Selector(default="fullWidth", objects=["fullWidth", "inset", "middle"])

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

    scroll = param.Selector(objects=["body", "paper"], default="paper", doc="""
        Whether the dialog should scroll the content or the paper.""")

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

    anchor = param.Selector(default="left", objects=["left", "right", "top", "bottom"])

    size = param.Integer(default=250, doc="""
        The width (for left/right anchors) or height (for top/bottom anchors) of the drawer.""")

    open = param.Boolean(default=False, doc="""
        Whether the drawer is open.""")

    variant = param.Selector(default="temporary", objects=["permanent", "persistent", "temporary"])

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


__all__ = [
    "Accordion",
    "Alert",
    "Backdrop",
    "Card",
    "Column",
    "Container",
    "Dialog",
    "Divider",
    "Drawer",
    "FlexBox",
    "Grid",
    "Paper",
    "Row",
    "Tabs",
]
