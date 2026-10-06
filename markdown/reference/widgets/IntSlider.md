```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `IntSlider` widget allows selecting selecting an integer value within a set bounds using a slider.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`end`** (int): The range's upper bound
* **`start`** (int): The range's lower bound
* **`step`** (int): The interval between values
* **`value`** (int): The selected value as an int type
* **`value_throttled`** (int): The selected value as a int type throttled until mouseup

##### Display

* **`bar_color`** (color): Color of the slider bar as a hexadecimal RGB value.
* **`direction`** (`str`): Whether the slider should go from left to right ('ltr') or right to left ('rtl').
* **`format`** (string): The datetime's format
* **`label`** (`str`): The title of the widget.
* **`marks`** (`boolean | list[dict]`):  Marks indicate predetermined values to which the user can move the slider. If True the `options` are shown as marks. If a list, it should contain dicts with 'value' and an optional 'label' keys.
* **`orientation`** (`Literal["horizonta", "vertical"]`): Whether the slider should be displayed in a 'horizontal' or 'vertical' orientation.
* **`show_value`** (`boolean`): Whether to show the widget value as a label or not. 
* **`tooltips`** (`boolean | Literal["auto"]`): Whether to display tooltips on the slider handle.
* **`track`** (`Literal["normal", "inverted"]`): Whether to display 'normal' or 'inverted'.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

The `IntSlider` widget allows selecting a integer `value` in a range defined by the `start` and `end` values:


```python
int_slider = pmui.IntSlider(label='Integer Slider', start=0, end=8, step=2, value=4)

int_slider
```

The ``IntSlider`` value is returned as a integer and can be accessed and set like any other widget:


```python
int_slider.value
```

### Format

A custom format string or bokeh `TickFormatter` may be used to format the slider values:


```python
from bokeh.models.formatters import PrintfTickFormatter

str_format = pmui.IntSlider(label='Rank', format='0o', start=0, end=100)

tick_format = pmui.IntSlider(label='Count', format=PrintfTickFormatter(format='%d ducks'), start=0, end=100)

pmui.Column(str_format, tick_format)
```

### Label

You may remove the `label`/ `name` by not setting it.


```python
pmui.IntSlider()
```

### Show Value

You may remove the value label by setting `show_value=False`.


```python
pmui.IntSlider(show_value=False)
```

### Disabled

The widget can be disabled with `disabled=True`.


```python
pmui.IntSlider(label='Int Slider (disabled)', disabled=True)
```

### Color

You can specify a `color`.


```python
pmui.FlexBox(*(
    pmui.IntSlider(label=f'Float Slider ({color})', color=color)
    for color in pmui.IntSlider.param.color.objects
))
```

### Sizes

For smaller slider, use the parameter `size="small"`.


```python
pmui.Row(
    pmui.IntSlider(label='Age Slider', size="small"),
    pmui.IntSlider(label='Age Slider', size="medium"),
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
    "value": 30,
    "label": '30°C',
  },
  {
    "value": 60,
    "label": '60°C',
  },
  {
    "value": 100,
    "label": '100°C',
  },
]

pmui.IntSlider(marks=marks)
```

### Tooltip always visible

You can force the thumb label to be always visible with `tooltips=True`.


```python
pmui.IntSlider(label='Age', tooltips=True, value=42)
```

### Tracks

The *track* can be inverted or removed with `track="inverted"` and `track=False` respectively:


```python
pmui.Row(
    pmui.IntSlider(label='Age Slider', value=42, track="inverted"),
    pmui.IntSlider(label='Age Slider', value=42, track=False)
)
```

### Vertical Sliders

The `orientation` of a slider may be "vertical":


```python
pmui.IntSlider(label='Age Slider', value=42, orientation="vertical")
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.IntSlider(label="Zoom :material/zoom_out_map:", start=0, end=10, value=4)
```

### API Reference

The `IntSlider` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.IntSlider(label='IntSlider').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Slider:**

- [Material UI Slider Reference](https://mui.com/material-ui/react-slider/) - Complete documentation for the underlying Material UI component
- [Material UI Slider API](https://mui.com/material-ui/api/slider/) - Detailed API reference and configuration options
