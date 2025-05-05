from copy import deepcopy

import colorsys
import holoviews as hv
import hvplot.pandas
import numpy as np
import panel as pn
import panel_material_ui as pmu
import pandas as pd

pn.extension(sizing_mode="stretch_width")

pmu.Paper.margin = 10

LORUM_IPSUM = """\
**Lorem Ipsum** is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the
industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type
and scrambled it to make a type specimen book"""

# App Code

@pn.cache
def get_data(n_categories: int, n_rows=100):
    x = np.random.rand(n_rows)
    y = np.random.rand(n_rows)

    categories = [f"Category {i+1}" for i in range(n_categories)]
    category = np.random.choice(categories, n_rows)

    dataframe = pd.DataFrame({"x": x, "y": y, "category": category}).sort_values('category')

    return dataframe

def get_categorical_plot(df, palette):
    return df.hvplot.scatter(
        x="x",
        y="y",
        size=75,
        color="category",
        cmap=palette,
        height=350,
        responsive=True,
        title="Categorical Plot",
        tools=["fullscreen"],
        legend='top_right',
    ).opts(
        backend_opts={
            'plot.toolbar.autohide': True
        },
        toolbar='above'
    )

def get_continous_plot(color="#9c27b0"):
    np.random.seed(42)
    data = pd.DataFrame(
        {
            "x": np.random.rand(100),
            "y": np.random.rand(100),
            "value": np.random.rand(100) * 100,
        }
    )
    custom_cmap = pmu.theme.linear_gradient("#ffffff", color, n=256)
    return data.hvplot.scatter(
        x="x",
        y="y",
        c="value",
        size=75,
        cmap=custom_cmap,
        colorbar=True,
        height=350,
        responsive=True,
        title="Continuous Plot",
        tools=['fullscreen'],
    ).opts(
        backend_opts={
            'plot.toolbar.autohide': True
        },
        toolbar='above'
    )

# Configure theme
paper = pmu.Checkbox(
    value=True, label="Paper", sizing_mode="fixed", align="center"
)
font_family = pmu.Select(
    label="Font", options=["Roboto", "Impact", "Palatino Linotype"]
)
primary_color = pmu.ColorPicker(
    value="#9c27b0",
    name="Primary Color",
)

theme_config = {
    "palette": {
        "primary": {
            "main": primary_color,
        },
    },
    "typography": {
        "fontFamily": (font_family,),
    },
}

n_colors = pmu.IntSlider(
    value=3,
    start=1,
    end=10,
    name="Categories",
)

theme = pmu.ThemeToggle(sizing_mode="fixed", align="center")
action_row = pmu.Row(paper, primary_color, n_colors, font_family, pn.HSpacer(), theme)


# Set up  plots
data = pn.bind(get_data, n_colors)
palette = pn.bind(pmu.theme.generate_palette, primary_color, n_colors)

categorical_plot = hv.DynamicMap(pn.bind(
    get_categorical_plot,
    df=data,
    palette=palette
))

continous_plot = hv.DynamicMap(pn.bind(
    get_continous_plot, color=primary_color
))


colors_out = pmu.TextInput(
    value=pn.rx(', ').join(palette),
    name="Categorical Colors",
    disabled=True,
)
button_out = pmu.Button(label="Click Me", color="primary")
column_out = pmu.Column(colors_out, button_out, LORUM_IPSUM)

elevation = paper.rx().rx.where(1, 0)

pmu.Container(
    pmu.Paper(action_row, elevation=elevation),
    pmu.Paper(continous_plot, elevation=elevation),
    pmu.Paper(categorical_plot, elevation=elevation),
    pmu.Paper(column_out, elevation=elevation),
    theme_config=theme_config, width_option='md'
).servable()
