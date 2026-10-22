```python
import datetime as dt

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DateSlider` widget allows selecting selecting a date value within a set bounds using a slider.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`as_datetime`**: Whether to return value as a date (default) or datetime
* **`disabled`** (boolean): Whether the widget is editable
* **`start`** (date or datetime): The range's lower bound
* **`step`** (integer): The selected step i the slider in days
* **`end`** (date or datetime): The range's upper bound
* **`value`** (date or datetime): The selected value as a datetime type
* **`value_throttled`** (datetime): The selected value as a datetime type throttled until mouseup

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


```python
date_slider = pmui.DateSlider(label='Date Slider', start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))

date_slider
```

``DateSlider.value`` returns a datetime type that can be read out or set like other widgets:


```python
date_slider.value
```

### Label

You may remove the `label`/ `name` by not setting it.


```python
pmui.DateSlider(start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))
```

### Show Value

You may remove the value label by setting `show_value=False`.


```python
pmui.DateSlider(start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8), show_value=False, label='DateSlider')
```

### Disabled

The widget can be disabled with `disabled=True`.


```python
pmui.DateSlider(label='Date Slider (disabled)', disabled=True, start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))
```

### Color

You can specify a `color`.


```python
pmui.FlexBox(*(
    pmui.DateSlider(label=f'Date Slider ({color})', color=color, start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))
    for color in pmui.DateSlider.param.color.objects
))
```

### Sizes

For smaller slider, use the parameter `size="small"`.


```python
pmui.Row(
    pmui.DateSlider(label='Date Slider', size="small", start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8)),
    pmui.DateSlider(label='Date Slider', size="medium", start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8)),
)
```

### Custom Marks

You can have custom marks by providing a rich list to the `marks` parameter. Note that unlike continuous sliders the `value` of the marks should be the integer index of the option.


```python
marks = [
  {
    "value": dt.datetime(2019, 1, 1),
    "label": "01/01",
  },
  {
    "value": dt.datetime(2019, 3, 1),
    "label": "03/01",
  },
  {
    "value": dt.datetime(2019, 5, 1),
    "label": "05/01",
  },
  {
    "value": dt.datetime(2019, 6, 1),
    "label": "06/01",
  }  
]

pmui.DateSlider(marks=marks, start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))
```

### Tooltip always visible

You can force the thumb label to be always visible with `tooltips=True`.


```python
pmui.DateSlider(
    label='Date', tooltips=True, start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8)
)
```

### Tracks

The *track* can be inverted or removed with `track="inverted"` and `track=False` respectively:


```python
pmui.Row(
    pmui.DateSlider(label='Date Slider', track=False, start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8)),
    pmui.DateSlider(label='Date Slider', track="inverted", start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))
)
```

### Vertical Sliders

The `orientation` of a slider may be "vertical":


```python
pmui.DateSlider(label='Date Slider', orientation="vertical", start=dt.datetime(2019, 1, 1), end=dt.datetime(2019, 6, 1), value=dt.datetime(2019, 2, 8))
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_date_slider = pmui.DateSlider(
    label=":material/today: Date",
    start=dt.datetime(2019, 1, 1),
    end=dt.datetime(2019, 6, 1),
    value=dt.datetime(2019, 2, 8),
)

icon_date_slider
```

### Controls

The `DateSlider` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(date_slider.api(jslink=True), date_slider)
```

### References

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html).

Learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

See also the Material UI `DateSlider` [Reference](https://mui.com/material-ui/react-slider/) and [API](https://mui.com/material-ui/api/slider/) documentation for inspiration.
