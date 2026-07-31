# Vega and Vega-Lite Specifications

Panel Material UI has integrated theming support for Vega and Vega-Lite specifications when using the `Vega` pane. This means that your charts will automatically adapt to the active theme, including respecting the primary color, font family, and toggling between dark and light mode.

## Basic Theming

To enable this behavior, you can either use the `Page` component or include a `ThemeToggle` in your app. Vega specifications will automatically respect the current Material-UI theme.

```{pyodide}
import panel as pn
import panel_material_ui as pmu

pn.extension("vega")

toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

vega_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/cars.json"},
    "mark": {"type": "circle", "size": 60},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {"field": "Origin", "type": "nominal"},
        "tooltip": [
            {"field": "Name", "type": "nominal"},
            {"field": "Origin", "type": "nominal"},
            {"field": "Horsepower", "type": "quantitative"},
            {"field": "Miles_per_Gallon", "type": "quantitative"}
        ]
    },
    "width": 600,
    "height": 400
}

pmu.Container(
    toggle,
    pn.pane.Vega(vega_spec, sizing_mode="stretch_width"),
    width_option="md"
).preview()
```

## Palettes & Color Schemes

When visualizing categorical data, each color should be visibly distinct from all the other colors, not nearby in color space, to make each category separately visible.

You can find existing Vega color schemes in the [Vega documentation](https://vega.github.io/vega/docs/schemes/) and use them with the `scale` property.

### Categorical Color Palettes

If you want to create categorical color maps aligned with your Material theme, you can use the `pmu.theme.generate_palette` function and apply it directly to your Vega specification.

```{pyodide}
import panel as pn
import panel_material_ui as pmu

pn.extension("vega")

primary_color = "#6200ea"
colors = pmu.theme.generate_palette(primary_color)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

vega_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/iris.json"},
    "mark": {"type": "circle", "size": 100},
    "encoding": {
        "x": {"field": "petalWidth", "type": "quantitative"},
        "y": {"field": "petalLength", "type": "quantitative"},
        "color": {
            "field": "species",
            "type": "nominal",
            "scale": {"range": colors}
        },
        "tooltip": [
            {"field": "species", "type": "nominal"},
            {"field": "petalWidth", "type": "quantitative"},
            {"field": "petalLength", "type": "quantitative"}
        ]
    },
    "width": 600,
    "height": 400
}

pmu.Container(
    toggle,
    pn.pane.Vega(vega_spec, sizing_mode="stretch_width"),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

### Continuous Color Scales

Similarly, you can use the `pmu.theme.linear_gradient` function to get a color scale aligned with your Material theme for continuous data.

```{pyodide}
import panel as pn
import panel_material_ui as pmu

pn.extension("vega")

primary_color = "#6200ea"
cmap = pmu.theme.linear_gradient("#ffffff", primary_color, n=10)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

vega_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/cars.json"},
    "mark": {"type": "circle", "size": 60},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {
            "field": "Acceleration",
            "type": "quantitative",
            "scale": {"range": cmap}
        },
        "tooltip": [
            {"field": "Name", "type": "nominal"},
            {"field": "Horsepower", "type": "quantitative"},
            {"field": "Miles_per_Gallon", "type": "quantitative"},
            {"field": "Acceleration", "type": "quantitative"}
        ]
    },
    "width": 600,
    "height": 400
}

pmu.Container(
    toggle,
    pn.pane.Vega(vega_spec, sizing_mode="stretch_width"),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

## Advanced Theming with Configuration

Vega-Lite provides a powerful configuration system that can be combined with Panel Material UI themes. You can add a `config` object to your specification to customize the appearance.

### Using Built-in Vega Themes

```{pyodide}
import panel as pn
import panel_material_ui as pmu

pn.extension("vega")

toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

@pn.depends(toggle.param.dark_theme)
def create_themed_chart(dark_theme):
    theme = "dark" if dark_theme else "default"

    vega_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/stocks.csv"},
        "mark": "line",
        "encoding": {
            "x": {"field": "date", "type": "temporal"},
            "y": {"field": "price", "type": "quantitative"},
            "color": {"field": "symbol", "type": "nominal"}
        },
        "width": 600,
        "height": 300,
        "config": {
            "theme": theme
        }
    }
    return vega_spec

pmu.Container(
    toggle,
    pn.pane.Vega(create_themed_chart, sizing_mode="stretch_width"),
    width_option="md"
).preview()
```

### Creating Custom Material-Aligned Configurations

You can create comprehensive Vega configurations that automatically align with your Material UI theme colors:

```{pyodide}
import panel as pn
import panel_material_ui as pmu

pn.extension("vega")

toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

def create_material_config(primary_color="#1976d2", dark_theme=False):
    """Create a Vega-Lite config aligned with Material Design."""
    font_family = "Roboto, Helvetica, Arial, sans-serif"
    colors = pmu.theme.generate_palette(primary_color)

    # Theme-specific colors
    if dark_theme:
        background = "transparent"
        text_color = "white"
        grid_color = "#555555"
        domain_color = "#777777"
    else:
        background = "transparent"
        text_color = "#424242"
        grid_color = "#e0e0e0"
        domain_color = "#bdbdbd"

    return {
        "background": background,
        "font": font_family,
        "axis": {
            "labelFont": font_family,
            "labelFontSize": 12,
            "labelColor": text_color,
            "titleFont": font_family,
            "titleFontSize": 14,
            "titleColor": text_color,
            "titleFontWeight": 500,
            "grid": True,
            "gridColor": grid_color,
            "gridOpacity": 0.5,
            "domain": False,
            "ticks": False,
            "labelPadding": 8,
            "titlePadding": 16
        },
        "legend": {
            "labelFont": font_family,
            "labelFontSize": 12,
            "labelColor": text_color,
            "titleFont": font_family,
            "titleFontSize": 14,
            "titleColor": text_color,
            "titleFontWeight": 500,
            "symbolSize": 80,
            "symbolStrokeWidth": 0,
            "cornerRadius": 4
        },
        "title": {
            "font": font_family,
            "fontSize": 18,
            "fontWeight": 500,
            "color": text_color,
            "anchor": "start",
            "align": "left",
            "offset": 20
        },
        "view": {
            "stroke": "transparent",
            "strokeWidth": 0
        },
        "range": {
            "category": colors,
            "diverging": pmu.theme.linear_gradient("#ffffff", primary_color, n=9),
            "heatmap": pmu.theme.linear_gradient("#ffffff", primary_color, n=9),
            "ordinal": colors,
            "ramp": pmu.theme.linear_gradient("#ffffff", primary_color, n=9)
        },
        "mark": {
            "color": primary_color,
            "tooltip": True
        },
        "arc": {"fill": primary_color},
        "area": {"fill": primary_color, "fillOpacity": 0.7},
        "bar": {"fill": primary_color},
        "circle": {"fill": primary_color, "stroke": primary_color},
        "line": {"stroke": primary_color, "strokeWidth": 2},
        "point": {"fill": primary_color, "stroke": primary_color, "size": 60},
        "rect": {"fill": primary_color},
        "square": {"fill": primary_color},
        "tick": {"fill": primary_color},
        "trail": {"fill": primary_color}
    }

@pn.depends(toggle.param.dark_theme)
def create_configured_chart(dark_theme):
    primary_color = "#e91e63"
    config = create_material_config(primary_color, dark_theme)

    vega_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/cars.json"},
        "mark": {"type": "circle", "size": 60},
        "encoding": {
            "x": {"field": "Horsepower", "type": "quantitative"},
            "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
            "color": {"field": "Origin", "type": "nominal"},
            "tooltip": [
                {"field": "Name", "type": "nominal"},
                {"field": "Origin", "type": "nominal"},
                {"field": "Horsepower", "type": "quantitative"},
                {"field": "Miles_per_Gallon", "type": "quantitative"}
            ]
        },
        "width": 600,
        "height": 400,
        "config": config
    }
    return vega_spec

primary_color = "#e91e63"

pmu.Container(
    toggle,
    pn.pane.Vega(create_configured_chart, sizing_mode="stretch_width"),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

## Interactive Charts with Material UI Controls

You can combine Vega's interactivity with Panel Material UI components for a cohesive user experience:

```{pyodide}
import panel as pn
import panel_material_ui as pmu

pn.extension("vega")

# Material UI controls
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})
color_picker = pmu.ColorPicker(
    name="Primary Color",
    value="#1976d2",
    width=200
)

origin_select = pmu.Select(
    name="Origin Filter",
    value="All",
    options=["All", "Europe", "Japan", "USA"],
    width=200
)

def create_interactive_chart(primary_color, origin_filter, dark_theme):
    """Create an interactive Vega chart with Material UI theming."""
    colors = pmu.theme.generate_palette(primary_color)
    config = create_material_config(primary_color, dark_theme)

    # Data filtering
    data_url = "https://raw.githubusercontent.com/vega/vega/master/docs/data/cars.json"
    transform = []
    if origin_filter != "All":
        transform.append({"filter": f"datum.Origin == '{origin_filter}'"})

    vega_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "data": {"url": data_url},
        "transform": transform,
        "mark": {"type": "circle", "size": 80},
        "encoding": {
            "x": {"field": "Horsepower", "type": "quantitative"},
            "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
            "color": {
                "field": "Cylinders",
                "type": "ordinal",
                "scale": {"range": colors}
            },
            "tooltip": [
                {"field": "Name", "type": "nominal"},
                {"field": "Origin", "type": "nominal"},
                {"field": "Horsepower", "type": "quantitative"},
                {"field": "Miles_per_Gallon", "type": "quantitative"},
                {"field": "Cylinders", "type": "ordinal"}
            ]
        },
        "width": 600,
        "height": 400,
        "config": config
    }
    return vega_spec

chart = pn.bind(
    create_interactive_chart,
    primary_color=color_picker,
    origin_filter=origin_select,
    dark_theme=toggle.param.dark_theme
)

theme_config = pn.bind(
    lambda color: {"palette": {"primary": {"main": color}}},
    color=color_picker
)

pmu.Container(
    pmu.Row(toggle, color_picker, origin_select, styles={"margin-bottom": "20px"}),
    pn.pane.Vega(chart, sizing_mode="stretch_width"),
    theme_config=theme_config,
    width_option="lg"
).preview()
```

## Working with Selections

The Vega pane supports Vega-Lite selections, which can be combined with Panel Material UI components for rich interactivity:

```{pyodide}
import panel as pn
import panel_material_ui as pmu
import pandas as pd

pn.extension("vega")

toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

# Create a Vega-Lite specification with brush selection
vega_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": {"url": "https://raw.githubusercontent.com/vega/vega/master/docs/data/cars.json"},
    "params": [{
        "name": "brush",
        "select": {"type": "interval"}
    }],
    "mark": {"type": "circle", "size": 60},
    "encoding": {
        "x": {"field": "Horsepower", "type": "quantitative"},
        "y": {"field": "Miles_per_Gallon", "type": "quantitative"},
        "color": {
            "condition": {
                "param": "brush",
                "field": "Origin",
                "type": "nominal"
            },
            "value": "lightgray"
        },
        "tooltip": [
            {"field": "Name", "type": "nominal"},
            {"field": "Origin", "type": "nominal"},
            {"field": "Horsepower", "type": "quantitative"},
            {"field": "Miles_per_Gallon", "type": "quantitative"}
        ]
    },
    "width": 600,
    "height": 400,
    "config": create_material_config("#1976d2", False)
}

vega_pane = pn.pane.Vega(vega_spec, debounce=10, sizing_mode="stretch_width")

def selection_info(selection):
    """Display information about the current selection."""
    if not selection:
        return pmu.Alert("No selection made. Drag to select points!", severity="info")

    info_text = "**Selection:**\\n"
    for field, values in selection.items():
        info_text += f"- {field}: {values[0]:.2f} to {values[1]:.2f}\\n"

    return pmu.Alert(info_text, severity="success")

info_panel = pn.bind(selection_info, vega_pane.selection.param.brush)

pmu.Container(
    toggle,
    pmu.Row(
        vega_pane,
        pmu.Column(
            pmu.Typography("## Selection Info", variant="h6"),
            info_panel,
            width_option="sm"
        ),
        styles={"gap": "20px"}
    ),
    width_option="xl"
).preview()
```

## Best Practices

1. **Consistent Color Schemes**: Use `pmu.theme.generate_palette()` and `pmu.theme.linear_gradient()` to ensure your Vega charts match your Material UI theme.

2. **Responsive Design**: Set chart properties like `"width": "container"` and use `sizing_mode="stretch_width"` in the Vega pane for responsive behavior.

3. **Theme Synchronization**: When using `ThemeToggle`, create reactive functions that adapt the Vega configuration to light/dark mode changes.

4. **Comprehensive Configuration**: Use the `config` object to create consistent theming across all chart elements including axes, legends, and marks.

5. **Interactive Integration**: Combine Vega selections with Panel Material UI components for rich, themed dashboards.

6. **Font Consistency**: Always specify the Material Design font stack in your configuration: `"Roboto, Helvetica, Arial, sans-serif"`.

7. **Transparent Backgrounds**: Use `"background": "transparent"` to ensure charts integrate seamlessly with your Material UI containers.

Remember that Vega-Lite configurations are applied at the specification level and will only affect the specific chart, making them ideal for fine-grained theming control.
