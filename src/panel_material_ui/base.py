from __future__ import annotations

import param
from panel.config import config
from panel.custom import ReactComponent

COLORS = ["primary", "secondary", "error", "info", "success", "warning"]


class MaterialComponent(ReactComponent):
    theme = param.Selector(default=config.theme, objects=["default", "dark"])

    _importmap = {
        "imports": {
            "@mui/material/": "https://esm.sh/@mui/material@6.1.7/",
            "@mui/icons-material/": "https://esm.sh/@mui/icons-material@6.1.6/",
        }
    }

    # _bundle = "panel-material-ui.bundle.js"

    __abstract = True
