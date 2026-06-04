```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Select` widget is used for collecting user provided information from a list or dictionary of `options` via a dropdown menu or selection area. Its built upon the [Material UI Select](https://mui.com/material-ui/react-select/) component.

The `Select` widget falls into the broad category of single-value, option-selection widgets that provide a compatible API and include the [`RadioBoxGroup`](RadioBoxGroup.ipynb), [`AutocompleteInput`](AutocompleteInput.ipynb) and [`DiscreteSlider`](DiscreteSlider.ipynb) widgets.

Explore more about using widgets to add interactivity to your applications in the [Make your component interactive](https://panel.holoviz.org/how_to/interactivity/index.html), [Link Parameters](https://panel.holoviz.org/how_to/links/index.html) or 
[Declarative API](https://panel.holoviz.org/how_to/param/index.html) guides.

#### Parameters:

For details on other options for customizing the component, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable.
* **`disabled_options`** (list): Optional list of `options` that are disabled, i.e., unusable and un-clickable. If `options` is a dictionary, the list items must be dictionary values.
* **`filter_on_search`** (boolean): Whether to filter or highlight the matching options on search.
* **`filter_str`** (str): Filter string for the dropdown.
* **`groups`** (dict): A dictionary whose keys are used to visually group the options and whose values are either a list or a dictionary of options to select from. Mutually exclusive with `options` and valid only if `size` is 1.
* **`options`** (list or dict): A list or dictionary of options to select from.
* **`searchable`** (boolean): Whether to render a search box.
* **`value`** (object): The current value; must be one of the option values.

##### Display

* **`bookmarks`** (list): List of bookmarked options that are rendered first.
* **`color`** (str): The color variant of the input, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`dropdown_open`** (bool): Whether the dropdown is open.
* **`dropdown_height`** (int): Height of the dropdown menu.
* **`label`** (str): The title of the widget.
* **`variant`** (str): One of filled, outlined (default), or standard.

##### Styling

- **`sx`** (dict): Component-level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel, certain parameters are allowed as aliases:

- **`name`**: Alias for `label`.

___

### Basic Usage

The `Select` widget allows selecting from a list of `options`:


```python
select = pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], height=200)

select
```

Like most other widgets, ``Select`` has a value parameter that can be accessed or set:


```python
select.value
```

The `options` parameter also accepts a dictionary whose keys are going to be the labels of the dropdown menu. 


```python
select = pmui.Select(label='Age', options={'Ten': 10, 'Twenty': 20, 'Thirty': 30}, height=200)

select
```


```python
select.value
```

Updating the value will display the right label.


```python
select.value = 30
```

### Filled and Standard Variants


```python
pmui.Row(
    pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], variant="standard"),
    pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], variant="filled"),
    height=200
)
```

### Colors


```python
pn.FlexBox(*[pmui.Select(label=color, options=['Ten', 'Twenty', 'Thirty'], color=color) for color in pmui.Select.param.color.objects])
```

The color will show when you select a select widget.

### Other Parameters


```python
pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], disabled=True, loading=True)
```

### Searchable

You can make the `Select` widget `searchable`.


```python
pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], searchable=True, height=250)
```

You can configure whether options are filtered or merely highlighted on search.


```python
pmui.Row(
    pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], searchable=True, filter_on_search=True),
    pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], searchable=True, filter_on_search=False),
    height=250
)
```

You may provide a default string to filter on:


```python
pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty'], searchable=True, filter_str="F", height=250)
```

### Dropdown Height and Open State

You may control the `dropdown_height` and the `drowdown_open` state programmatically:


```python
pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty'], dropdown_height=200, dropdown_open=False, height=250)
```

### Disabled Options

A subset of the displayed items can be disabled with `disabled_options`. The widget `value` cannot be set to one of the `disabled_options`, either programmatrically or with the user interface.


```python
pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty'], disabled_options=['Twenty'], height=200)
```

### Grouping

The items displayed in the dropdown menu can be grouped visually (also known as *optgroup*) by setting the `groups` parameter **instead of** `options`. `groups` accepts a dictionary whose keys are used to group the options and whose values are defined similarly to how `options` are defined.


```python
grouped = pmui.Select(label='Select', groups={'Europe': ['Greece', 'France'], 'Africa': ['Algeria', 'Congo']}, height=300)

grouped
```

### Bookmarks

Options can also be set as `bookmarks` which moves them to the top of the list:


```python
pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty'], bookmarks=['Ten', 'Fourty'], height=250)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.Select(
    label="Mode :material/zoom_out_map:",
    options={"Zoom :material/zoom_out_map:": "zoom", "Explore :material/explore:": "explore"},
    value="zoom",
)
```

### API Reference

#### Parameters

The `Select` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Select(label='Age', options=['Ten', 'Twenty', 'Thirty', 'Fourty', 'Fifty']).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Select:**

- [Material UI Select Reference](https://mui.com/material-ui/react-select/) - Complete documentation for the underlying Material UI component
- [Material UI Select API](https://mui.com/material-ui/api/select/) - Detailed API reference and configuration options
