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

    # ``sizing_mode`` values that make a widget fill its container along an axis.
    _width_responsive_modes = ("stretch_width", "stretch_both", "scale_width", "scale_both")
    _height_responsive_modes = ("stretch_height", "stretch_both", "scale_height", "scale_both")

    __abstract = True

    def __init__(self, **params):
        if 'label' not in params and 'name' in params:
            params['label'] = params['name']
        self._drop_default_size_for_responsive(params)
        super().__init__(**params)

    def _responsive_axes(self, params):
        """
        Return the ``(width, height)`` param names that physically control the
        horizontal and vertical extent. Identity by default; overridden where a
        widget swaps the axes (e.g. vertical sliders).
        """
        return 'width', 'height'

    def _drop_default_size_for_responsive(self, params):
        """
        Drop the fixed default size when a stretch/scale ``sizing_mode`` is
        requested without an explicit size, so the widget fills its container
        like a core Panel widget instead of staying at its standalone default
        (e.g. ``width=300``). An explicitly passed size is always respected.
        """
        sizing_mode = params.get('sizing_mode')
        if sizing_mode is None:
            return
        cls = type(self)
        axis_modes = zip(
            self._responsive_axes(params),
            (self._width_responsive_modes, self._height_responsive_modes),
            strict=True,
        )
        for axis, responsive_modes in axis_modes:
            if (sizing_mode in responsive_modes and axis not in params
                    and getattr(cls.param, axis).default is not None):
                params[axis] = None

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
