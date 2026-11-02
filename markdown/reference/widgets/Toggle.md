```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Toggle` widget allows users to toggle between `True` and `False` states using a button-style interface. This widget provides the same functionality as the `Checkbox` and `Switch` widgets but with a more prominent visual appearance that's perfect for actions and feature toggles.

Ideal for primary actions, feature toggles, and situations where you want the toggle state to be highly visible and engaging, the `Toggle` widget offers a button-like alternative to traditional checkboxes and switches.

#### Parameters

For more details on customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (bool): When True, the widget becomes non-interactive and appears grayed out.
* **`value`** (bool): The current state of the toggle (`True` for pressed/active, `False` for unpressed/inactive).

##### Display

* **`end_icon`** (str): An icon displayed to the right of the button label. Accepts Material UI icon names or SVG strings.
* **`icon`** (str): An icon displayed to the left of the button label. Accepts Material UI icon names or SVG strings.
* **`icon_size`** (str): The size of the icons (e.g., '12px', '1em', '2rem').
* **`label`** (str): The descriptive text displayed on the toggle button.
* **`variant`** (str): The visual style of the button - `'contained'`, `'outlined'`, or `'text'`.

##### Styling

- **`color`** (str): The color theme applied to the toggle button when active.
- **`sx`** (dict): Advanced styling options for fine-tuned appearance control.
- **`theme_config`** (dict): Theme-level configuration for consistent styling across your application.

##### Aliases

For seamless compatibility with Panel widgets, certain parameters accept aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alternative parameter name for `label`

___

### Basic Usage

Getting started with the Toggle widget is straightforward. Here's how to create a simple toggle button with a descriptive label and initial state:


```python
toggle = pmui.Toggle(label='Toggle', button_type='success', value=True)

toggle
```

The `value` parameter automatically updates to reflect the toggle state: `True` when pressed/active, `False` when unpressed/inactive. You can also programmatically set this value to control the toggle state.


```python
toggle.value
```

### Color Options

Customize your toggle's appearance to match your application's design language using the `color` parameter. Each color provides different visual emphasis and semantic meaning:


```python
pmui.Toggle(label="secondary", color="secondary", value=True)
```

Here's a showcase of all available color options:


```python
pmui.FlexBox(
    *(pmui.Toggle(label=color, color=color, value=True) for color in pmui.Toggle.param.color.objects)
)
```

### Icons and Visual Enhancement

The `Toggle` widget supports various ways to add visual elements. You can use Unicode characters and emoji in the label for simple graphical buttons:


```python
pmui.FlexBox(
    pmui.Toggle(label='\u25c0', width=50),
    pmui.Toggle(label='\u25b6', width=50),
    pmui.Toggle(label='🔍', width=100),
    pmui.Toggle(label="▶️ Play", width=100),
    pmui.Toggle(label="Pause ⏸️", width=100)
)
```

For more professional interfaces, you can use explicit icons. Material UI provides a comprehensive icon library accessible by name:


```python
pmui.Toggle(icon='lock', button_type='light', icon_size='2em')
```

You can also use custom SVG icons for complete design control:


```python
shuffle_icon = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-arrows-shuffle" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M18 4l3 3l-3 3" />
  <path d="M18 20l3 -3l-3 -3" />
  <path d="M3 7h3a5 5 0 0 1 5 5a5 5 0 0 0 5 5h5" />
  <path d="M21 7h-5a4.978 4.978 0 0 0 -3 1m-4 8a4.984 4.984 0 0 1 -3 1h-3" />
</svg>
"""

pmui.Toggle(icon=shuffle_icon, button_type='success', label='Shuffle', icon_size='2em')
```

For enhanced visual communication, combine both start and end icons:


```python
pmui.Toggle(icon='send', button_type='light', icon_size='2em', end_icon='rocket', label='Sent')
```

### Disabled and Loading States

Like other widgets, the `Toggle` can be disabled and/or show a loading indicator to provide clear feedback during various application states:


```python
pmui.Toggle(label="Toggle", disabled=True, loading=True)
```

### Example: Notification Toggle

Let's create a practical example that demonstrates how toggles work in real applications. This notification toggle shows how to bind toggle values to dynamic content updates:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

notifications_toggle = pmui.Toggle(
    label="Notifications", 
    icon="notifications", 
    color="primary",
    value=True
)

def create_notification_status(value):
    if value:
        return "🔔 Notifications are enabled - you'll receive updates"
    
    return "🔕 Notifications are disabled - you won't receive updates"

notification_status = pn.bind(create_notification_status, notifications_toggle)

pmui.Column(notifications_toggle, notification_status)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.Toggle(
    label=":material/zoom_out_map: Zoom mode",
    color="primary",
    value=True,
)
```

### API Reference

#### Interactive Parameter Explorer

The `Toggle` widget offers numerous customization options that can be modified from both Python and JavaScript. Explore these parameters interactively to see their effects in real-time:


```python
pmui.Toggle(label="Toggle").api(jslink=True)
```

### Further Learning

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Master the art of creating interactive applications with widgets and dynamic updates
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect widget parameters to create responsive, reactive user interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build sophisticated parameter-driven applications with minimal code

**Material UI Toggle Button:**

- [Material UI Toggle Button Reference](https://mui.com/material-ui/react-toggle-button/) - Comprehensive documentation for the underlying Material UI component
- [Material UI Toggle Button API](https://mui.com/material-ui/api/toggle-button/) - Complete API reference with advanced configuration options and examples
