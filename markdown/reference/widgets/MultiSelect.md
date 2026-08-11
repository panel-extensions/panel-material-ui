```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `MultiSelect` widget allows selecting multiple values from a list of options. It is built upon the [Material UI Select](https://mui.com/material-ui/react-select/#multiple-select) component with the `native` and `multiple` props.

The `MultiSelect` widget falls into the broad category of multi-value, option-selection widgets that provide a compatible API and include the [`CrossSelector`](CrossSelector.ipynb), [`CheckBoxGroup`](CheckBoxGroup.ipynb) and [`CheckButtonGroup`](CheckButtonGroup.ipynb) widgets.

Explore more about using widgets to add interactivity to your applications in the [Make your component interactive](https://panel.holoviz.org/how_to/interactivity/index.html), [Link Parameters](https://panel.holoviz.org/how_to/links/index.html) or [Declarative API](https://panel.holoviz.org/how_to/param/index.html) guides.

#### Parameters:

For details on other options for customizing the component, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable.
* **`max_items`** (int): Maximum number of options that can be selected.
* **`options`** (list or dict): A list or dictionary of options to select from.
* **`size`** (int): The number of options to display at once. Controls the visible height of the list area.
* **`value`** (list): Currently selected option values.

##### Display

* **`color`** (str): The color variant of the input.
* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The title of the widget.
* **`variant`** (str): One of `'filled'`, `'outlined'` (default), or `'standard'`.

##### Styling

- **`sx`** (dict): Component-level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel, certain parameters are allowed as aliases:

- **`name`**: Alias for `label`.

___

### Basic Usage

The `MultiSelect` widget allows selecting multiple values from a list of `options`:


```python
multi_select = pmui.MultiSelect(
    label='Fruits', value=['Apple', 'Pear'],
    options=['Apple', 'Banana', 'Pear', 'Strawberry'], size=4
)

multi_select
```

Like most other widgets, `MultiSelect` has a value parameter that can be accessed or set:


```python
multi_select.value
```

The `options` parameter also accepts a dictionary whose keys are going to be the visible labels:


```python
dict_select = pmui.MultiSelect(
    label='Frameworks', value=['panel', 'bokeh'],
    options={'Panel': 'panel', 'Bokeh': 'bokeh', 'Plotly': 'plotly', 'Matplotlib': 'matplotlib'},
    size=4
)

dict_select
```

### Filled and Standard Variants


```python
options = ['Apple', 'Banana', 'Pear', 'Strawberry']

pmui.Row(
    pmui.MultiSelect(label='Outlined', options=options, variant="outlined", size=4, width=200),
    pmui.MultiSelect(label='Filled', options=options, variant="filled", size=4, width=200),
    pmui.MultiSelect(label='Standard', options=options, variant="standard", size=4, width=200),
)
```

### Colors


```python
pn.FlexBox(*[
    pmui.MultiSelect(label=color, options=['A', 'B', 'C'], color=color, value=['A'], size=3, width=150)
    for color in pmui.MultiSelect.param.color.objects
])
```

### Size

The `size` parameter controls how many rows are visible at once.


```python
many_options = [f"Option {i}" for i in range(20)]

pmui.Row(
    pmui.MultiSelect(label='size=5', options=many_options, size=5, width=200),
    pmui.MultiSelect(label='size=12', options=many_options, size=12, width=200),
)
```

### Max Items

The `max_items` parameter limits how many options can be selected at once. When the limit is reached, selecting a new option deselects the oldest one:


```python
pmui.MultiSelect(
    label='Select up to 3',
    options=['Apple', 'Banana', 'Pear', 'Strawberry', 'Mango', 'Kiwi'],
    max_items=3, size=6
)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.MultiSelect(label='Fruits', options=['Apple', 'Banana', 'Pear'], value=[], helper_text='Hold Ctrl to select multiple')
```

### Disabled


```python
pmui.MultiSelect(
    label='Disabled', options=['Apple', 'Banana', 'Pear'],
    value=['Apple'], disabled=True, size=3
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.MultiSelect(
    label="Modes :material/zoom_out_map:",
    options={"Zoom :material/zoom_out_map:": "zoom", "Explore :material/explore:": "explore"},
    value=["zoom"],
    size=2,
)
```

### API Reference

#### Parameters

The `MultiSelect` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.MultiSelect(
    label='Fruits', options=['Apple', 'Banana', 'Pear', 'Strawberry', 'Mango', 'Kiwi'],
    value=['Apple'], size=6
).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Select:**

- [Material UI Select Reference](https://mui.com/material-ui/react-select/#multiple-select) - Complete documentation for the underlying Material UI component
- [Material UI Select API](https://mui.com/material-ui/api/select/) - Detailed API reference and configuration options
