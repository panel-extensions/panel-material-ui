from dataclasses import dataclass
import panel_material_ui as pmui

@dataclass(frozen=True)
class ThemeColors:
    primary: str = "#4099da"
    secondary: str =  "#644c76"
    success: str = "#8ecdc8"
    error: str = "#e85757"
    warning: str = "#fdd779"
    info: str = "#644c76"

LIGHT_THEME = ThemeColors()

DARK_THEME = ThemeColors(
    primary =  LIGHT_THEME.secondary,
    secondary = LIGHT_THEME.primary,
)

def get_colors(dark_theme: bool = True) -> ThemeColors:
    """
    Get the theme colors based on the dark theme flag.

    Args:
        dark_theme (bool): If True, return dark theme colors. Otherwise, return light theme colors.
    """
    if dark_theme:
        return DARK_THEME
    return LIGHT_THEME

LIGHT_CMAP = pmui.theme.linear_gradient("#ffffff", LIGHT_THEME.primary, n=256)
DARK_CMAP = pmui.theme.linear_gradient("#ffffff", DARK_THEME.primary, n=256)

def get_continous_cmap(dark_theme: bool = False) -> str:
    """
    Get the color map based on the dark theme flag.

    Args:
        dark_theme (bool): If True, return dark theme color map. Otherwise, return light theme color map.
    """
    if dark_theme:
        return DARK_CMAP
    return LIGHT_CMAP

def get_categorical_palette(dark_theme: bool=False, n_colors=20):
    """
    Get the categorical color palette based on the dark theme flag.
    Args:
        dark_theme (bool): If True, return dark theme color palette. Otherwise, return light theme color palette.
        n_colors (int): Number of colors in the palette.
    """
    colors = get_colors(dark_theme)
    palette = [colors.primary, colors.secondary, colors.success, colors.warning, colors.error]
    if n_colors <= len(palette):
        return palette[:n_colors]
    return pmui.theme.generate_palette(colors.primary, n_colors=n_colors)
