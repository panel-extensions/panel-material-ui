from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import param
from bokeh.models import Spacer as BkSpacer
from panel.layout.base import ListLike, NamedListLike
from panel.viewable import Child

from ..base import MaterialComponent

if TYPE_CHECKING:
    from panel.viewable import Viewable


class MaterialListLike(MaterialComponent, ListLike):
    __abstract = True

    def __init__(self, *objects, **params):
        if objects:
            params["objects"] = objects
        super().__init__(**params)


class MaterialNamedListLike(MaterialComponent, NamedListLike):

    __abstract = True



class Paper(MaterialListLike):
    """
    Paper implements a container for displaying content on an elevated surface.

    Reference to the Material UI Paper component:
    https://mui.com/material-ui/react-paper/

    :Example:
    >>> Paper(name="Paper", objects=[1, 2, 3], elevation=10, width=200, height=200)
    """

    elevation = param.Integer(default=1, bounds=(0, None))

    _esm_base = "Paper.jsx"


class Card(MaterialListLike):
    """
    A `Card` layout allows arranging multiple panel objects in a
    collapsible, vertical container with a header bar.

    :Example:

    >>> Card(some_widget, some_pane, some_python_object, title='Card')
    """

    collapsed = param.Boolean(
        default=False,
        doc="""
        Whether the contents of the Card are collapsed.""",
    )

    collapsible = param.Boolean(
        default=True,
        doc="""
        Whether the Card should be expandable and collapsible.""",
    )

    elevation = param.Integer(default=1, bounds=(0, None))

    header = Child(
        doc="""
        A Panel component to display in the header bar of the Card.
        Will override the given title if defined."""
    )

    raised = param.Boolean(
        default=True,
        doc="""
        Whether the Card should be visually raised above the background.""",
    )

    title = param.String(
        doc="""
        A title to be displayed in the Card header, will be overridden
        by the header if defined."""
    )

    outlined = param.Boolean(default=False)

    _esm_base = "Card.jsx"

    def select(self, selector: type | Callable[[Viewable], bool] | None = None) -> list[Viewable]:
        return ([] if self.header is None else self.header.select(selector)) + super().select(selector)


class Accordion(MaterialNamedListLike):
    """
    The `Accordion` layout is a type of `Card` layout that allows switching
    between multiple objects by clicking on the corresponding card header.

    The labels for each card will default to the `name` parameter of the card’s
    contents, but may also be defined explicitly as part of a tuple.

    `Accordion` has a list-like API that allows
    interactively updating and modifying the cards using the methods `append`,
    `extend`, `clear`, `insert`, `pop`, `remove` and `__setitem__`.

    Missing features (if any) when comparing with the corresponding
    Panel Accordion layout [panel.Accordion](https://panel.holoviz.org/reference/layouts/Accordion.html):
    `active_header_background`, `header_background`, `header_color`, `scroll`

    Reference to the Material UI Accordion component:
    https://mui.com/material-ui/react-accordion/

    :Example:

    >>> Accordion(("Card 1", "Card 1 objects"), ("Card 2", "Card 2 objects"))
    """

    active = param.List(
        default=[],
        doc="""
        List of indexes of active cards.""",
    )

    toggle = param.Boolean(
        default=False,
        doc="""
        Whether to toggle between active cards or allow multiple cards""",
    )

    _names = param.List(default=[])

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
    inferred from the `name` parameter of the tab’s contents.

    Like `Accordion`, `Tabs` has a list-like API with methods to
    `append`, `extend`, `clear`, `insert`, `pop`, `remove` and `__setitem__`,
    which make it possible to interactively update and modify the tabs.

    Missing features (if any) when comparing with the corresponding
    Panel Tabs layout [panel.Tabs](https://panel.holoviz.org/reference/layouts/Tabs.html):
    `closable`, `scroll`.

    Reference to the Material UI Accordion component:
    https://mui.com/material-ui/react-tabs/

    :Example:

    >>> Tabs(("Tab 1", "Tab 1 objects"), ("Tab 2", "Card 2 objects"))

    """
    active = param.Integer(
        default=0,
        bounds=(0, None),
        doc="""
        Index of the currently displayed objects.""",
    )

    color = param.Selector(default="primary", objects=["primary", "secondary"])

    dynamic = param.Boolean(default=False)

    tabs_location = param.ObjectSelector(
        default="above",
        objects=["above", "below", "left", "right"],
        doc="""
        The location of the tabs relative to the tab contents.""",
    )

    _names = param.List(default=[])

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
        models = []
        for i, sv in enumerate(child):
            if self.dynamic and i != self.active:
                model = BkSpacer()
            elif ref in sv._models:
                model = sv._models[ref][0]
            else:
                model = sv._get_model(doc, root, parent, comm)
            models.append(model)
        return models


class Divider(MaterialListLike):
    """
    A `Divider` draws a horizontal rule (a `<hr>` tag in HTML) to separate
    multiple components in a layout.

    Reference to the equivalent Panel Divider layout:
    https://panel.holoviz.org/reference/layouts/Divider.html

    :Example:

    >>> Divider(sizing_mode="stretch_width")
    """

    orientation = param.Selector(default="horizontal", objects=["horizontal", "vertical"])

    variant = param.Selector(default="fullWidth", objects=["fullWidth", "inset", "middle"])

    _esm_base = "Divider.jsx"


class Alert(MaterialListLike):

    closed = param.Boolean(default=False)

    closeable = param.Boolean(default=False)

    severity = param.Selector(objects=["error", "warning", "info", "success"], default="success")

    object = param.String(default="")

    title = param.String(default=None)

    variant = param.Selector(default="filled", objects=["filled", "outlined"])

    _esm_base = "Alert.jsx"


class Backdrop(MaterialListLike):
    """
    The `Backdrop` component can be used to create a semi-transparent overlay over the application's UI.
    It is often used to focus attention on a specific part of the interface,
    such as during loading states or while a modal dialog is open.

    Reference to the corresponding Material UI `Backdrop`:
    https://mui.com/material-ui/react-backdrop/

    :Example:
    >>> close = Button(on_click=lambda _: backdrop.param.update(open=False), label='Close')  # type: ignore
    >>> backdrop = Backdrop(LoadingIndicator(), close)
    >>> button = Button(on_click=lambda _: backdrop.param.update(open=True), label=f'Open {Backdrop.name}')
    >>> pn.Column(button, backdrop).servable()
    """

    open = param.Boolean(default=False)

    _esm_base = "Backdrop.jsx"


class Dialog(MaterialListLike):
    """
    The `Dialog` can be used to display important content in a modal-like overlay that requires
    user interaction. It is often used for tasks such as confirmations, forms, or displaying
    additional information.

    Reference to the corresponding Material UI `Dialog`:
    https://mui.com/material-ui/react-dialog/

    :Example:
    >>> close = Button(on_click=lambda _: dialog.param.update(open=False), label='Close')  # type: ignore
    >>> dialog = Dialog("This is a modal", close)
    >>> button = Button(on_click=lambda _: dialog.param.update(open=True), label=f'Open {Dialog.name}')
    >>> pn.Column(button, dialog).servable()
    """

    full_screen = param.Boolean(default=False)

    open = param.Boolean(default=False)

    title = param.String(default="")

    _esm_base = "Dialog.jsx"
