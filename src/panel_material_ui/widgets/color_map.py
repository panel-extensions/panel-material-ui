from __future__ import annotations

import numpy as np
import param
from panel.widgets.select import ColorMap as _PnColorMap

from .base import MaterialWidget


def _sample_colormap(cmap):
    if "matplotlib" not in getattr(cmap, "__module__", ""):
        return cmap

    samples = np.linspace(0, 1, getattr(cmap, "N", 10))
    rgba_tmpl = "rgba({0}, {1}, {2}, {3:.3g})"
    return [rgba_tmpl.format(*(rgba[:3] * 255).astype(int), rgba[-1]) for rgba in cmap(samples)]


class ColorMap(MaterialWidget, _PnColorMap):
    """Select a colormap from a dictionary of palettes."""

    error_state = param.Boolean(default=False, doc="Whether to display the widget in an error state.")
    helper_text = param.String(default="", doc="Helper text displayed below the widget.")
    options = param.Dict(default={}, doc="Dictionary of colormaps.")
    ncols = param.Integer(default=1, bounds=(1, None), doc="Number of columns of swatches to display.")
    swatch_height = param.Integer(default=20, bounds=(1, None), doc="Height of the color swatches.")
    swatch_width = param.Integer(default=100, bounds=(1, None), doc="Width of the color swatches.")
    value = param.Parameter(default=None, doc="The selected colormap.")
    value_name = param.String(default=None, allow_None=True, doc="Name of the selected colormap.")

    _esm_base = "ColorMap.jsx"
    _rename = {"options": "options", "value_name": None, "title": None}

    def _process_param_change(self, params):
        options = params.pop("options", None)
        params.pop("title", None)
        if "value" in params and not isinstance(params["value"], (str, type(None))):
            option_source = self.options if options is None else options
            for index, option in enumerate(option_source.values()):
                if option == params["value"]:
                    params["value"] = list(option_source)[index]
                    break
        props = MaterialWidget._process_param_change(self, params)
        props.pop("title", None)
        if options is not None:
            props["options"] = {name: _sample_colormap(cmap) for name, cmap in options.items()}
        return props

    def _process_property_change(self, msg):
        msg = MaterialWidget._process_property_change(self, msg)
        if "value" in msg:
            value = msg["value"]
            if value is None or (isinstance(value, str) and value == ""):
                msg["value"] = None
            elif isinstance(value, str) and value in self.options:
                msg["value"] = self.options[value]
            else:
                msg = _PnColorMap._process_property_change(self, msg)
        return msg


__all__ = ["ColorMap"]
