from __future__ import annotations

import colorsys
import pathlib

import numpy as np
import param
from bokeh.themes import Theme as _BkTheme
from panel.config import config
from panel.io.resources import (
    CDN_DIST,
    component_resource_path,
    resolve_custom_path,
)
from panel.io.state import state
from panel.theme.base import THEME_CSS, Theme
from panel.theme.material import Material, MaterialDarkTheme, MaterialDefaultTheme
from panel.util import relative_to
from panel.viewable import Viewable

MATERIAL_UI_ICONS = """
.material-icons { font-family: 'Material Icons'; }
.material-icons-outlined { font-family: 'Material Icons Outlined'; }
"""

MATERIAL_THEME = {
    "attrs": {
        "Axis": {
            "axis_label_standoff": 10,
            "axis_label_text_font_size": "1.25em",
            "axis_label_text_font_style": "normal",
            "major_label_text_font_size": "1.025em",
        },
        "Legend": {
            "spacing": 8,
            "glyph_width": 15,
            "label_standoff": 8,
            "label_text_font_size": "1.025em",
        },
        "ColorBar": {
            "title_text_font_size": "1.025em",
            "title_text_font_style": "normal",
            "major_label_text_font_size": "1.025em",
        },
        "Title": {
            "text_font_size": "1.15em",
        },
    }
}

def rgb2hex(rgb: tuple[int, int, int]) -> str:
    """
    Convert RGB tuple to hex.

    Parameters
    ----------
    rgb : tuple
        The RGB(A) tuple to convert.

    Returns
    -------
    str
        The hex color.
    """
    return "#{:02x}{:02x}{:02x}".format(*(int(v*255) for v in rgb))

def hex2rgb(hex: str) -> tuple[int, int, int]:
    """
    Convert hex color to RGB tuple.

    Parameters
    ----------
    hex : str
        The hex color to convert.

    Returns
    -------
    tuple[int, int, int]
        The RGB tuple.
    """
    return [int(hex[i : i + 2], 16) for i in range(1, 6, 2)]

def linear_gradient(start_hex: str, finish_hex: str, n: int = 10) -> list[str]:
    """
    Interpolates the color gradient between to hex colors.

    Parameters
    ----------
    start_hex : str
        The starting hex color.
    finish_hex : str
        The finishing hex color.
    n : int, optional
        The number of colors to generate.

    Returns
    -------
    list[str]
        A list of colors in hex format.
    """
    s = hex2rgb(start_hex)
    f = hex2rgb(finish_hex)
    gradient = [s]
    for t in range(1, n):
        curr_vector = [int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)]
        gradient.append(curr_vector)
    return [rgb2hex([c/255. for c in rgb]) for rgb in gradient]

def generate_palette(color: str, n_colors: int = 3) -> list[str]:
    """
    Generate a palette of colors from a base color.

    Parameters
    ----------
    color : str
        The base color to generate the palette from.
    n_colors : int, optional
        The number of colors to generate.

    Returns
    -------
    list[str]
        A list of colors in hex format.
    """
    hex_color = color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # noqa

    hues = np.linspace(0, 1, int(n_colors) + 1)[:-1]
    hues += h
    hues %= 1
    hues -= hues.astype(int)
    rgb_palette = [colorsys.hls_to_rgb(h_i, l, s) for h_i in hues]
    hex_palette = [
        f"#{int(r_i * 255):02x}{int(g_i * 255):02x}{int(b_i * 255):02x}"
        for r_i, g_i, b_i in rgb_palette
    ]
    return hex_palette


class MuiDefaultTheme(MaterialDefaultTheme):

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_THEME))

class MuiDarkTheme(MaterialDarkTheme):

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_THEME))


class MaterialDesign(Material):

    modifiers = {
        **Material.modifiers,
        Viewable: {
            'stylesheets': Material.modifiers[Viewable]['stylesheets'] + [MATERIAL_UI_ICONS]
        }
    }

    _resources = {}
    _themes = {'dark': MuiDarkTheme, 'default': MuiDefaultTheme}

    @classmethod
    def _get_modifiers(cls, viewable, theme, isolated=None):
        if isolated is None:
            isolated = not hasattr(viewable, '_esm_base')
        theme_type = type(theme) if isinstance(theme, Theme) else theme
        is_server = bool(state.curdoc.session_context) if not state._is_pyodide and state.curdoc else False
        modifiers, child_modifiers = cls._resolve_modifiers(type(viewable), theme_type, is_server=is_server)  # type: ignore
        modifiers = dict(modifiers)
        if hasattr(viewable, '_esm_base'):
            del modifiers['stylesheets']
        else:
            pre = list(cls._resources.get('css', {}).values())
            css = pathlib.Path(theme.css)
            if css:
                if relative_to(css, THEME_CSS):
                    css = f'{CDN_DIST}bundled/theme/{css.name}'
                elif resolve_custom_path(theme, css):
                    css = component_resource_path(theme, 'css', css)
                else:
                    css = css.read_text(encoding='utf-8')
                pre.append(css)
            modifiers['stylesheets'] = pre + modifiers['stylesheets']
        return modifiers, child_modifiers


param.Parameterized.__setattr__(config, 'design', MaterialDesign)
