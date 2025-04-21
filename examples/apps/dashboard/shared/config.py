import panel as pn
import param
from panel_material_ui.base import COLORS as _BUTTON_COLORS, COLOR_ALIASES

BODY_BACKGROUND = "#f5f5f5"
BODY_STYLES = {"background": BODY_BACKGROUND, "width": "100vw"}  # Hack
ICON_CSS = """
.material-symbols-outlined {
    font-size: 12px;
}
"""
PAPER_STYLES = {
    "background": "white",
    "border-radius": "5px",
    "border": "1px solid #e5e5e5",
    "box-shadow": "0 1px 2px 0 rgba(0,0,0,.05)",
}
PAGES = [
    {"label": "Dashboard", "href": "dashboard", "icon": "dashboard"},
    {"label": "Tables", "href": "tables", "icon": "table_view"},
    {"label": "Notifications", "href": "notifications", "icon": "notifications"},
]

pn.config.css_files=[
    # "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=schedule,weekend,person,leaderboard"
]

_COLOR = {"Dark": "#42424a", "Transparent": "inherit", "White": "white"}
_BUTTON_COLORS = [color for color in _BUTTON_COLORS if color not in COLOR_ALIASES]

class PageSettings(param.Parameterized):
    dark_theme = param.Boolean(default=False)

    sidebar_button_color = param.Selector(default="dark", objects=_BUTTON_COLORS)
    sidebar_background_color = param.Selector(default="White", objects=["Dark", "Transparent", "White"])
    navbarimportfixed = param.Boolean(default=False)

    def __init__(self, **params):
        super().__init__(**params)

        pn.state.location.sync(self, parameters=["dark_theme", "sidebar_button_color", "sidebar_background_color"])

    @param.depends("dark_theme", watch=True)
    def _handle_dark_theme_change(self):
        pn.config.theme=("dark" if self.dark_theme else "default")

    @param.depends("sidebar_background_color")
    def sidebar_styles(self):
        return {"background": _COLOR[self.sidebar_background_color], "border-radius": "5px", "margin": "10px"}
