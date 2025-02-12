from __future__ import annotations

import param
from bokeh.themes import Theme as _BkTheme
from panel.config import config
from panel.theme import DarkTheme, DefaultTheme, Native
from panel.theme.material import (
    MATERIAL_DARK_THEME,
    MATERIAL_THEME,
)
from panel.widgets import Tabulator


class MaterialLight(DefaultTheme):

    base_css = param.Filename(default=None)

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_THEME))


class MaterialDark(DarkTheme):

    base_css = param.Filename(default=None)

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_DARK_THEME))


class MaterialDesign(Native):

    modifiers = {
        Tabulator: {
            'theme': 'materialize'
        },
    }

    _themes = {'dark': MaterialDark, 'default': MaterialLight}


config.design = MaterialDesign
