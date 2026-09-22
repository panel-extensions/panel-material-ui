```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `ColorMap` widget selects a colormap from a dictionary of named palettes. Each option is displayed as a color gradient, making it useful for choosing a consistent palette for a plot or data application.

Discover more about interactive widgets in the [Panel interactivity guides](https://panel.holoviz.org/how_to/interactivity/index.html), or learn about [callbacks and links](https://panel.holoviz.org/how_to/links/index.html) and [declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters

For details on other options for customizing the component, see the [Panel Material UI customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`options`** (dict): A dictionary mapping palette names to lists of colors. The colors can be CSS color strings such as hexadecimal values.
* **`value`** (object): The currently selected palette as its list of colors.
* **`value_name`** (str): The name of the currently selected palette. Setting this parameter selects the corresponding option.
* **`ncols`** (int): The number of columns used to lay out swatches in each palette.
* **`swatch_height`** (int): The height of each color swatch in pixels.
* **`swatch_width`** (int): The width of each color swatch in pixels.

##### Display

* **`disabled`** (bool): Whether the widget is interactive.
* **`error_state`** (bool): Whether to display the widget in an error state.
* **`helper_text`** (str): Text displayed below the widget.
* **`label`** (str): The title displayed for the widget.
* **`description`** (str): Tooltip text displayed when hovering over the widget.

##### Styling

* **`sx`** (dict): Component-level styling API for fine-grained customization.
* **`theme_config`** (dict): Theming API for consistent design system integration.

### Basic Usage

Pass a dictionary of named palettes to `options`. Each palette is rendered as a visible gradient in the menu:


```python
palettes = {
    "Sunset": ["#fff7bc", "#fec44f", "#d95f0e", "#993404"],
    "Ocean": ["#f7fbff", "#6baed6", "#2171b5", "#08306b"],
    "Forest": ["#f7fcf5", "#74c476", "#238b45", "#00441b"],
}

color_map = pmui.ColorMap(label="Palette", options=palettes, value_name="Ocean", height=200)
color_map
```

The selected palette is available through both `value_name` and `value`:


```python
color_map.value_name, color_map.value
```

### Swatch Layout and Sizing

Use `ncols` to arrange the colors in multiple columns. `swatch_width` and `swatch_height` control the size of each color swatch:


```python
pmui.ColorMap(
    label="Large swatches",
    options=palettes,
    value_name="Sunset",
    ncols=2,
    swatch_width=140,
    swatch_height=28,
    height=250
)
```

### Value and Value Name

`value_name` is convenient when working with named palettes, while `value` exposes the actual list of colors. Updating either representation keeps the other in sync:


```python
color_map.value_name = "Forest"
color_map.value
```


```python
color_map.value = palettes["Sunset"]
color_map.value_name
```

### Disabled, Error, Helper Text, and Description

`disabled` prevents selection. Use `error_state` and `helper_text` to communicate validation state, and `description` to provide additional context in a tooltip:


```python
pmui.Column(
    pmui.ColorMap(
        label="Required palette",
        options=palettes,
        value_name="Ocean",
        error_state=True,
        helper_text="Select a palette before continuing.",
        description="The palette used for the data visualization.",
    ),
    pmui.ColorMap(label="Read-only palette", options=palettes, value_name="Forest", disabled=True),
)
```

### Example: Reactive Palette Preview

The selected palette can drive other components with `pn.bind`. This small example displays the selected palette as a deterministic HTML gradient and reports its name:


```python
def palette_preview(name):
    colors = palettes.get(name, [])
    gradient = ", ".join(colors)
    return pn.pane.HTML(
        f"<div style='height:48px;border-radius:4px;background:linear-gradient(90deg, {gradient})'></div>"
        f"<p>Selected palette: <b>{name}</b></p>"
    )

preview = pn.bind(palette_preview, color_map.param.value_name)
pmui.Column(color_map, preview)
```

### API Reference

Show all parameters and their current values:


```python
pmui.ColorMap(label="Palette", options=palettes).api(jslink=True)
```

### References

* [Panel ColorMap documentation](https://panel.holoviz.org/reference/widgets/ColorMap.html)
* [Panel interactivity guides](https://panel.holoviz.org/how_to/interactivity/index.html)
* [Panel Material UI customization guides](https://panel-material-ui.holoviz.org/customization/index.html)
