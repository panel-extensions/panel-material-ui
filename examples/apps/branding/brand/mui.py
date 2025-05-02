import panel_material_ui as pmui
import panel as pn
from .colors import DARK_THEME, LIGHT_THEME
from .assets import FAVICON_URL, LOGO_SVG_URL, RAW_CSS
from copy import deepcopy

_LIGHT_THEME_CONFIG = {
    "palette": {
            "primary": {"main": LIGHT_THEME.primary,},
            "secondary": {"main": LIGHT_THEME.secondary},
            "success": {"main": LIGHT_THEME.success},
            "error": {"main": LIGHT_THEME.error},
            "warning": {"main": LIGHT_THEME.warning},
            "info": {"main": LIGHT_THEME.info},
            "contrastThreshold": 3,
            "tonalOffset": 0.2
        },
        "typography": {
            "fontFamily": ("Montserrat", "Helvetica Neue", "Arial", "sans-serif"),
            "fontSize": 16,
            # The values below don't seem to be used
            "fontWeight": 700,
            "letterSpacing": 10.2,
            "lineHeight": 1.5,
        },
        "shape": {
            "borderRadius": 8,
        },
        "components": {
            "MuiButtonBase": {
            "defaultProps": {
                "disableRipple": True,
                "disableElevation": True,
            },
            },
        },
}
_DARK_THEME_CONFIG = deepcopy(_LIGHT_THEME_CONFIG)
_DARK_THEME_CONFIG["palette"]["primary"] = {
    "main": DARK_THEME.primary,
}
_DARK_THEME_CONFIG["palette"]["secondary"] = {
    "main": DARK_THEME.secondary,
}

THEME_CONFIG = {
    "light": _LIGHT_THEME_CONFIG,
    "dark": _DARK_THEME_CONFIG,
}

# @pn.cache
def configure():
    """
    Configure the theme for the application.
    """
    pmui.Page.param.theme_config.default = THEME_CONFIG["light"]

    pmui.Page.config.raw_css.append(RAW_CSS)
    pmui.Page.config.css_files.append("https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap")
    # The below DOES NOT WORK YET
    # pmui.Page.param.logo.default = LOGO_SVG_URL
    # pmui.Page.param.favicon.default = FAVICON_URL
    pmui.Page.meta.icon = FAVICON_URL
    pmui.Page.meta.name = "Company"
