"""
Material UI theme configuration for the Orbitron brand.

This module provides functions to configure Panel Material UI components
with consistent theming, typography, and styling according to brand guidelines.
"""
import panel_material_ui as pmui
import panel as pn
from typing import Dict, Any
from copy import deepcopy

from .colors import DARK_THEME, LIGHT_THEME
from .assets import FAVICON_PATH, LOGO_PATH, RAW_CSS

# Theme configuration for light mode
_LIGHT_THEME_CONFIG: Dict[str, Any] = {
    "palette": {
        "primary": {
            "main": LIGHT_THEME.primary,
        },
        "secondary": {"main": LIGHT_THEME.secondary},
        "success": {"main": LIGHT_THEME.success},
        "error": {"main": LIGHT_THEME.error},
        "warning": {"main": LIGHT_THEME.warning},
        "info": {"main": LIGHT_THEME.info},
        "contrastThreshold": 3,
        "tonalOffset": 0.2,
    },
    "typography": {
        "fontFamily": ("Montserrat", "Helvetica Neue", "Arial", "sans-serif"),
        "fontSize": 16,
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
            },
        },
    },
}

# Create dark theme configuration from light theme
_DARK_THEME_CONFIG = deepcopy(_LIGHT_THEME_CONFIG)
_DARK_THEME_CONFIG["palette"]["primary"] = {
    "main": DARK_THEME.primary,
}
_DARK_THEME_CONFIG["palette"]["secondary"] = {
    "main": DARK_THEME.secondary,
}

# Combined theme configuration
THEME_CONFIG: Dict[str, Dict[str, Any]] = {
    "light": _LIGHT_THEME_CONFIG,
    "dark": _DARK_THEME_CONFIG,
}

# Custom notification message
_DISCONNECT_NOTIFICATION: str = """The connection to the server was lost. Please refresh to \
reconnect."""

# Montserrat font URL
_MONTSERRAT_FONT_URL: str = "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap"


def _configure_session() -> None:
    """
    Configure Panel session-specific settings.

    This includes disconnect notifications and other session-level configurations.
    """
    pn.config.disconnect_notification = _DISCONNECT_NOTIFICATION


@pn.cache
def _configure_general() -> None:
    """
    Configure general theme settings for Panel Material UI components.

    This includes theme configuration, CSS, fonts, logos, and component defaults.
    """
    # Page configuration
    pmui.Page.param.theme_config.default = THEME_CONFIG

    # CSS and font configuration
    if RAW_CSS:
        pmui.Page.config.raw_css.append(RAW_CSS)

    pmui.Page.config.css_files.append(_MONTSERRAT_FONT_URL)

    # Brand assets configuration
    pmui.Page.param.logo.default = LOGO_PATH
    pmui.Page.favicon = FAVICON_PATH
    pmui.Page.meta.apple_touch_icon = ""  # Intentionally left empty
    pmui.Page.meta.name = "Orbitron"

    # Component-specific configurations
    pmui.Button.param.disable_elevation.default = True

    # Fix missing closing bracket in stylesheets
    pn.pane.Image.stylesheets = ["img {border-radius: 2px}"]
    pn.widgets.Tabulator.param.theme = "materialize"


def configure() -> None:
    """
    Configure the complete theme for the application.

    This is the main entry point for applying the Orbitron brand theme
    to a Panel Material UI application.

    Examples
    --------
    >>> from brand.mui import configure
    >>> configure()
    >>> app = pmui.Page(title="My Orbitron App")
    """
    _configure_general()
    _configure_session()


# If module is run directly, apply configuration
if __name__ == "__main__":
    configure()
