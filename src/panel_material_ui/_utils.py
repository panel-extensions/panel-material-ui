import os

from panel.io.cache import cache
from panel.pane.base import panel
from panel.pane.image import ImageBase


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
        else:
            raise ValueError(f"Could not embed logo {icon}.")
    else:
        icon_string = icon
    return icon_string
