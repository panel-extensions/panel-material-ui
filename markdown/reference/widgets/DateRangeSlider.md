```python
import datetime as dt

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DateRangeSlider` widget allows selecting a date range using a slider with two handles.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`start`** (datetime): The range's lower bound
* **`end`** (datetime): The range's upper bound
* **`step`** (int): Step in days
* **`value`** (tuple): Tuple of upper and lower bounds of the selected range expressed as datetime types
* **`value_throttled`** (tuple): Tuple of upper and lower bounds of the selected range expressed as datetime types throttled until mouseup

##### Display

* **`bar_color`** (color): Color of the slider bar as a hexadecimal RGB value
* **`direction`** (str): Whether the slider should go from left to right ('ltr') or right to left ('rtl')
* **`format`** (str): The datetime format
* **`label`** (str): The title of the widget
* **`orientation`** (str): Whether the slider should be displayed in a 'horizontal' or 'vertical' orientation.
* **`tooltips`** (boolean): Whether to display tooltips on the slider handle

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

The slider start and end can be adjusted by dragging the handles and whole range can be shifted by dragging the selected range.


```python
date_range_slider = pmui.DateRangeSlider(
    label='Date Range Slider',
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
    step=2
)

date_range_slider
```

``DateRangeSlider.value`` returns a tuple of datetime values that can be read out and set like other widgets:


```python
date_range_slider.value
```

### Label

You may remove the `label`/ `name` by not setting it.


```python
pmui.DateRangeSlider(
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
)
```

### Show Value

You may remove the value label by setting `show_value=False`.


```python
pmui.DateRangeSlider(
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
    show_value=False, label='DateRangeSlider'
)
```

### Disabled

The widget can be disabled with `disabled=True`.


```python
pmui.DateRangeSlider(
    label='Date Range Slider (disabled)', disabled=True,
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10))
)
```

### Color

You can specify a `color`.


```python
pmui.FlexBox(*(
    pmui.DateRangeSlider(
        label=f'Date Range Slider ({color})', color=color,
        start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
        value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
    )
    for color in pmui.DateRangeSlider.param.color.objects
))
```

### Sizes

For smaller slider, use the parameter `size="small"`.


```python
pmui.Row(
    pmui.DateRangeSlider(
        label='Date Range Slider', size="small",
        start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
        value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10))
    ),
    pmui.DateRangeSlider(
        label='Date Range Slider', size="medium",
        start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
        value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10))
    ),
)
```

### Custom Marks

You can have custom marks by providing a rich list to the `marks` parameter. Note that unlike continuous sliders the `value` of the marks should be the integer index of the option.


```python
marks = [
  {
    "value": dt.datetime(2017, 1, 1),
    "label": "01/01",
  },
  {
    "value": dt.datetime(2017, 3, 1),
    "label": "03/01",
  },
  {
    "value": dt.datetime(2017, 5, 1),
    "label": "05/01",
  },
  {
    "value": dt.datetime(2017, 12, 1),
    "label": "12/01",
  }  
]

pmui.DateRangeSlider(
    marks=marks, start=dt.datetime(2017, 1, 1), end=dt.datetime(2018, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10))
)
```

### Tooltip always visible

You can force the thumb label to be always visible with `tooltips=True`.


```python
pmui.DateRangeSlider(
    label='Date', tooltips=True,
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
)
```

### Tracks

The *track* can be inverted or removed with `track="inverted"` and `track=False` respectively:


```python
pmui.Row(
    pmui.DateRangeSlider(
        label='Date Range Slider', track=False,
        start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
        value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
    ),
    pmui.DateRangeSlider(
        label='Date Range Slider', track="inverted",
        start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
        value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
    )
)
```

### Vertical Sliders

The `orientation` of a slider may be "vertical":


```python
pmui.DateRangeSlider(
    label='Date Range Slider', orientation="vertical",
    start=dt.datetime(2017, 1, 1), end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10))
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_date_range_slider = pmui.DateRangeSlider(
    label=":material/date_range: Range",
    start=dt.datetime(2017, 1, 1),
    end=dt.datetime(2019, 1, 1),
    value=(dt.datetime(2017, 1, 1), dt.datetime(2018, 1, 10)),
)

icon_date_range_slider
```

### Controls

The `DateRangeSlider` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(date_range_slider.api(jslink=True), date_range_slider)
```

### References

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html).

Learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

See also the Material UI `DateRangeSlider` [Reference](https://mui.com/material-ui/react-slider/) and [API](https://mui.com/material-ui/api/slider/) documentation for inspiration.
