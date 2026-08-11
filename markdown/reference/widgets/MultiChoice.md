```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `MultiChoice` widget allows selecting multiple values from a list of options. It falls into the broad category of multi-value, option-selection widgets that provide a compatible API and include the [`MultiSelect`](MultiSelect.ipynb), [`CrossSelector`](CrossSelector.ipynb), [`CheckBoxGroup`](CheckBoxGroup.ipynb) and [`CheckButtonGroup`](CheckButtonGroup.ipynb) widgets. The `MultiChoice` widget provides a much more compact UI than [`MultiSelect`](MultiSelect.ipynb).

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`bookmarks`** (list): List of bookmarked options that are rendered first.
* **`disabled`** (boolean): Whether the widget is editable
* **`disabled_options`** (list): List of options that are disabled.
* **`filter_on_search`** (boolean): Whether to filter or highlight the matching options on search.
* **`option_limit`** (int): Maximum number of options to display at once.
* **`options`** (list or dict): List or dictionary of options
* **`search_option_limit`** (int): Maximum number of options to display at once if search string is entered.
* **`max_items`** (int): Maximum number of options that can be selected
* **`searchable`** (boolean): Whether to render a search box.
* **`value`** (list): Currently selected option values

##### Display

* **`color`** (str): The color variant of the input and indicating the selected item(s), which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`delete_button`** (boolean): Whether to display a button to delete a selected option
* **`dropdown_height`** (int | None): Height of the select dropdown.
* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The title of the widget
* **`placeholder`** (str): String displayed when no selection has been made.
* **`solid`** (boolean): Whether to display widget with solid or light style.
* **`variant`** (str): One of filled, outlined (default), or standard.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`
___

### Basic Usage

The `MultiChoice` widget allows selecting multiple values from a list of `options`:


```python
multi_choice = pmui.MultiChoice(label='MultiChoice', value=['Apple', 'Pear'],
    options=['Apple', 'Banana', 'Pear', 'Strawberry'])

pmui.Column(multi_choice, height=250)
```

``MultiChoice.value`` returns a list of the currently selected options:


```python
multi_choice.value
```

The `options` parameter also accepts a dictionary whose keys are going to be the labels of the dropdown menu. 


```python
ages = pmui.MultiChoice(
    label='Ages', options={'Ten': 10, 'Twenty': 20, 'Thirty': 30}, height=200
)

ages
```


```python
ages.value
```

Updating the value will display the right label.


```python
ages.value = [20, 30]
```

### Filled and Standard Variants


```python
pmui.Row(
    pmui.MultiChoice(label='Fruits', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], variant="standard"),
    pmui.MultiChoice(label='Fruits', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], variant="filled"),
    height=200
)
```

### Chips

By default the selections are rendered as chips, this can be disabled with `chip=False`, alternatively the chip variant can be toggled with `solid=False`:


```python
pmui.Row(
    pmui.MultiChoice(label='Fruits', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], chip=False),
    pmui.MultiChoice(label='Fruits', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], solid=False)
)
```

### Colors


```python
pn.FlexBox(*[pmui.MultiChoice(
    label=color, value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], color=color
) for color in pmui.Select.param.color.objects])
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.MultiChoice(label='Tags', options=['Python', 'JavaScript', 'Rust'], value=[], helper_text='Select one or more tags')
```

### Disabled & Loading

Like all widgets the `MultiChoice` supports `disabled` and `loading` states:


```python
pmui.MultiChoice(label='Ages', options=['Ten', 'Twenty', 'Thirty'], disabled=True, loading=True)
```

### Searchable

You can make the `MultiChoice` widget `searchable`.


```python
pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty'], searchable=True, height=350)
```

You can configure whether options are filtered or merely highlighted on search.


```python
pmui.Row(
    pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty'], searchable=True, filter_on_search=True),
    pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty'], searchable=True, filter_on_search=False),
    height=350
)
```

You may provide a default string to filter on:


```python
pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty'], searchable=True, filter_str="F", height=250)
```

### Dropdown Height and Open State

You may control the dropdown height and the drowdown open state


```python
pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty'], dropdown_height=200, dropdown_open=True, height=250)
```

### Disabled Options

A subset of the displayed items can be disabled with `disabled_options`. The widget `value` cannot be set to one of the `disabled_options`, either programmatrically or with the user interface.


```python
pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty'], disabled_options=['Twenty'], height=200)
```

### Bookmarks


```python
pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty'], bookmarks=['Ten', 'Fourty'], height=250).show()
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.MultiChoice(
    label="Modes :material/zoom_out_map:",
    options={"Zoom :material/zoom_out_map:": "zoom", "Explore :material/explore:": "explore"},
    value=["zoom"],
)
```

### API Reference

#### Parameters

The `MultiChoice` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.MultiChoice(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty']).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Select:**

- [Material UI Select Reference](https://mui.com/material-ui/react-select/) - Complete documentation for the underlying Material UI component
- [Material UI Select API](https://mui.com/material-ui/api/select/) - Detailed API reference and configuration options
