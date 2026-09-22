```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `LiteralInput` widget allows entering any valid Python literal (such as a number, string, list, dict, or tuple) using a text input box. This is useful for quickly entering and editing Python objects in dashboards and notebooks.

You can optionally set a `type` to validate the literal before updating the parameter. The `serializer` parameter lets you choose between Python's `ast.literal_eval` (default) and JSON serialization for parsing and formatting values.

#### Parameters:

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`enter_pressed`** (event): An event that triggers when the `<enter>` key is pressed.
- **`serializer`**: The serialization method to use (`'ast'` or `'json'`).
- **`type`**: The expected Python type (e.g., `dict`, `list`, `tuple`, `int`, `float`, `bool`, `str`).
- **`value`**: The current value, parsed as a Python literal.
- **`value_input`** (`str`): The current value as a string, updated on every key press.

##### Display

* **`color`** (str): The color variant of the input, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
- **`error_state`**: Indicates if the input could not be parsed as a valid literal.
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

For more details on customization, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html), [layout](https://panel.holoviz.org/how_to/layout/index.html), and [styling](https://panel.holoviz.org/how_to/styling/index.html) how-to guides.

___

### Basic Usage

The `LiteralInput` widget can be used to enter any valid Python literal. For example, you can enter a number, a string, a list, a dictionary, or a tuple


```python
literal_input = pmui.LiteralInput(label='Enter a literal', value={"a", 1})
literal_input
```

`LiteralInput.value` returns a literal type that can be read out and set like other widgets:


```python
literal_input.value
```

### Placeholder

The `LiteralInput` widget supports a `placeholder` which is displayed when the `value` is `None`:


```python
pmui.LiteralInput(label='Enter a literal', value=None, placeholder='e.g. 42, [1,2,3], {"a": 1}')
```

### Value Input

The `LiteralInput.value` is updated after an `enter_pressed` event or when switching focus, i.e. when clicking or tabbing away from the widget. To get the current `str` value after every keystroke you can inspect the `value_input` instead:


```python
literal_input = pmui.LiteralInput(label='Value', value={"a": 1})

pmui.Column(
    literal_input,
    pmui.Row(pn.pane.Str(literal_input.param.value), pn.pane.Str(literal_input.param.value_input))
)
```

### Enter Pressed

The `enter_pressed` parameter is triggered when the ENTER key is pressed


```python
literal_input_enter = pmui.LiteralInput(label="Press ENTER", value="abc")

enter_count = pn.rx(0)
def update_enter_count(event):
    enter_count.rx.value += 1
pn.bind(update_enter_count, literal_input_enter.param.enter_pressed, watch=True)

pmui.Column(literal_input_enter, enter_count)
```

### Maximum Length

The `max_length` controls the maximum number of characters that can be entered:


```python
pmui.LiteralInput(label='Enter a literal', value={"a", 1}, max_length=12)
```

### Error State

If the input cannot be parsed as a valid Python literal, the widget will indicate an error state, e.g. try entering `[]` and hit enter:


```python
pmui.LiteralInput(label='Invalid input', type=dict, value={})
```

By changing the value to `[}` you will change the `error_state`.

### Type and Serializer

Optionally, you can specify the expected `type` and the `serializer` method (either `'ast'` for Python literals or `'json'` for JSON data).                        


```python
ast_input = pmui.LiteralInput(label='Enter a literal', type=dict, serializer="ast", value={'a': 1}, placeholder='e.g. 42, [1,2,3], {"a": 1}')
json_input = pmui.LiteralInput(label='Enter a literal', type=dict, serializer="json", value={'a': 1}, placeholder='e.g. 42, [1,2,3], {"a": 1}')

def to_type(value):
    return str(type(value))

pmui.Row(
    pmui.Column(ast_input, pn.pane.Str(ast_input.param.value)),
    pmui.Column(json_input, pn.pane.Str(json_input.param.value)),
)
```

### DictInput, ListInput, and TupleInput

Specialized versions of `LiteralInput` are available for entering dictionaries, lists, and tuples. These widgets ensure the value is always of the expected type.


```python
pmui.DictInput(label='Enter a dictionary', placeholder="e.g. {'a': 1, 'b': 2}")
```


```python
pmui.ListInput(label='Enter a list', placeholder='e.g. [1, 2, 3]')
```


```python
pmui.TupleInput(label='Enter a tuple', placeholder='e.g. (1, 2, 3)')
```

### Disabled and Loading


```python
pmui.LiteralInput(label='Enter a literal', value=42, placeholder='e.g. 42, [1,2,3], {"a": 1}', disabled=True, loading=True)
```

### Color Options

You can set the `color` parameter to visually distinguish the `LiteralInput` when active. Available options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":


```python
pmui.FlexBox(
    *[pmui.LiteralInput(label=color, color=color) for color in pmui.TextInput.param.color.objects]
)
```

### Size

The `size` parameter allows toggling between "small", "medium" (default) and "large" sized input fields:


```python
pmui.FlexBox(
    pmui.LiteralInput(label='Small', size="small"),
    pmui.LiteralInput(label='Medium', size="medium"),
)
```

### Variant

The `variant` parameter controls the visual style of the input. Choose from "filled", "outlined" (default), or "standard":


```python
pmui.FlexBox(
    pmui.LiteralInput(label='Filled', variant="filled"),
    pmui.LiteralInput(label='Outlined', variant="outlined"),
    pmui.LiteralInput(label='Standard', variant="standard"),
)
```

### Description Tooltip


```python
pmui.LiteralInput(label='Enter a literal', value=42, description="A tooltip shown when hovering")
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.LiteralInput(label="Zoom :material/zoom_out_map:", value={"mode": "zoom"})
```

### API Reference

#### Parameters

The `LiteralInput` exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.LiteralInput(label='LiteralInput').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html)
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html)
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html)

**Material UI TextField:**

- [Material UI TextField Reference](https://mui.com/material-ui/react-text-field)
- [Material UI TextField API](https://mui.com/material-ui/api/text-field/)
