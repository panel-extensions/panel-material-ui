```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `TextInput` widget allows entering any string using a text input box.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`enter_pressed`** (event): An event that triggers when the `<enter>` key is pressed.
* **`value`** (str): The current value updated when pressing the `<enter>` key or when the widget loses focus because the user clicks away or presses the tab key.
* **`value_input`** (str): The current value updated on every key press.

##### Display

* **`color`** (str): The color variant of the inputs, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
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

The `TextInput` widget provides a simple text entry form:


```python
text_input = pmui.TextInput(label=':material/zoom_out_map: Some label')
text_input
```

``TextInput.value`` returns a string type that can be read out and set like other widgets:


```python
text_input.value
```

### Placeholder

The `TextInput` widget provides a simple text entry form and supports a `placeholder` which is displayed when the `value` is empty:


```python
pmui.TextInput(label="Some label", placeholder="Some placeholder")
```

### Value Input

The `TextInput.value` is updated after an `enter_pressed` event or when switching focus, i.e. when clicking or tabbing away from the widget. To get the current value after every keystroke you can inspect the `value_input` instead:


```python
value_input = pmui.TextInput(label='Value', value='Hello W')

pmui.Column(
    value_input,
    pmui.Row(pmui.Typography(value_input.param.value), pmui.Typography(value_input.param.value_input))
)
```

### Enter Pressed

The `enter_pressed` parameter is triggered when ENTER key is pressed


```python
text_input_enter = pmui.TextInput(label="Press ENTER")

enter_count = pn.rx(0)
def update_enter_count(event):
    enter_count.rx.value += 1
pn.bind(update_enter_count, text_input_enter.param.enter_pressed, watch=True)

pmui.Column(text_input_enter, enter_count)
```

### Maximum Length

The `max_length` controls the maximum number of characters that can be entered:


```python
pmui.TextInput(label='Name (max_length=12)', max_length=12)
```

### Error State

Often times you will want to validate the input to a `TextInput`. To indicate that there is some error in the entry you can set the `error_state` parameter:


```python
pmui.TextInput(label='TextInput (invalid entry)', error_state=True)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.TextInput(label='Name', helper_text='Enter your full name')
```

### Disabled and Loading

Like other widgets, the `AutocompleteInput` can be disabled and/or show a loading indicator.


```python
pmui.TextInput(
    label='Text Input', disabled=True, loading=True,
)
```

### Color Options

You can set the `color` parameter to visually distinguish the `TextInput` when active. Available options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":


```python
pmui.FlexBox(
    *[pmui.TextInput(label=color, color=color) for color in pmui.TextInput.param.color.objects]
)
```

### Size

The `size` parameter allows toggling between "small", "medium" (default) and "large" sized input fields:


```python
pmui.FlexBox(
    pmui.TextInput(label='Small', size="small"),
    pmui.TextInput(label='Medium', size="medium"),
)
```

### Variant

The `variant` parameter controls the visual style of the input. Choose from "filled", "outlined" (default), or "standard":


```python
pmui.FlexBox(
    pmui.TextInput(label='Filled', variant="filled"),
    pmui.TextInput(label='Outlined', variant="outlined"),
    pmui.TextInput(label='Standard', variant="standard"),
)
```

### Description Tooltip


```python
pmui.TextInput(label='Some label', description="Some tooltip")
```

### Example: Search

This example will search a list based on `value_input`:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

VALUES = [
    "Hello", "Hello World", "Hello Panel Material UI",
    "Hallo", "Hallo World", "Hallo Panel Material UI",
]

search_text = pmui.TextInput(label='Search', placeholder='Search here')

def search(text):
    if text:
        return [v for v in VALUES if text.lower() in v.lower()]
    return VALUES

pmui.Column(search_text, pn.bind(search, search_text.param.value_input),)
```

### Example: Input Form with Validation

The form below requires you to enter a name 3 characters long or longer:


```python
import param
import panel as pn
import panel_material_ui as pmui

pn.extension()

class FormState(param.Parameterized):
    value = param.String(default='', label="Name", doc="Input value for the text field.")
    error_message = param.String(default='', doc="Error message for validation.")

    @pn.depends("value")
    def label(self):
        if not self.error_message:
            return "Name"
        return f"Name ({self.error_message})"

    @pn.depends("value")
    def error_state(self):
        return bool(self.error_message)
    
    @pn.depends("value", "error_message")
    def validated_value(self):
        if not self.value or self.error_message:
            return None
        return f"Valid value: **{self.value}**"
    
    @param.depends('value', watch=True)
    def validate_value(self):
        if len(self.value) < 3:
            self.error_message = "Must be at least 3 characters"
        else:
            self.error_message = ""
    

state = FormState()

text_input = pmui.TextInput(value=state.value, label=state.label, placeholder='Enter your name...', error_state=state.error_state)

def set_value(event):
    state.value = text_input.value

submit_button = pmui.Button(label='Submit', color='primary', on_click=set_value)

pmui.Column(
    "## TextInput Form",
    text_input,
    submit_button,
    state.validated_value,
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.TextInput(
    label=":material/zoom_out_map: Search",
    placeholder="Search...",
)
```

### API Reference

#### Parameters


```python
pmui.TextInput(
    label='TextInput'
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
