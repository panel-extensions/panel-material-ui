from __future__ import annotations

import param
from bokeh.themes import Theme as _BkTheme
from panel.config import config
from panel.theme.material import (
    MATERIAL_DARK_THEME,
    MATERIAL_THEME,
    Material,
    MaterialDarkTheme,
    MaterialDefaultTheme,
)


class MaterialLight(MaterialDefaultTheme):

    base_css = param.Filename(default=None)

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_THEME))


class MaterialDark(MaterialDarkTheme):

    base_css = param.Filename(default=None)

    bokeh_theme = param.ClassSelector(
        class_=(_BkTheme, str), default=_BkTheme(json=MATERIAL_DARK_THEME))


class MaterialDesign(Material):

    _resources = {}
    _themes = {'dark': MaterialDark, 'default': MaterialLight}


config.design = MaterialDesign
