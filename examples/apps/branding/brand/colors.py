from dataclasses import dataclass

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
    LIGHT_THEME
