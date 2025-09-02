from __future__ import annotations

import json
import os

import bokeh
from bokeh.embed.bundle import URL
from packaging.version import Version
from panel.io.cache import cache
from panel.pane.base import panel
from panel.pane.image import ImageBase

bokeh_version = Version(Version(bokeh.__version__).base_version)
BOKEH_GE_3_8 = bokeh_version >= Version('3.8')

@cache
def _read_icon(icon):
    """
    Read an icon from a file or URL and return a base64 encoded string.
    """
    if os.path.isfile(icon):
        img = panel(icon)
        if not isinstance(img, ImageBase):
            raise ValueError(f"Could not determine file type of logo: {icon}.")
        imgdata = img._data(img.object)
        if imgdata:
            icon_string = img._b64(imgdata)
            if str(icon).endswith('.ico'):
                icon_string = icon_string.replace("data:image/ico;", "data:image/x-icon;")
        else:
            raise ValueError(f"Could not embed logo {icon}.")
    else:
        icon_string = icon
    return icon_string

def conffilter(value):
    return json.dumps(dict(value)).replace('"', '\'')

class json_dumps(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, URL):
            return str(obj)
        return super().default(obj)
