from __future__ import annotations

import param
from panel._param import Margin
from panel.widgets.base import WidgetBase

from ..base import ESMTransform, MaterialComponent


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
      placement="right"
      slotProps={{{{ popper: {{ container: props.el }} }}}}
    >
      {{widget}}
    </Tooltip>) : widget
  )
}}
"""


class MaterialWidget(MaterialComponent, WidgetBase):
    description = param.String()

    disabled = param.Boolean(default=False)

    label = param.String(default="")

    margin = Margin(default=10)

    width = param.Integer(default=300, bounds=(0, None))

    __abstract = True

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
