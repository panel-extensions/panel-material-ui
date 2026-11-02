```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `ColorPicker` widget provides an intuitive interface for selecting color values in your Panel applications.

#### Parameters:

For comprehensive customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`alpha`** (boolean): Whether to display input controls for a color's alpha (transparency) channel.
* **`disabled`** (boolean): Whether the widget is interactive or read-only.
* **`format`** (str): The format of the returned color value. Options include:
   - `hex`: Hexadecimal color value (e.g., '#ff0000')
   - `rgb`: RGB color value (e.g., 'rgb(255, 0, 0)')
   - `rgba`: RGBA color value with alpha channel (e.g., 'rgba(255, 0, 0, 0.5)')
   - `hsl`: HSL color value (e.g., 'hsl(0, 100%, 50%)')
   - `hsv`: HSV color value (e.g., 'hsv(0, 100%, 100%)')
* **`value`** (color): The current color value

##### Display

* **`color`** (str): The accent color of the color picker when active or focused.
* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The descriptive label displayed above the widget
* **`size`** (`Literal["small", "medium", "large"]`): The visual size of the input field
* **`variant`** (`Literal["filled", "outlined", "standard"]`): The visual style variant of the input field

##### Styling

- **`sx`** (dict): Component-level styling API for fine-grained customization.
- **`theme_config`** (dict): Theming API for consistent design system integration.

##### Aliases

For compatibility with existing Panel code, certain parameters have aliases:

- **`name`**: Alias for `label`
___

### Basic Usage

The `ColorPicker` displays a color preview square that, when clicked, opens your browser's native color selection interface. This provides a familiar and accessible way for users to choose colors:


```python
colorpicker = pmui.ColorPicker(label='Color Picker', value='#99ef78')

colorpicker
```

The `.value` returns the selected color as a hexadecimal RGB string:


```python
colorpicker.value
```

### Format

The `ColorPicker` supports multiple color format specifications to match your application's needs. Configure the `format` parameter to control how color values are represented when a user makes a selection:


```python
pmui.FlexBox(
  pmui.ColorPicker(label='HEX Color Picker', value='#99ef78', format='hex'),
  pmui.ColorPicker(label='RGB Color Picker', value='rgb(0, 24, 24)', format='rgb'),
  pmui.ColorPicker(label='RGBA Color Picker', value='rgba(90, 255, 120, 0.5)', format='rgba'),
  pmui.ColorPicker(label='HSL Color Picker', value='hsl(0, 100%, 50%)', format='hsl'),
  pmui.ColorPicker(label='HSV Color Picker', value='hsv(0, 100%, 100%)', format='hsv'),
)
```

### Alpha Channel

Enable transparency control by setting the `alpha` parameter to `True`. This adds an alpha channel slider to the color picker, allowing users to adjust the opacity of their selected color:


```python
pmui.ColorPicker(label='HEX Color Picker', value='#99ef78ff', alpha=True)
```

### Color Options

The `color` parameter allows you to visually distinguish the `ColorPicker` component when it's active or focused. This helps create a cohesive visual hierarchy in your application. Available color options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":


```python
pmui.FlexBox(
    *[pmui.ColorPicker(label=color, color=color, value='#f3f3f3') for color in pmui.ColorPicker.param.color.objects]
)
```

### Variant Styles

The `variant` parameter controls the visual appearance of the input field, allowing you to match your application's design aesthetic. Choose from "filled", "outlined" (default), or "standard":


```python
pmui.FlexBox(
    pmui.ColorPicker(label='Filled', variant="filled"),
    pmui.ColorPicker(label='Outlined', variant="outlined"),
    pmui.ColorPicker(label='Standard', variant="standard"),
)
```

### Size

The `size` parameter controls the size of the input. Choose from "small", "medium" (default), or "large":


```python
pmui.FlexBox(
    pmui.ColorPicker(label='Small', size="small"),
    pmui.ColorPicker(label='Medium', size="medium"),
    pmui.ColorPicker(label='Large', size="large"),
)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.ColorPicker(label='Color', value='#ff0000', helper_text='Choose a theme color')
```

### Disabled and Loading

Like other widgets, the `ColorPicker` can be disabled and/or show a loading indicator:


```python
pmui.ColorPicker(label='Color Picker', value='#99ef78', disabled=True, loading=True)
```

### Example: Color Designer

This example demonstrates how to use the `ColorPicker` widget to select a color and interactively display the selected color.


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

text_color = pmui.ColorPicker(label="Text Color", value="#e91e63")

def get_result(color):
    return f"<span style='background:{color};color:white;padding:10px;border-radius:8px'>{color}</span>"

result = pn.bind(get_result, text_color)

pmui.Column("# 🎨 Color Designer", result, text_color,)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_color_picker = pmui.ColorPicker(
    label=":material/palette: Accent color",
    value="#99ef78",
)

icon_color_picker
```

### API Reference

#### Parameters


```python
colorpicker.api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI DatePicker:**

- [Material UI ColorPicker Reference](https://viclafouch.github.io/mui-color-input/) - Complete documentation for the underlying Material UI component
- [Material UI ColorPicker API](https://viclafouch.github.io/mui-color-input/docs/api-reference/) - Detailed API reference and configuration options
