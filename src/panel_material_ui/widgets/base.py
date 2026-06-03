from __future__ import annotations

import typing as t

import param
from panel._param import Margin
from panel.viewable import Children
from panel.widgets.base import WidgetBase

from ..base import MaterialComponent

if t.TYPE_CHECKING:
    T = t.TypeVar('T')


class MaterialWidget(MaterialComponent, WidgetBase):
    """
    MaterialWidget is a base class for all Material UI widgets.

    Example
    -------
    >>> MaterialWidget(label='My Widget', description='Helpful info')
    """

    attached = Children(doc="""
        Elements that are attached to this object but are not direct
        children.""")
    description = param.String(default="", doc="Tooltip text to display when hovering over the widget.")
    disabled = param.Boolean(default=False, doc="Whether the widget is disabled.")
    label = param.String(default="", doc="The label for the widget.")
    margin = Margin(default=10, doc="Margin around the widget.")
    width = param.Integer(default=300, bounds=(0, None), allow_None=True, doc="Width of the widget.")

    _rename = {"label": "label"}

    __abstract = True

    def __init__(self, **params):
        if 'label' not in params and 'name' in params:
            params['label'] = params['name']
        super().__init__(**params)

    def _process_param_change(self, params):
        description = params.pop("description", None)
        icon = params.pop("icon", None)
        label = params.pop("label", None)
        props = MaterialComponent._process_param_change(self, params)
        if icon:
            props["icon"] = icon
        if label:
            props["label"] = label
        if description:
            props["description"] = description
        return props

    def focus(self):
        """
        Sends a message to the frontend to focus the widget.
        """
        self._send_msg({"action": "focus"})

    @classmethod
    def from_param(cls: type[T], parameter: param.Parameter, **params) -> T:
        """
        Construct a widget from a Parameter and link the two
        bi-directionally.

        Parameters
        ----------
        parameter: param.Parameter
          A parameter to create the widget from.

        Returns
        -------
        Widget instance linked to the supplied parameter
        """
        widget = super().from_param(parameter, **params)
        if isinstance(parameter.owner, MaterialComponent) and isinstance(parameter.name, str):
            widget.jslink(parameter.owner, value=parameter.name)
        return widget
