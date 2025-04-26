# Default options

import panel as pn
import panel_material_ui as pmu
import polars
import holoviews as hv
import hvplot.pandas
import seaborn as sns
import numpy as np
import colorsys
import pandas as pd
from bokeh.themes._light_minimal import json as BOKEH_LIGHT
from bokeh.themes._dark_minimal import json as BOKEH_DARK
from bokeh.themes import Theme
from copy import deepcopy
import matplotlib.colors as mcolors

pn.extension(sizing_mode="stretch_width")
pmu.Paper.margin=10

LORUM_IPSUM = """\
**Lorem Ipsum** is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the
industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type
and scrambled it to make a type specimen book"""

# General Code: COULD BE PART OF panel_material_ui.theme module?

@pn.cache
def get_categorical_palette(color: str, n_colors: int=3)->list[str]:
    hex_color = color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    hues = np.linspace(0, 1, int(n_colors) + 1)[:-1]
    hues += h
    hues %= 1
    hues -= hues.astype(int)
    rgb_palette = [colorsys.hls_to_rgb(h_i, l, s) for h_i in hues]
    hex_palette = ['#{:02x}{:02x}{:02x}'.format(int(r_i * 255), int(g_i * 255), int(b_i * 255)) for r_i, g_i, b_i in rgb_palette]
    return hex_palette

def get_continous_color_map(color: str):
    return mcolors.LinearSegmentedColormap.from_list(
        'custom_cmap', ['white', color], N=256
    )

def get_bokeh_theme(dark_theme: bool, font_family: str="Helvetica"):
    if dark_theme:
        json = BOKEH_DARK
    else:
        json = BOKEH_LIGHT

    json = deepcopy(json)
    for key1, val1 in json.items():
        for key2, val2 in val1.items():
            for key3 in val2:
                if key3.endswith("_font"):
                    json[key1][key2][key3]=font_family

    return Theme(json=json)


# App Code

@pn.cache
def get_theme_config(primary_color, font_family="fantasy"):
    return {
        "palette": {
            "primary": {
                "main": primary_color,
            },
        },
        "typography": {
            "fontFamily": (font_family, ),
        }
    }

@pn.cache
def get_data(n_categories: int, n_rows=100):
    x = np.random.rand(n_rows)
    y = np.random.rand(n_rows)

    categories = [f'Category {i+1}' for i in range(n_categories)]
    category = np.random.choice(categories, n_rows)

    dataframe = pd.DataFrame({
        'x': x,
        'y': y,
        'category': category
    })

    return dataframe

def get_categorical_plot(df, colors):
    plot = df.hvplot.scatter(x='x', y='y', by='category', title="Categorical Plot")
    plot.opts(hv.opts.Scatter(color=hv.Cycle(colors),))
    return plot

def get_continous_plot(color="#9c27b0"):
    np.random.seed(42)
    data = pd.DataFrame({
        'x': np.random.rand(100),
        'y': np.random.rand(100),
        'value': np.random.rand(100) * 100  # Continuous variable
    })
    custom_cmap = get_continous_color_map(color)

    return data.hvplot.scatter(
        x='x',
        y='y',
        c='value',  # Use the 'value' column for color mapping
        cmap=custom_cmap,  # Continuous color map
        colorbar=True,  # Show color bar
        title='Continuous Plot'
    )

paper = pmu.Checkbox(value=True, name="Paper", sizing_mode="fixed", align="center")
theme = pmu.ThemeToggle(sizing_mode="fixed", align="center")
font_family = pmu.Select(name="Font", options=["Roboto", "Impact", "Palatino Linotype"])

primary_color = pmu.ColorPicker(value="#9c27b0", name="Primary Color",)
theme_config = pn.bind(get_theme_config, primary_color, font_family)
n_colors = pmu.IntSlider(value=3, start=1, end=10, theme_config=theme_config, name="Categories",)

data = pn.bind(get_data, n_colors)
colors = pn.bind(get_categorical_palette, primary_color, n_colors)
categorical_plot = pn.bind(get_categorical_plot, df=data, colors=colors)

bokeh_theme = pn.bind(get_bokeh_theme, theme, font_family)
categorical_pane=pn.pane.HoloViews(categorical_plot, theme=bokeh_theme, sizing_mode="stretch_width")

continous_plot = pn.bind(get_continous_plot, color=primary_color)
continous_pane =pn.pane.HoloViews(continous_plot, theme=bokeh_theme, sizing_mode="stretch_width")

action_row = pn.Row(paper, primary_color, n_colors, font_family, pn.HSpacer(), theme)
colors_out = pmu.TextInput(value=pn.bind(lambda c: ", ".join(c), colors), name="Categorical Colors", disabled=True, theme_config=theme_config)
button_out = pmu.Button(name="Click Me", color="primary", theme_config=theme_config)
column_out = pn.Column(colors_out, button_out, LORUM_IPSUM)

@pn.depends(paper)
def get_layout(paper: bool):
    if paper:
        return pn.Column(
            pmu.Paper(action_row),
            pmu.Paper(categorical_pane),
            pmu.Paper(continous_pane),
            pmu.Paper(column_out),
            max_width=800
        )
    else:
        return pn.Column(
            action_row,
            categorical_pane,
            continous_pane,
            column_out,
            max_width=800
        )

pn.panel(get_layout).servable()
