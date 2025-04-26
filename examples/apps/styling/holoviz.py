# Default options

import panel as pn
import panel_material_ui as pmu
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
from bokeh.models import HoverTool

pn.extension(sizing_mode="stretch_width")
pmu.Paper.margin = 10

# def disable_logo(plot, element):
#     plot.state.toolbar.logo = None
# hv.plotting.bokeh.ElementPlot.hooks.append(disable_logo)


def get_hook(color: str = "salmon"):
    def hook(plot, element, color=color):

        fig = plot.handles["plot"]
        toolbar = fig.toolbar
        toolbar.logo = None
        plot.state.toolbar.autohide = True
        plot.state.toolbar_location = "above"
        fig.add_tools("fullscreen")

        css = f"""
.bk-right.bk-active, .bk-above.bk-active {{
    --highlight-color: {color} !important;
}}
"""
        toolbar.stylesheets = [css]

    return hook


LORUM_IPSUM = """\
**Lorem Ipsum** is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the
industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type
and scrambled it to make a type specimen book"""

# General Code: COULD BE PART OF panel_material_ui.theme module?


@pn.cache
def get_categorical_palette(color: str, n_colors: int = 3) -> list[str]:
    hex_color = color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    hues = np.linspace(0, 1, int(n_colors) + 1)[:-1]
    hues += h
    hues %= 1
    hues -= hues.astype(int)
    rgb_palette = [colorsys.hls_to_rgb(h_i, l, s) for h_i in hues]
    hex_palette = [
        "#{:02x}{:02x}{:02x}".format(int(r_i * 255), int(g_i * 255), int(b_i * 255))
        for r_i, g_i, b_i in rgb_palette
    ]
    return hex_palette


def get_continous_color_map(color: str):
    return mcolors.LinearSegmentedColormap.from_list(
        "custom_cmap", ["white", color], N=256
    )


def get_bokeh_theme(dark_theme: bool, font_family: str = "Helvetica"):
    if dark_theme:
        json = BOKEH_DARK
    else:
        json = BOKEH_LIGHT

    json = deepcopy(json)
    for key1, val1 in json.items():
        for key2, val2 in val1.items():
            for key3 in val2:
                if key3.endswith("_font"):
                    json[key1][key2][key3] = font_family

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
            "fontFamily": (font_family,),
        },
    }


@pn.cache
def get_data(n_categories: int, n_rows=100):
    x = np.random.rand(n_rows)
    y = np.random.rand(n_rows)

    categories = [f"Category {i+1}" for i in range(n_categories)]
    category = np.random.choice(categories, n_rows)

    dataframe = pd.DataFrame({"x": x, "y": y, "category": category})

    return dataframe


def get_hover_tool(
    tooltips: list[tuple], color, font_family: str = "Roboto", font_size="15px"
):
    html = f"""<div style="font-family: {font_family};font-size: {font_size};margin-bottom: 5px;">"""
    for item in tooltips:
        html += f"""<em style="color:{color}">{item[0]}:</em><span>&nbsp;{item[1]}</span><br/>"""
    html += """</div>"""

    return HoverTool(tooltips=html)


def get_categorical_plot(df, colors, color, font_family="Roboto"):
    hover_tool = get_hover_tool(
        [("Category", "@category"), ("X", "@x"), ("Y", "@y")],
        color=color,
        font_family=font_family,
    )

    plot = df.hvplot.scatter(
        x="x",
        y="y",
        size=75,
        by="category",
        title="Categorical Plot",
        tools=[hover_tool],
        color=hv.Cycle(colors),
    )
    hook = get_hook(color)
    plot.opts(hooks=[hook])
    return plot


def get_continous_plot(color="#9c27b0", font_family: str = "Roboto"):
    np.random.seed(42)
    data = pd.DataFrame(
        {
            "x": np.random.rand(100),
            "y": np.random.rand(100),
            "value": np.random.rand(100) * 100,
        }
    )
    custom_cmap = get_continous_color_map(color)
    hover_tool = get_hover_tool(
        [("Index", "$index"), ("X", "@x"), ("Y", "@y")],
        color=color,
        font_family=font_family,
    )

    hook = get_hook(color)
    return data.hvplot.scatter(
        x="x",
        y="y",
        c="value",
        size=75,
        cmap=custom_cmap,
        colorbar=True,
        title="Continuous Plot",
        tools=[hover_tool],
        legend_position="bottom_right",  # Does not work!
    ).opts(hooks=[hook])


paper = pmu.Checkbox(value=True, name="Paper", sizing_mode="fixed", align="center")
theme = pmu.ThemeToggle(sizing_mode="fixed", align="center")
font_family = pmu.Select(name="Font", options=["Roboto", "Impact", "Palatino Linotype"])

primary_color = pmu.ColorPicker(
    value="#9c27b0",
    name="Primary Color",
)
theme_config = pn.bind(get_theme_config, primary_color, font_family)
n_colors = pmu.IntSlider(
    value=3,
    start=1,
    end=10,
    theme_config=theme_config,
    name="Categories",
)

data = pn.bind(get_data, n_colors)
colors = pn.bind(get_categorical_palette, primary_color, n_colors)
categorical_plot = pn.bind(
    get_categorical_plot,
    df=data,
    colors=colors,
    color=primary_color,
    font_family=font_family,
)

bokeh_theme = pn.bind(get_bokeh_theme, theme, font_family)
categorical_pane = pn.pane.HoloViews(
    categorical_plot, theme=bokeh_theme, sizing_mode="stretch_width"
)

continous_plot = pn.bind(
    get_continous_plot, color=primary_color, font_family=font_family
)
continous_pane = pn.pane.HoloViews(
    continous_plot, theme=bokeh_theme, sizing_mode="stretch_width"
)

action_row = pn.Row(paper, primary_color, n_colors, font_family, pn.HSpacer(), theme)
colors_out = pmu.TextInput(
    value=pn.bind(lambda c: ", ".join(c), colors),
    name="Categorical Colors",
    disabled=True,
    theme_config=theme_config,
)
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
            max_width=800,
        )
    else:
        return pn.Column(
            action_row, categorical_pane, continous_pane, column_out, max_width=800
        )


pn.panel(get_layout).servable()
