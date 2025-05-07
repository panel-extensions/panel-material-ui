"""
Color definitions and utilities for brand theming.

This module provides a consistent color palette for both light and dark themes,
along with utility functions to retrieve appropriate colors for different visualization needs.
"""
from dataclasses import dataclass
from typing import List
import panel_material_ui as pmui


@dataclass(frozen=True)
class ThemeColors:
    """
    Container for theme color definitions.

    Attributes
    ----------
    primary : str
        Primary brand color (hex format)
    secondary : str
        Secondary brand color (hex format)
    success : str
        Color for success states (hex format)
    error : str
        Color for error states (hex format)
    warning : str
        Color for warning states (hex format)
    info : str
        Color for information states (hex format)
    """
    primary: str = "#4099da"
    secondary: str = "#644c76"
    success: str = "#8ecdc8"
    error: str = "#e85757"
    warning: str = "#fdd779"
    info: str = "#644c76"


# Predefined theme instances
LIGHT_THEME = ThemeColors()

DARK_THEME = ThemeColors(
    primary=LIGHT_THEME.secondary,
    secondary=LIGHT_THEME.primary,
)


def get_colors(dark_theme: bool = False) -> ThemeColors:
    """
    Get the theme colors based on the dark theme flag.

    Parameters
    ----------
    dark_theme : bool, default=False
        If True, return dark theme colors. Otherwise, return light theme colors.

    Returns
    -------
    ThemeColors
        Color palette object for the requested theme
    """
    return DARK_THEME if dark_theme else LIGHT_THEME


# Predefined color maps
LIGHT_CMAP = pmui.theme.linear_gradient("#ffffff", LIGHT_THEME.primary, n=256)
DARK_CMAP = pmui.theme.linear_gradient("#222222", DARK_THEME.primary, n=256)


def get_continuous_cmap(dark_theme: bool = False) -> List[str]:
    """
    Get the continuous color map based on the dark theme flag.

    Parameters
    ----------
    dark_theme : bool, default=False
        If True, return dark theme color map. Otherwise, return light theme color map.

    Returns
    -------
    List[str]
        List of hex color codes forming a continuous color map
    """
    return DARK_CMAP if dark_theme else LIGHT_CMAP


def get_categorical_palette(dark_theme: bool = False, n_colors: int = 20) -> List[str]:
    """
    Get a categorical color palette based on the dark theme flag.

    For small palettes (n_colors <= 5), returns the theme's main colors.
    For larger palettes, generates additional colors based on the primary color.

    Parameters
    ----------
    dark_theme : bool, default=False
        If True, return dark theme color palette. Otherwise, return light theme color palette.
    n_colors : int, default=20
        Number of colors in the returned palette.

    Returns
    -------
    List[str]
        List of hex color codes suitable for categorical data
    """
    colors = get_colors(dark_theme)
    palette = [
        colors.primary,
        colors.secondary,
        colors.success,
        colors.warning,
        colors.error,
    ]
    if n_colors <= len(palette):
        return palette[:n_colors]
    return pmui.theme.generate_palette(colors.primary, n_colors=n_colors)
