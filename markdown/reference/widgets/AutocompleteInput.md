```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `AutocompleteInput` widget enhances a standard text input by providing a panel of suggested options as you type. This widget is ideal in two main scenarios:

- When the input must be selected from a predefined set of valid values, such as a location field requiring a recognized location name.
- When any value is allowed, but offering suggestions—such as previous searches or similar terms—can help users save time and reduce errors.

`AutocompleteInput` belongs to the family of single-value, option-selection widgets, which also includes [`RadioBoxGroup`](RadioBoxGroup.ipynb), [`Select`](Select.ipynb), and [`DiscreteSlider`](DiscreteSlider.ipynb). These widgets share a consistent API for ease of use.

#### Parameters

For more details on customization, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (bool): If True, the widget is not editable.
* **`case_sensitive`** (bool, default=True): Controls whether matching is case sensitive.
* **`lazy_search`** (bool, default=False): If True, search queries are sent to the backend for processing.
* **`min_characters`** (int, default=2): Minimum number of characters required before suggestions appear.
* **`options`** (list or dict): The set of selectable options, provided as a list or dictionary.
* **`restrict`** (bool, default=True): If False, users can enter values not present in the options list.
* **`search_strategy`** (str): Determines how suggestions are matched. "starts_with" (default) matches from the beginning; "includes" matches any substring.
* **`value`** (str): The selected value, updated when the user presses <enter>. If `restrict=True`, must be one of the options.
* **`value_input`** (str): The current input value, updated on every key press.

##### Display

* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The widget's title.
* **`size`** (`Literal["small", "medium"]`): Whether the input field is "small" or "medium" sized.
* **`placeholder`** (str): Text shown when no value is selected.

##### Styling

- **`color` (str)**: Choose from "default" (default), "primary", "secondary", "error", "info", "success", "warning", "light", "dark", or "danger".
- **`sx`** (dict): Component-level styling options.
- **`theme_config`** (dict): Theming options.
- **`variant`** (str): Choose from "filled", "outlined" (default), or "standard".

##### Aliases

For compatibility with Panel, some parameters have aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

In its simplest form, `AutocompleteInput` lets users select a value from a predefined list of options.


```python
autocomplete = pmui.AutocompleteInput(
    label='Autocomplete Input', options=['Biology', 'Chemistry', 'Physics'], color='warning'
)

pmui.Row(autocomplete, height=125)
```

The available options appear as you start typing parts of the options in the list like "Bi", "Ch" or "Ph".

- The `value` parameter shows the currently selected option (updated when you press <enter> or select an option).
- The `value_input` parameter reflects the text currently entered or highlighted in the input field.


```python
pmui.Row(autocomplete.param.value, autocomplete.param.value_input)
```

Try typing "Ph" in the AutocompleteInput above, then select "Physics". Notice how the `value` parameter updates only when you make a selection, while `value_input` reflects your current input.

### Using a Dictionary for Options

You can also provide the `options` parameter as a dictionary. The keys will be displayed as labels in the dropdown menu, while the values are the actual option values.


```python
options_dict = pmui.AutocompleteInput(label='Autocomplete', options={'Biology': 1, 'Chemistry': 2, 'Physics': 3})

pmui.Row(options_dict, height=125)
```

Notice that the label is shown when no value is selected.

Let's observe how the `value` and `value_input` parameters change as you type and select a value.


```python
pmui.Row(options_dict.param.value, options_dict.param.value_input)
```

### Placeholder

You can set a `placeholder` to display helpful guidance in the input field when no value is selected.


```python
pmui.AutocompleteInput(
    label='Autocomplete Input', placeholder="Enter a value", options=['Biology', 'Chemistry', 'Physics'],
)
```

### Case Sensitivity

Control whether the filter is case sensitive using the `case_sensitive` parameter.


```python
case_insensitive = pmui.AutocompleteInput(
    label='Autocomplete Input', case_sensitive=False, options=['Biology', 'Chemistry', 'Physics'],
)

pmui.Row(case_insensitive, height=125)
```

Now, the option "Physics" will appear regardless of whether you type "ph", "pH", "Ph", or "PH".

### Minimum Characters Required

You can adjust the minimum number of characters a user must type before suggestions appear using the `min_characters` parameter.


```python
min_characters = pmui.AutocompleteInput(
    label='Autocomplete Input', min_characters=0, options=['Biology', 'Chemistry', 'Physics'],
)

pmui.Row(min_characters, height=200)
```

### Search Strategy

By default, `search_strategy` is set to "starts_with". You can change it to "includes" to match any part of the option string.

Try entering "aa", "bb", "cc", or "zz" to see how the matching works.


```python
search_strategy = pmui.AutocompleteInput(
    label='Autocomplete Input', search_strategy="includes", options=['aabbcc', 'bbaacc', 'zzaabb'],
)

pmui.Row(search_strategy, height=200)
```

Try entering "aa", "bb", "cc" or "zz".

### Lazy Search

When working with a huge number of options it is sometimes not feasible to send all the options to the frontend. Instead we may want to perform the search on the server and only return the results. This behavior can be enabled by setting `lazy_search=True`:


```python
N = 5000
options = [f"Item {i:04d}" for i in range(1, N + 1)]

lazy_autocomplete = pmui.AutocompleteInput(
    name="Search items",
    options=options,
    placeholder="Start typing (e.g. 'Item 0123')",
    case_sensitive=False,
    lazy_search=True
)

pmui.Row(lazy_autocomplete, height=200)
```

### Restrict Input

Control whether users can enter values not present in the options list using the `restrict` parameter.

If `restrict=False`, the `AutocompleteInput` will allow any input, not just the provided options. This is useful when you want to suggest completions but not limit user input.


```python
not_restricted = autocomplete.clone(value='Mathematics', restrict=False, options=['Biology', 'Chemistry', 'Physics'])

pmui.Row(not_restricted, height=125)
```

Let's observe how the `value` parameter updates as you enter custom values.


```python
pn.pane.Str(not_restricted.param.value)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.AutocompleteInput(label='Search', options=['Biology', 'Chemistry', 'Physics'], helper_text='Start typing to search')
```

### Disabled and Loading

Like other widgets, the `AutocompleteInput` can be disabled and/or show a loading indicator.


```python
pmui.AutocompleteInput(
    label='Autocomplete Input', disabled=True, loading=True, options=['Biology', 'Chemistry', 'Physics'],
)
```

### Color Options

You can set the `color` parameter to visually distinguish the `AutocompleteInput` when active. Available options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":


```python
pmui.FlexBox(
    *[pmui.AutocompleteInput(label=color, color=color) for color in pmui.AutocompleteInput.param.color.objects]
)
```

### Size

The `size` parameter allows toggling between "small" and "medium" (default) sized input fields:


```python
pmui.FlexBox(
    pmui.AutocompleteInput(label='Small', size="small"),
    pmui.AutocompleteInput(label='Medium', size="medium"),
)
```

### Variant

The `variant` parameter controls the visual style of the input. Choose from "filled", "outlined" (default), or "standard":


```python
pmui.FlexBox(
    pmui.AutocompleteInput(label='Filled', variant="filled"),
    pmui.AutocompleteInput(label='Outlined', variant="outlined"),
    pmui.AutocompleteInput(label='Standard', variant="standard"),
)
```

### Example: Favorite Programming Language

Lets create a self contained example:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

programming_languages = [
    "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", 
    "TypeScript", "Swift", "Kotlin", "Ruby", "PHP", "Scala", 
    "R", "MATLAB", "Julia", "Perl", "Haskell", "Clojure"
]

language_input = pmui.AutocompleteInput(
    label="Favorite Programming Language",
    options=programming_languages,
    placeholder="Start typing a programming language...",
    width=300
)

def create_text(value):
    if not value:
        return "No programming language selected"
    if value=="Python":
        return "🐍 **Python** is a great choice!"
    return f"Your favorite programming language is **{value}**"

text = pn.bind(create_text, language_input)

pn.Column("*Type in the field below to see autocomplete suggestions*", language_input, text)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_options = {
    ":material/zoom_out_map: Full screen": "fullscreen",
    ":material/zoom_in: Zoom in": "zoom_in",
    ":material/zoom_out: Zoom out": "zoom_out",
}

pmui.AutocompleteInput(
    label=":material/zoom_out_map: View",
    options=icon_options,
    value="fullscreen",
)
```

### API Reference

#### Parameters


```python
pmui.AutocompleteInput(
    label='Autocomplete Input', options=['Biology', 'Chemistry', 'Physics'],
).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI AutoComplete:**

- [Material UI AutoComplete Reference](https://mui.com/material-ui/react-autocomplete) - Complete documentation for the underlying Material UI component
- [Material UI AutoComplete API](https://mui.com/material-ui/api/autocomplete/) - Detailed API reference and configuration options
