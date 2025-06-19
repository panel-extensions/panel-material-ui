# Bokeh, hvPlot, and HoloViews

Panel Material UI has integrated theming support for Bokeh, hvPlot, and HoloViews. This means that the plots will automatically adapt to the active theme, including respecting the primary color, the font family, and toggling between dark and light mode.

## Basic Theming

To enable this behavior, you can either use the `Page` component or include a `ThemeToggle` in your app.

```{pyodide}
import panel as pn
import panel_material_ui as pmu
import pandas as pd
import hvplot.pandas

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/penguins/v1/penguins.csv")

toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

pmu.Container(
    toggle,
    df.hvplot.scatter(
        x="bill_length_mm", y="bill_depth_mm", by="species",
        height=400, responsive=True
    ),
    width_option="md"
).preview()
```

## Palettes & Colormaps

When visualizing categorical data, each color should be visibly distinct from all the other colors, not nearby in color space, to make each category separately visible.

You can find existing categorical color maps [here](https://colorcet.holoviz.org/user_guide/Categorical.html) and [here](https://holoviews.org/user_guide/Colormaps.html#categorical-colormaps).

### Categorical

If you want to create categorical color maps aligned with your Material theme, you can use the `pmu.utils.get_palette` function.

```{pyodide}
import pandas as pd
import hvplot.pandas
import panel_material_ui as pmu

df = pd.read_csv("https://datasets.holoviz.org/penguins/v1/penguins.csv")

primary_color = "#6200ea"
colors = pmu.theme.generate_palette(primary_color)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

pmu.Container(
    toggle,
    df.hvplot.scatter(
        x="bill_length_mm", y="bill_depth_mm", color="species",
        height=400, responsive=True, cmap=colors
    ),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

### Continuous

Similarly, you can use the `pmu.theme.linear_gradient` function to get a color map aligned with your Material theme.

```{pyodide}
import panel as pn
import panel_material_ui as pmu
import pandas as pd
import hvplot.pandas

df = pd.read_csv("https://datasets.holoviz.org/penguins/v1/penguins.csv")
primary_color = "#6200ea"

pn.extension()

cmap = pmu.theme.linear_gradient("#ffffff", primary_color, n=256)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

plot = df.hvplot.scatter(
    x="bill_length_mm", y="flipper_length_mm", c="body_mass_g",
    cmap=cmap, colorbar=True, height=400, responsive=True
).opts(
    backend_opts={
        'plot.toolbar.autohide': True
    },
    toolbar='above'
)

pmu.Container(
    toggle,
    plot,
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```
