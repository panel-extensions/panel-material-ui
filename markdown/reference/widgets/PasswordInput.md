```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `PasswordInput` allows entering any string using an obfuscated text input box.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`value`** (str): The current value updated when pressing `<enter>` key.
* **`value_input`** (str): The current value updated on every key press.

##### Display

* **`color`** (str): The color variant of the input, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`error_state`** (boolean): Indicates an invalid text entry.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`max_length`** (int): The maximum number of allowed characters.
* **`label`** (str): The title of the widget
* **`placeholder`** (str): A placeholder string displayed when no value is entered.
* **`size`** (`Literal["small", "medium"]`): The size variant of the widget.
* **`variant`** (`Literal["filled", "outlined", "standard"]`): The variant of the input field.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

The `PasswordInput` widget provides a simple text entry form and supports a `placeholder` which is displayed when the `value` is empty:


```python
password_input = pmui.PasswordInput(label='Password', placeholder='Enter your password here...')
password_input
```

``PasswordInput.value`` returns a string type that can be read out and set like other widgets:


```python
password_input.value
```

### Value Input

The `PasswordInput.value` is updated after an `enter_pressed` event or when switching focus, i.e. when clicking or tabbing away from the widget. To get the current value after every keystroke you can inspect the `value_input` instead:


```python
value = pmui.PasswordInput(label='Value Input', value='Hello W')
value_input = pmui.PasswordInput(label='Value Input', value='Hello W')

pmui.Column(
    pmui.Row(value, pmui.Typography(value.param.value)),
    pmui.Row(value_input, pmui.Typography(value_input.param.value_input))
)
```

### Maximum Length

The `max_length` controls the maximum number of characters that can be entered:


```python
pmui.PasswordInput(label='Password (max_length=12)', max_length=12)
```

### Error State

The `error_state` parameter allows setting of the message that is displayed if validation of the input fails.


```python
pmui.PasswordInput(label='PasswordInput (invalid entry)', error_state=True)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.PasswordInput(label='Password', helper_text='Must be at least 8 characters')
```

### Disabled and Loading

Like other widgets, the `PasswordInput` can be disabled and/or show a loading indicator.


```python
pmui.PasswordInput(
    label='Text Input', disabled=True, loading=True,
)
```

### Color Options

You can set the `color` parameter to visually distinguish the `PasswordInput` when active. Available options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":


```python
pmui.FlexBox(
    *[pmui.PasswordInput(label=color, color=color) for color in pmui.PasswordInput.param.color.objects]
)
```

### Size

The `size` parameter allows toggling between "small" and "medium" (default) sized input fields:


```python
pmui.FlexBox(
    pmui.PasswordInput(label='Small', size="small"),
    pmui.PasswordInput(label='Medium', size="medium"),
)
```

### Variant

The `variant` parameter controls the visual style of the input. Choose from "filled", "outlined" (default), or "standard":


```python
pmui.FlexBox(
    pmui.PasswordInput(label='Filled', variant="filled"),
    pmui.PasswordInput(label='Outlined', variant="outlined"),
    pmui.PasswordInput(label='Standard', variant="standard"),
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.PasswordInput(label="Zoom :material/zoom_out_map:", placeholder="Enter password")
```

### API Reference

#### Parameters


```python
pmui.PasswordInput(
    label='PasswordInput'
).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI AutoComplete:**

- [Material UI TextField Reference](https://mui.com/material-ui/react-text-field) - Complete documentation for the underlying Material UI component
- [Material UI TextField API](https://mui.com/material-ui/api/text-field/) - Detailed API reference and configuration options


```python
pmui.Row(password_input.controls(jslink=True), password_input)
```
