```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `EditableRangeSlider` widget allows selecting an integer range using a slider with two handles and two input boxes to manually adjust the range.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`end`** (float): The range's upper bound
* **`start`** (float): The range's lower bound
* **`step`** (float): The interval between values
* **`value`** (tuple): Tuple of upper and lower bounds of selected range
* **`value_throttled`** (tuple): Tuple of upper and lower bounds of selected range throttled until mouseup

##### Display

* **`bar_color`** (color): Color of the slider bar as a hexadecimal RGB value.
* **`direction`** (`str`): Whether the slider should go from left to right ('ltr') or right to left ('rtl').
* **`format`** (string): The datetime's format.
* **`inline_layout`** (`boolean`): Whether the editable input fields should be laid out inline with the slider. 
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

The `EditableRangeSlider` widget allows selecting a floating point range tuple in a range defined by the `start` and `end` values:


```python
range_slider = pmui.EditableRangeSlider(
    label='Editable Slider', start=0, end=3.141, step=0.01, value=(0, 1.57)
)

range_slider
```

The `value` of the widget is returned as a tuple of floats and can be accessed and set like any other widget:


```python
range_slider.value
```

### Fixed Range

The slider is bounded by the `start` and `end` values but the text input fields can exceed `end` and go below `start`. If `value` should be fixed to a certain range it can be set with `fixed_start` and `fixed_end`:


```python
pmui.EditableRangeSlider(
    label='Fixed Range', start=0, end=3.141, step=0.01, value=(0, 1.57), fixed_start=-3.14, fixed_end=6.282
)
```

### Format

A custom format string or bokeh `TickFormatter` may be used to format the slider values:


```python
from bokeh.models.formatters import PrintfTickFormatter

str_format = pmui.EditableRangeSlider(label='Distance', format='1[.]00')

tick_format = pmui.EditableRangeSlider(label='Distance', format=PrintfTickFormatter(format='%.2f m'), width=400)

pmui.Column(str_format, tick_format)
```

### Label

You may remove the `label`/ `name` by not setting it.


```python
pmui.EditableRangeSlider()
```

### Show Value

You may remove the value label by setting `show_value=False`.


```python
pmui.EditableRangeSlider(show_value=False)
```

### Disabled

The widget can be disabled with `disabled=True`.


```python
pmui.EditableRangeSlider(label='Range Slider (disabled)', disabled=True)
```

### Inline

The editable text entry fields can be added rendered inline with `inline_layout=True`:


```python
pmui.EditableRangeSlider(label='Range Slider (inline)', inline_layout=True)
```

### Color

You can specify a `color`.


```python
pmui.FlexBox(*(
    pmui.EditableRangeSlider(label=f'Range Slider ({color})', color=color)
    for color in pmui.EditableRangeSlider.param.color.objects
))
```

### Sizes

For smaller slider, use the parameter `size="small"`.


```python
pmui.Row(
    pmui.EditableRangeSlider(label='Length Slider', size="small"),
    pmui.EditableRangeSlider(label='Length Slider', size="medium"),
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

pmui.EditableRangeSlider(marks=marks)
```

### Tooltip always visible

You can force the thumb label to be always visible with `tooltips=True`.


```python
pmui.EditableRangeSlider(label='Length', tooltips=True, value=(53.2, 91.3))
```

### Tracks

The *track* can be inverted or removed with `track="inverted"` and `track=False` respectively:


```python
pmui.Row(
    pmui.EditableRangeSlider(label='Length Slider', value=(53.2, 91.3), track=False),
    pmui.EditableRangeSlider(label='Length Slider', value=(53.2, 91.3), track="inverted")
)
```

### Vertical Sliders

The `orientation` of a slider may be "vertical":


```python
pmui.EditableRangeSlider(label='Length Slider', value=(53.2, 91.3), orientation="vertical")
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.EditableRangeSlider(
    label=":material/zoom_out_map: Scale range",
    start=0,
    end=3.0,
    step=0.1,
    value=(0.5, 2.0),
)
```

### API Reference

The `EditableRangeSlider` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.EditableRangeSlider().api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Slider:**

- [Material UI Slider Reference](https://mui.com/material-ui/react-slider/) - Complete documentation for the underlying Material UI component
- [Material UI Slider API](https://mui.com/material-ui/api/slider/) - Detailed API reference and configuration options
