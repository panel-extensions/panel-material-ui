```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DiscreteSlider` widget allows users to select a value from a discrete list or dictionary of values using a slider. Its built upon the [Material UI Slider](https://mui.com/material-ui/react-slider/) component.

It falls into the broad category of single-value, option-selection widgets that provide a compatible API and include the [`AutocompleteInput`](AutocompleteInput.ipynb), and [`Select`](Select.ipynb) widgets.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (`boolean`): Whether the widget is editable.
* **`options`** (`list | dict`): A list or dictionary of options to select from.
* **`value`** (`object`): The current value; must be one of the option values. Updated when the *handle* is dragged. 
* **`value_throttled`** (`object`): The current value; must be one of the option values. Updated when the *handle* is released.

##### Display

* **`bar_color`** (color): Color of the slider bar as a hexadecimal RGB value.
* **`direction`** (`str`): Whether the slider should go from left to right ('ltr') or right to left ('rtl').
* **`formatter`** (`str`): A custom Python format string. Default is '%.3g'.
* **`label`** (`str`): The title of the widget.
* **`marks`** (`boolean | list[dict]`):  Marks indicate predetermined values to which the user can move the slider. If True the `options` are shown as marks. If a list, it should contain dicts with 'value' and an optional 'label' keys.
* **`orientation`** (`Literal["horizontal", "vertical"]`): Whether the slider should be displayed in a 'horizontal' or 'vertical' orientation.
* **`show_value`** (`boolean`): Whether to show the widget value as a label or not. 
* **`tooltips`** (`boolean | Literal["auto"]`): Whether to display tooltips on the slider handle.
* **`track`** (`Literal["normal", "inverted"]`): Whether to display 'normal' or 'inverted'.

##### Styling

- **`sx`** (`dict`): Component level styling API.
- **`theme_config`** (`dict`): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

The `DiscreteSlider` allow users to select a value from a discrete range.


```python
slider = pmui.DiscreteSlider(label='Age', options=['Ten', 'Twenty', 'Thirty'])

slider
```

Like most other widgets, ``DiscreteSlider`` has a value parameter that can be accessed or set:


```python
slider.value
```

The `options` parameter also accepts a dictionary whose keys are going to be the labels of the slider. 


```python
value_slider = pmui.DiscreteSlider(label='Age', options={'Ten': 10, 'Twenty': 20, 'Thirty': 30})

value_slider
```

In this scenario the `value` will reflect the value of the item in the `options` dictionary:


```python
value_slider.value
```

### Label

You may remove the `label`/ `name` by not setting it.


```python
pmui.DiscreteSlider(options=['Ten', 'Twenty', 'Thirty'])
```

### Show Value

You may remove the value label by setting `show_value=False`.


```python
pmui.DiscreteSlider(label='Age', options=['Ten', 'Twenty', 'Thirty'], value='Twenty', show_value=False)
```

### Disabled

The widget can be disabled with `disabled=True`.


```python
pmui.DiscreteSlider(label='Age', options=['Ten', 'Twenty', 'Thirty'], disabled=True)
```

### Color

You can specify a `color`.


```python
pmui.DiscreteSlider(label="Age", options=['Ten', 'Twenty', 'Thirty'], color="secondary")
```

### Sizes

For smaller slider, use the parameter `size="small"`.


```python
pmui.Row(
    pmui.DiscreteSlider(label='Age Slider', options=['Ten', 'Twenty', 'Thirty'], size="small"),
    pmui.DiscreteSlider(label='Age Slider', options=['Ten', 'Twenty', 'Thirty'], size="medium"),
)
```

### Custom Marks

You can have custom marks by providing a rich list to the `marks` parameter. Note that unlike continuous sliders the `value` of the marks should be the integer index of the option.


```python
marks = [
  {
    "value": 0,
    "label": '0°C',
  },
  {
    "value": 1,
    "label": '20°C',
  },
  {
    "value": 2,
    "label": '37°C',
  },
  {
    "value": 3,
    "label": '100°C',
  },
]

pmui.DiscreteSlider(options=[0, 20, 37, 100], marks=marks)
```

### Label always visible

You can force the thumb label to be always visible with `tooltips=True`.


```python
pmui.DiscreteSlider(label='Age', options=['Ten', 'Twenty', 'Thirty'], value='Twenty', tooltips=True)
```

### Tracks

The *track* can be inverted or removed with `track="inverted"` and `track=False` respectively:


```python
pmui.Row(
    pmui.DiscreteSlider(label='Age Slider', options=['Ten', 'Twenty', 'Thirty'], value='Twenty', track=False),
    pmui.DiscreteSlider(label='Age Slider', options=['Ten', 'Twenty', 'Thirty'], value='Twenty', track="inverted")
)
```

### Vertical Sliders


```python
pmui.DiscreteSlider(label='Age Slider', options=['Ten', 'Twenty', 'Thirty'], value='Twenty', orientation="vertical")
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_discrete_slider = pmui.DiscreteSlider(
    label=":material/tune: Priority",
    options={
        ":material/looks_one: Low": 1,
        ":material/looks_two: Medium": 2,
        ":material/looks_3: High": 3,
    },
    value=2,
)

icon_discrete_slider
```

### API Reference

The `DiscreteSlider` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.DiscreteSlider(options=['Ten', 'Twenty', 'Thirty']).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Slider:**

- [Material UI Slider Reference](https://mui.com/material-ui/react-slider/) - Complete documentation for the underlying Material UI component
- [Material UI Slider API](https://mui.com/material-ui/api/slider/) - Detailed API reference and configuration options
