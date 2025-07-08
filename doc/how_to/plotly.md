# Plotly Theming

Panel Material UI provides integrated theming support for Plotly, which is applied automatically.

## Basic Usage

The theme will be applied automatically:

```{pyodide}
import panel as pn
import panel_material_ui as pmui
import plotly.express as px

pn.extension("plotly")

df = px.data.iris()

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species",
    height=400
)

pmui.Container(
    plot, width_option="md"
).preview(height=500)
```

and will automatically switch when in dark mode:

```{pyodide}
import panel as pn
import panel_material_ui as pmui
import plotly.express as px

pn.extension("plotly")

df = px.data.iris()

toggle = pmui.ThemeToggle(styles={"margin-left": "auto"}, value=True)

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species",
    height=400
)

pmui.Container(
    toggle, plot, dark_theme=True, width_option="md"
).preview(height=500)
```

## Color Palettes & Scales

Plotly provides built-in [categorical color sequences](https://plotly.com/python/discrete-color/) and [continuous color scales](https://plotly.com/python/builtin-colorscales/).

In addition, Panel Material UI provides utilities to generate categorical color palettes and continuous color scales that align with Material Design and your chosen color theme.

### Categorical Colors

In order to align the Material UI theming with the plot color sequence you can generate a palette using the `pmui.theme.generate_palette` utility and provide it using the `color_discrete_sequence`:

```{pyodide}
import panel as pn
import plotly.express as px
import panel_material_ui as pmui

pn.extension("plotly")

df = px.data.iris()

primary_color = "#4099da"

# Generate colors using existing theme function
colors = pmui.theme.generate_palette(primary_color, n_colors=3)

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species",
    height=400,
    color_discrete_sequence=colors
)

toggle = pmui.ThemeToggle(styles={"margin-left": "auto"}, value=False)

pmui.Container(
    toggle,
    plot,
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview(height=500)
```

:::{note}
When using Plotly Figure directly you can provide a discrete color sequence via the `colorway` argument of the `layout` property, i.e.:

```python
go.Figure(layout={'colorway': ...})
```
:::

### Continuous Colors

Create continuous color scales using the `pmui.theme.linear_gradient` function for continuous data visualization:

```{pyodide}
import panel as pn
import plotly.express as px
import panel_material_ui as pmui

pn.extension("plotly")

df = px.data.iris()
primary_color = "#4099da"

colorscale = pmui.theme.linear_gradient("#ffffff", primary_color, n=256)

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="petal_length",
    height=400,
    color_continuous_scale=colorscale
)

toggle = pmui.ThemeToggle(styles={"margin-left": "auto"}, value=False)

pmui.Container(
    toggle,
    plot,
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview(height=500)
```
