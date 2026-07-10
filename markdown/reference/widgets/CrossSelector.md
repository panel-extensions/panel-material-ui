```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `CrossSelector` widget allows selecting multiple values from a list of options. It falls into the broad category of multi-value, option-selection widgets that provide a compatible API and include the [`MultiSelect`](MultiSelect.ipynb), [`CheckBoxGroup`](CheckBoxGroup.ipynb) and [`CheckButtonGroup`](CheckButtonGroup.ipynb) widgets.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`options`** (list or dict): List or dictionary of options
* **`searchable`** (boolean): Whether to render a search box.
* **`value`** (list): Currently selected option values

##### Display

* **`color`** (str): The color variant of the inputs, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`label`** (str): The title of the widget

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

The `CrossSelector` provides a convenient API for selecting from multiple options:


```python
cross_select = pmui.CrossSelector(label='CrossSelector', value=['Apple', 'Pear'],
    options=['Apple', 'Banana', 'Pear', 'Strawberry'])

cross_select
```

`CrossSelector.value` returns a list of the currently selected options:


```python
cross_select.value
```

### Searchable

You can also disable the search field in the selector by setting `searchable=False`:


```python
pmui.CrossSelector(label='Age', options=['Ten', 'Twenty', 'Thirty'], searchable=False)
```

### Colors


```python
pn.FlexBox(*[pmui.CrossSelector(
    label=color, value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], color=color
) for color in pmui.CrossSelector.param.color.objects])
```

### Disabled & Loading

Like all widgets the `CrossSelector` supports `disabled` and `loading` states:


```python
pmui.CrossSelector(label='Ages', options=['Ten', 'Twenty', 'Thirty'], disabled=True, loading=True)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_cross_selector = pmui.CrossSelector(
    label=":material/checklist: Status",
    value=["high", "paused"],
    options={
        ":material/priority_high: High": "high",
        ":material/pause_circle: Paused": "paused",
        ":material/low_priority: Low": "low",
    },
)

icon_cross_selector
```

### API Reference

#### Parameters

The `CrossSelector` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.CrossSelector(
    label='CrossSelector', value=['Apple', 'Pear'],
    options=['Apple', 'Banana', 'Pear', 'Strawberry']
).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Transfer List:**

- [Material UI Transfer List Reference](https://mui.com/material-ui/react-transfer-list/) - Complete documentation for the underlying Material UI component
