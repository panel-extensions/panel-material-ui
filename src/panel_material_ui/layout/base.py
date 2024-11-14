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
    elevation = param.Integer(default=1, bounds=(0, None))

    _esm = "Paper.jsx"


class Card(MaterialListLike):
    """
    A `Card` layout allows arranging multiple panel objects in a
    collapsible, vertical container with a header bar.

    Reference: https://panel.holoviz.org/reference/layouts/Card.html

    :Example:

    >>> Card(
    ...   some_widget, some_pane, some_python_object,
    ...   title='Card', styles=dict(background='WhiteSmoke'),
    ... )
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

    _esm = "Card.jsx"

    def select(self, selector: type | Callable[[Viewable], bool] | None = None) -> list[Viewable]:
        return ([] if self.header is None else self.header.select(selector)) + super().select(selector)


class Accordion(MaterialNamedListLike):
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

    _esm = "Accordion.jsx"

    def __init__(self, *objects, **params):
        if "objects" not in params:
            params["objects"] = objects
        super().__init__(**params)


class Tabs(MaterialNamedListLike):
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

    _esm = "Tabs.jsx"

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
    orientation = param.Selector(default="horizontal", objects=["horizontal", "vertical"])

    variant = param.Selector(default="fullWidth", objects=["fullWidth", "inset", "middle"])

    _esm = "Divider.jsx"


class Alert(MaterialListLike):
    closed = param.Boolean(default=False)

    closeable = param.Boolean(default=False)

    severity = param.Selector(objects=["error", "warning", "info", "success"], default="success")

    object = param.String(default="")

    title = param.String(default=None)

    variant = param.Selector(default="filled", objects=["filled", "outlined"])

    _esm = "Alert.jsx"


class Backdrop(MaterialListLike):
    open = param.Boolean(default=False)

    _esm = "Backdrop.jsx"


class Modal(MaterialListLike):
    open = param.Boolean(default=False)

    _esm = "Modal.jsx"


class Dialog(MaterialListLike):
    open = param.Boolean(default=False)

    _esm = "Dialog.jsx"
