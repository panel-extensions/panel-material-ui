from __future__ import annotations

import param
from bokeh.themes import Theme as _BkTheme
from panel.config import config
from panel.theme.material import Material, MaterialDarkTheme, MaterialDefaultTheme

MATERIAL_FONT = "Roboto, sans-serif, Verdana"
MATERIAL_BACKGROUND = "#121212"
MATERIAL_DARK_75 = "#1c1c1c"
MATERIAL_SURFACE = "#252525"
MATERIAL_DARK_25 = "#5c5c5c"
MATERIAL_TEXT_DIGITAL_DARK = "#ffffff"

MATERIAL_THEME = {
    "attrs": {
        "Axis": {
            "major_label_text_font_size": "1.025em",
            "axis_label_standoff": 10,
            "axis_label_text_font_size": "1.25em",
            "axis_label_text_font_style": "normal",
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


class MuiDefaultTheme(MaterialDefaultTheme):

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_THEME))

class MuiDarkTheme(MaterialDarkTheme):

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_THEME))


class MaterialDesign(Material):

    _resources = {}
    _themes = {'dark': MuiDarkTheme, 'default': MuiDefaultTheme}

    @classmethod
    def _get_modifiers(cls, viewable, theme, isolated=False):
        modifiers, child_modifiers = super()._get_modifiers(viewable, theme, isolated)
        if hasattr(viewable, '_esm_base'):
            del modifiers['stylesheets']
        return modifiers, child_modifiers


param.Parameterized.__setattr__(config, 'design', MaterialDesign)
