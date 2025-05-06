from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

import param
from panel._param import Margin
from panel.viewable import Viewable
from panel.widgets.base import WidgetBase

from ..base import ESMTransform, MaterialComponent

if TYPE_CHECKING:
    T = TypeVar('T')


class TooltipTransform(ESMTransform):

    _transform = """\
import Icon from "@mui/material/Icon";
import Tooltip from "@mui/material/Tooltip";

{esm}

function {output}(props) {{
  const [description] = props.model.useState("description")
  const [description_delay] = props.model.useState("description_delay")

  const widget = <{input} {{...props}} />
  return (description ? (
    <Tooltip
      title={{description}}
      arrow
      enterDelay={{description_delay}}
      enterNextDelay={{description_delay}}
      placement="right"
      slotProps={{{{ popper: {{ container: props.el }} }}}}
    >
      {{widget}}
    </Tooltip>) : widget
  )
}}
"""


class MaterialWidget(MaterialComponent, WidgetBase):
    """
    MaterialWidget is a base class for all Material UI widgets.
    """

    description = param.String(default=None)

    disabled = param.Boolean(default=False)

    label = param.String(default="")

    margin = Margin(default=10)

    width = param.Integer(default=300, bounds=(0, None), allow_None=True)

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
        if isinstance(parameter.owner, MaterialComponent):
            widget.jslink(parameter.owner, value=parameter.name)
        return widget

    def api(self, jslink: bool=False, sizing_mode="stretch_width", **kwargs)->Viewable:
        """Returns an interactive component for exploring the API of the widget.

        Parameters
        ----------
        jslink: bool
            Whether to use jslinks instead of Python based links.
            This does not allow using all types of parameters.
        sizing_mode: str
            Sizing mode for the component.
        kwargs: dict
            Additional arguments to pass to the component.

        Example:
        --------
        >>> pmui.Button(name="Open").api()
        """
        import panel as pn

        import panel_material_ui as pmui
        return pmui.Tabs(
            pn.pane.HTML(self.param, name="Table", sizing_mode="stretch_width"),
            pmui.Row(self.controls(jslink=jslink), self, name="Editor", sizing_mode="stretch_width"),
            sizing_mode=sizing_mode, **kwargs
        )
