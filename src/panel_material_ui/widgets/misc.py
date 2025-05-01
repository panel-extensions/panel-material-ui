from __future__ import annotations

import param
from panel.widgets.misc import FileDownload as _FileDownload

from .button import _ButtonBase


class FileDownload(_ButtonBase, _FileDownload):
    """
    The `FileDownload` widget allows a user to download a file.

    It works either by sending the file data to the browser on initialization
    (`embed`=True), or when the button is clicked.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/FileDownload.html
    - https://panel.holoviz.org/reference/widgets/FileDownload.html
    - https://mui.com/material-ui/react-button/

    :Example:

    >>> FileDownload(file='IntroductionToPanel.ipynb', filename='intro.ipynb')
    """

    icon_size = param.String(default="1em", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""")

    _esm_base = "FileDownload.jsx"
    _rename = {"_clicks": None, "icon": "icon", "icon_size": "icon_size"}
    _source_transforms = {"button_type": None, "button_style": None, "callback": None, "file": None, "value": None}

    def __init__(self, file=None, **params):
        self._default_label = 'label' not in params
        self._synced = False
        super().__init__(file=file, **params)

    def _handle_click(self, event=None):
        self._clicks += 1

__all__ = [
    "FileDownload"
]
