```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `MultiPill` widget allows selecting multiple values from a list or dictionary of `options` rendered as clickable pills. It is built on top of the [Material UI Chip](https://mui.com/material-ui/react-chip/) component.

The `MultiPill` widget falls into the broad category of multi-value, option-selection widgets that provide a compatible API and include the [`MultiSelect`](MultiSelect.ipynb), [`MultiChoice`](MultiChoice.ipynb) and [`CheckBoxGroup`](CheckBoxGroup.ipynb) widgets.

Discover more about using widgets to add interactivity to your applications in the [Make your component interactive](https://panel.holoviz.org/how_to/interactivity/index.html) guide. For linking or callbacks, see the [Links](https://panel.holoviz.org/how_to/links/index.html) and [Param](https://panel.holoviz.org/how_to/param/index.html) guides.

#### Parameters

For details on other options for customizing the component, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable.
* **`disabled_options`** (list): Optional list of `options` that are disabled.
* **`max_items`** (int): Maximum number of options that can be selected.
* **`options`** (list or dict): A list or dictionary of options to select from.
* **`value`** (list): The current list of selected values.

##### Display

* **`color`** (str): The color of selected pills.
* **`label`** (str): The title of the widget.
* **`size`** (str): One of small, medium (default), or large.
* **`variant`** (str): One of filled or outlined (default).

##### Styling

- **`sx`** (dict): Component-level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel, certain parameters are allowed as aliases:

- **`name`**: Alias for `label`.

___

### Basic Usage

The `MultiPill` widget allows selecting multiple options:


```python
multipill = pmui.MultiPill(
    label='Favourites',
    value=['Panel', 'hvPlot'],
    options=['Panel', 'hvPlot', 'HoloViews', 'GeoViews'],
)

multipill
```

### Dictionary Options

Provide options as a dictionary to map labels to values:


```python
pmui.MultiPill(
    label='Grades',
    value=['A'],
    options={'Excellent': 'A', 'Good': 'B', 'Fair': 'C'},
)
```

### Sizes

Use the `size` parameter to control the chip size:


```python
pmui.FlexBox(
    *(pmui.MultiPill(label=size, size=size, options=['One', 'Two', 'Three'], value=['Two'])
      for size in pmui.MultiPill.param.size.objects)
)
```

### Variants

Choose from `filled` or `outlined` variants:


```python
pmui.FlexBox(
    *(pmui.MultiPill(label=variant, variant=variant, options=['One', 'Two', 'Three'], value=['Two'])
      for variant in pmui.MultiPill.param.variant.objects)
)
```

### Colors

Color is applied to the selected pills:


```python
pmui.FlexBox(
    *(pmui.MultiPill(label=color, color=color, options=['One', 'Two'], value=['Two'])
      for color in pmui.MultiPill.param.color.objects)
)
```

### Disabled and Disabled Options

Disable the whole widget or individual options:


```python
pmui.Column(
    pmui.MultiPill(label='Disabled', options=['One', 'Two', 'Three'], value=['Two'], disabled=True),
    pmui.MultiPill(label='Disabled option', options=['One', 'Two', 'Three'], value=['Two'], disabled_options=['Two']),
)
```

Limit the number of selected pills with `max_items`:


```python
pmui.MultiPill(
    label='Top 2',
    value=['Python'],
    options=['Python', 'JavaScript', 'Rust', 'Go'],
    max_items=2,
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.MultiPill(
    label="Modes :material/zoom_out_map:",
    options={
        "Zoom :material/zoom_out_map:": "zoom",
        "Explore :material/explore:": "explore",
    },
    value=["zoom"],
)

```

### Controls

The `MultiPill` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(multipill.controls(jslink=True), multipill)
```
