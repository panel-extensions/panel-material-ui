# Altair and Vega-Lite

Panel Material UI has integrated theming support for Altair and Vega-Lite plots. This means that the plots will automatically adapt to the active theme, including respecting the primary color, the font family, and toggling between dark and light mode.

## Basic Theming

To enable this behavior, you can either use the `Page` component or include a `ThemeToggle` in your app. Altair plots will automatically respect the current Material-UI theme.

```{pyodide}
import panel as pn
import panel_material_ui as pmu
import altair as alt
from vega_datasets import data

pn.extension("vega")

df = data.cars()
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

chart = alt.Chart(df).mark_circle(size=60).encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color='Origin:N',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).properties(
    width=600,
    height=400
).interactive()

pmu.Container(
    toggle,
    pn.pane.Vega(chart, sizing_mode="stretch_width"),
    width_option="md"
).preview()
```

## Palettes & Color Schemes

When visualizing categorical data, each color should be visibly distinct from all the other colors, not nearby in color space, to make each category separately visible.

You can find existing Altair color schemes in the [Vega documentation](https://vega.github.io/vega/docs/schemes/) and use them with the `scale()` method.

### Categorical Color Palettes

If you want to create categorical color maps aligned with your Material theme, you can use the `pmu.theme.generate_palette` function.

```{pyodide}
import altair as alt
import panel_material_ui as pmu
import panel as pn
from vega_datasets import data

pn.extension("vega")

df = data.iris()

primary_color = "#0072B2"
colors = pmu.theme.generate_palette(primary_color)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

chart = alt.Chart(df).mark_circle(size=100).encode(
    x='petalWidth:Q',
    y='petalLength:Q',
    color=alt.Color('species:N').scale(range=colors),
    tooltip=['species', 'petalWidth', 'petalLength']
).properties(
    width=600,
    height=400
).interactive()

pmu.Container(
    toggle,
    pn.pane.Vega(chart, sizing_mode="stretch_width"),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

### Continuous Color Scales

Similarly, you can use the `pmu.theme.linear_gradient` function to get a color scale aligned with your Material theme for continuous data.

```{pyodide}
import altair as alt
import panel_material_ui as pmu
import panel as pn
from vega_datasets import data

pn.extension("vega")

df = data.cars()
primary_color = "#0072B2"
cmap = pmu.theme.linear_gradient("#ffffff", primary_color, n=10)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

chart = alt.Chart(df).mark_circle(size=60).encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color=alt.Color('Acceleration:Q').scale(range=cmap),
    tooltip=['Name', 'Horsepower', 'Miles_per_Gallon', 'Acceleration']
).properties(
    width=600,
    height=400
).interactive()

pmu.Container(
    toggle,
    pn.pane.Vega(chart, sizing_mode="stretch_width"),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).servable()
```

## Advanced Theming with Altair Themes

Altair provides a powerful theming system that can be combined with Panel Material UI themes. You can use `alt.theme.enable()` to set global chart themes, or create custom themes that align with your Material design.

### Using Built-in Altair Themes

```{pyodide}
import altair as alt
import panel_material_ui as pmu
import panel as pn
from vega_datasets import data

df = data.stocks()
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

@pn.depends(toggle.param.dark_theme)
def chart(dark_theme):
    if dark_theme:
        alt.theme.enable('dark')
    else:
        alt.theme.enable('powerbi')

    chart = alt.Chart(df).mark_line().encode(
        x='date:T',
        y='price:Q',
        color='symbol:N'
    ).properties(
        width=600,
        height=300
    ).interactive()
    return chart

pmu.Container(
    toggle,
    pn.pane.Vega(chart, sizing_mode="stretch_width"),
    width_option="md"
).servable()
```

### Creating Custom Material-Aligned Themes

You can create custom Altair themes that automatically align with your Material UI theme colors:

```{pyodide}
import panel as pn
import panel_material_ui as pmu
import altair as alt
from vega_datasets import data
from typing import Optional

pn.extension("vega")

df = data.cars()
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

chart = alt.Chart(df).mark_circle(size=60).encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color='Origin:N',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).properties(
    width=600,
    height=400
)

def configure(
    chart: alt.Chart,
    primary: str = "#1976d2",
    primary_dark: str | None = None,
    dark_theme: bool = True,
) -> alt.Chart:
    """
    Configure Altair chart with Material UI theme colors.

    Parameters
    ----------
    chart : alt.Chart
        The Altair chart to configure
    primary : str, default "#1976d2"
        Primary color for chart elements
    primary_dark : str, default "#115293"
        Darker variant of primary color for accents
    dark_theme : bool, default True
        Whether to use dark theme styling

    Returns
    -------
    alt.Chart
        Configured chart with Material UI theming
    """
    font = "Roboto, Helvetica, Arial, sans-serif"
    font_color = "rgb(255, 255, 255)" if dark_theme else "rgba(0, 0, 0, 0.87)"
    primary = primary_dark if (primary_dark and dark_theme) else primary
    colors = pmu.theme.generate_palette(primary, n_colors=5)
    return chart.configure(
        font=font,
        background="transparent"
    ).configure_view(
        stroke="transparent"
    ).configure_mark(
        color=primary,
        filled=True,
        tooltip=True,
    ).configure_axis(
        labelColor=font_color,
        titleColor=font_color,
        tickColor=font_color,
        gridColor=font_color,
        gridOpacity=0.33,
        domainColor=font_color,
    ).configure_legend(
        labelColor=font_color,
        titleColor=font_color,
    ).configure_title(
        color=font_color
    ).configure_range(
        # category=colors  # Use generated palette for categorical colors
    ).interactive()

# Define theme colors
# orsted blue
primary_color = "#788A12"
primary_dark_color = "#E38DE6"

pmu.Container(
    toggle,
    pn.pane.Vega(
        pn.bind(
            configure,
            chart,
            primary=primary_color,
            primary_dark=primary_dark_color,
            dark_theme=toggle.param.dark_theme,
        ),
        sizing_mode="stretch_width"
    ),
    """Lorum ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
    theme_config={
        "palette": {
            "primary": {
                "main": primary_color,
                "dark": primary_dark_color
            }
        }
    },
    width_option="md"
).servable()
```

## Interactive Charts with Material UI Controls

You can combine Altair's interactivity with Panel Material UI components for a cohesive user experience:

```{pyodide}
import altair as alt
import panel as pn
import panel_material_ui as pmui
from vega_datasets import data

df = data.cars()

color_picker = pmui.ColorPicker(
    name="Primary Color",
    value="#d219cb",
    sizing_mode="stretch_width",
)

def create_categorical_chart(color):
    return alt.Chart(df).mark_circle(size=80).encode(
        x='Horsepower:Q',
        y='Miles_per_Gallon:Q',
        color=alt.Color('Cylinders:O').scale(
            range=pmui.theme.generate_palette(color, n_colors=5)
        ),
        tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon', 'Cylinders']
    ).properties(
        width=600, height=400
    ).interactive()

def create_theme_config(color):
    return {
        "palette": {
            "primary": {
                "main": color,
            },
        }
    }

chart = pn.bind(create_categorical_chart, color=color_picker)
theme_config = pn.bind(create_theme_config, color=color_picker)

pmui.Page(
    title="Altair with Panel Material UI",
    sidebar=[pn.pane.PNG("https://altair-viz.github.io/_static/altair-logo-light.png", align="center"), color_picker],
    main=[pmui.Container(pn.pane.Vega(chart, sizing_mode="stretch_width"), width_option="lg", sx={"marginTop": "20px"})],
    theme_config=theme_config,
).servable()
```

## Best Practices

1. **Theme Synchronization**: When toggling the theme, your Altair charts will automatically adapt to light/dark mode changes.
2. **Consistent Color Schemes**: Use `pmu.theme.generate_palette()` and `pmu.theme.linear_gradient()` to ensure your Altair charts match your Material UI theme.
3. **Responsive Design**: Set chart properties like `width="container"` and use `sizing_mode="stretch_width"` in the Vega pane for responsive behavior.
4. **Tooltips**: Set tooltips with the `tooltip` encoding.
5. Make the axes interactive with the `.interactive()` method.
4. **Custom Themes**: Create reusable Altair themes that align with your Material Design system using `alt.theme.register()`.


Remember that Altair theme changes via `alt.theme.enable()` are global and will affect all subsequent charts unless explicitly changed or overridden.
