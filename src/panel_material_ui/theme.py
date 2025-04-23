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

MATERIAL_DARK_THEME = {
    "attrs": {
        "figure": {
            "background_fill_color": MATERIAL_SURFACE,
            "border_fill_color": MATERIAL_BACKGROUND,
            "outline_line_color": MATERIAL_DARK_75,
            "outline_line_alpha": 0.25,
        },
        "Grid": {
            "grid_line_color": MATERIAL_TEXT_DIGITAL_DARK,
            "grid_line_alpha": 0.25
        },
        "Axis": {
            "major_tick_line_alpha": 0,
            "major_tick_line_color": MATERIAL_TEXT_DIGITAL_DARK,
            "minor_tick_line_alpha": 0,
            "minor_tick_line_color": MATERIAL_TEXT_DIGITAL_DARK,
            "axis_line_alpha": 0,
            "axis_line_color": MATERIAL_TEXT_DIGITAL_DARK,
            "major_label_text_color": MATERIAL_TEXT_DIGITAL_DARK,
            "major_label_text_font": MATERIAL_FONT,
            "major_label_text_font_size": "1.025em",
            "axis_label_standoff": 10,
            "axis_label_text_color": MATERIAL_TEXT_DIGITAL_DARK,
            "axis_label_text_font": MATERIAL_FONT,
            "axis_label_text_font_size": "1.25em",
            "axis_label_text_font_style": "normal",
        },
        "Legend": {
            "spacing": 8,
            "glyph_width": 15,
            "label_standoff": 8,
            "label_text_color": MATERIAL_TEXT_DIGITAL_DARK,
            "label_text_font": MATERIAL_FONT,
            "label_text_font_size": "1.025em",
            "border_line_alpha": 0,
            "background_fill_alpha": 0.25,
            "background_fill_color": MATERIAL_SURFACE,
        },
        "ColorBar": {
            "title_text_color": MATERIAL_TEXT_DIGITAL_DARK,
            "title_text_font": MATERIAL_FONT,
            "title_text_font_size": "1.025em",
            "title_text_font_style": "normal",
            "major_label_text_color": MATERIAL_TEXT_DIGITAL_DARK,
            "major_label_text_font": MATERIAL_FONT,
            "major_label_text_font_size": "1.025em",
            "background_fill_color": MATERIAL_SURFACE,
            "major_tick_line_alpha": 0,
            "bar_line_alpha": 0,
        },
        "Title": {
            "text_font_size": "1.15em",
        }
    }
}


class MuiDarkTheme(MaterialDarkTheme):

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_DARK_THEME))


class MaterialDesign(Material):

    _resources = {}
    _themes = {'dark': MuiDarkTheme, 'default': MaterialDefaultTheme}

    @classmethod
    def _get_modifiers(cls, viewable, theme, isolated=True):
        modifiers, child_modifiers = super()._get_modifiers(viewable, theme, isolated)
        if hasattr(viewable, '_esm_base'):
            del modifiers['stylesheets']
        return modifiers, child_modifiers


param.Parameterized.__setattr__(config, 'design', MaterialDesign)
