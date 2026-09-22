```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Switch` widget allows users to toggle between `True` and `False` states with an intuitive flick-switch interface. This widget provides the same functionality as the `Checkbox` and `Toggle` widgets but with a distinctly modern visual appearance that clearly communicates on/off states.

Perfect for settings panels, feature toggles, and any binary choice where visual clarity is important, the `Switch` widget offers an elegant alternative to traditional checkboxes.

#### Parameters

For more details on customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (bool): When True, the widget becomes non-interactive and appears grayed out.
* **`value`** (bool): The current state of the switch (`True` for on/enabled, `False` for off/disabled).

##### Display

* **`edge`** (str): Controls the switch positioning - `'start'` (left-aligned), `'end'` (right-aligned), or `False` for center alignment.
* **`label`** (str): The descriptive text displayed alongside the switch.

##### Styling

- **`color`** (str): The color theme applied to the switch when active.
- **`size`** (str): Controls the physical size of the switch component.
- **`sx`** (dict): Advanced styling options for fine-tuned appearance control.
- **`theme_config`** (dict): Theme-level configuration for consistent styling across your application.

##### Aliases

For seamless compatibility with Panel widgets, certain parameters accept aliases:

- **`name`**: Alternative parameter name for `label`

___

### Basic Usage

Getting started with the Switch widget is straightforward. Here's how to create a simple switch with a descriptive label:


```python
switch = pmui.Switch(label='Switch')

switch
```

The `value` parameter automatically updates to reflect the switch state: `True` when switched on, `False` when switched off. You can also programmatically set this value to control the switch state.


```python
switch.value
```

### Color Options

Customize your switch's appearance to match your application's design language using the `color` parameter. Each color provides different visual emphasis and semantic meaning:


```python
pmui.Switch(value=True, label="secondary", color="secondary")
```

Here's a showcase of all available color options:


```python
pmui.FlexBox(
    *(pmui.Switch(value=True, label=color, color=color) for color in pmui.Switch.param.color.objects)
)
```

### Size Options

Adjust the switch size using the `size` parameter:


```python
pmui.FlexBox(
    pmui.Switch(label="small", size="small"),
    pmui.Switch(label="medium", size="medium"),
)
```

### Edge Options

Adjust the edge using the `edge` parameter:


```python
pmui.FlexBox(
    pmui.Switch(label="start", edge="start"),
    pmui.Switch(label="end", edge="end"),
    pmui.Switch(label="False", edge=False),
)
```

### Disabled and Loading

Like other widgets, the `Switch` can be disabled and/or show a loading indicator.


```python
pmui.Switch(label="Switch", disabled=True, loading=True)
```

### Example: Dark Mode Toggle


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

dark_mode = pmui.Switch(label="Dark Mode", value=False)

def create_theme_message(value):
    if value:
        return "🌙 Dark mode is enabled"
    
    return "☀️ Light mode is enabled"

theme_message = pn.bind(create_theme_message, dark_mode)

pmui.Column(dark_mode, theme_message)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.Switch(label="Zoom :material/zoom_out_map:", value=True)
```

### API Reference

#### Parameters

The `Switch` widget exposes a number of options which can be changed from both Python and Javascript:


```python
pmui.Switch(label="Switch").api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Switch:**

- [Material UI Switch Reference](https://mui.com/material-ui/react-switch/) - Complete documentation for the underlying Material UI component
- [Material UI Switch API](https://mui.com/material-ui/api/switch/) - Detailed API reference and configuration options
