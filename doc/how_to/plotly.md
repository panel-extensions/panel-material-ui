# Plotly

Panel Material UI provides integrated theming support for Plotly. This includes built-in `"pmui_light"` and `"pmui_dark"` [Plotly templates](https://plotly.com/python/templates/).

## Available Templates

When you import `panel_material_ui`, Plotly templates are automatically registered for immediate use:

- `"pmui_light"` - Light theme (set as default)
- `"pmui_dark"` - Dark theme

Both templates follow Material Design principles with proper typography, spacing, and color schemes.

## Basic Usage

The `"pmui_light"` template is applied by default.

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
).preview()
```

You may also apply the `"pmui_dark"` template.

```{pyodide}
import panel as pn
import panel_material_ui as pmui
import plotly.express as px

pn.extension("plotly")

df = px.data.iris()

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species",
    height=400, template="pmui_dark"
)

pmui.Container(
    plot, width_option="md"
).preview()
```

## Reactive Theme Switching

Create plots that automatically respond to theme changes by using the `update_template` function with Panel's reactive system:

```{pyodide}
import panel as pn
import panel_material_ui as pmui
import plotly.express as px
import plotly.io as pio

pn.extension("plotly")

# Create sample data and plot
df = px.data.iris()

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species",
    height=400
)

toggle = pmui.ThemeToggle(styles={"margin-left": "auto"})

pmui.Container(
    toggle,
    pn.pane.Plotly(
        pn.bind(pmui.plotly.update_template, plot, toggle)
    ),
    width_option="md"
).preview()
```

## Advanced Configuration

If you want to customize the templates or change the default template, you can explicitly call `register_pmui_templates()`:

```python
pmui.plotly.register_pmui_templates(
    primary_color="#4099da",        # Blue for light and dark mode
)
```

For further control, you may specify `primary_color_dark` and/or `default` arguments.

```python
pmui.plotly.register_pmui_templates(
    primary_color="#4099da",        # Blue for light mode
    primary_color_dark="#644c76",   # Purple for dark mode
    default="plotly_white"          # Set plotly_white as default
)
```

## Color Palettes & Scales

Plotly provides built-in [categorical color sequences](https://plotly.com/python/discrete-color/) and [continuous color scales](https://plotly.com/python/builtin-colorscales/).

In addition, Panel Material UI provides utilities to generate categorical color palettes and continuous color scales that align with Material Design and your chosen color theme.

### Categorical Colors

Generate categorical color palettes aligned with your Material theme using the `pmui.theme.generate_palette` function:

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

toggle = pmui.ThemeToggle(styles={"margin-left": "auto"})

pmui.Container(
    toggle,
    pn.pane.Plotly(
        pn.bind(pmui.plotly.update_template, plot, toggle)
    ),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

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

toggle = pmui.ThemeToggle(styles={"margin-left": "auto"})

pmui.Container(
    toggle,
    pn.pane.Plotly(
        pn.bind(pmui.plotly.update_template, plot, toggle)
    ),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```
