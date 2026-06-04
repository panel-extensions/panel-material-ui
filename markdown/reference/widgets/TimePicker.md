```python
import datetime as dt

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `TimePicker` widget allows entering a time value as text or `datetime.time`. 

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **``disabled``** (boolean): Whether the widget is editable
* **`end`** (str | datetime.time): Inclusive upper bound of the allowed time selection
* **`start`** (str | datetime.time): Inclusive lower bound of the allowed time selection
* **`value`** (str | datetime.time): The current value

##### Display

* **`clock`** (str): Whether to use 12 hour or 24 hour clock. Default is `'12h'`.
* **`format`** (str): Formatting specification for the display of the picked date.
    ```
    +----+------------------------------------+------------+
    | H  | Hours                              | 0 to 23    |
    | HH | Hours, 2-digits                    | 00 to 23   |
    | h  | Hours, 12-hour clock               | 1 to 12    |
    | hh | Hours, 12-hour clock, 2-digits     | 1 to 12    |
    | m  | Minutes                            | 0 to 59    |
    | mm | Minutes                            | 00 to 59   |
    | s  | Seconds                            | 0, 1 to 59 |
    | ss | Seconds                            | 00 to 59   |
    | a  | am/pm, lower-case                  | am or pm   |
    | A  | AM/PM, upper-cas                   | AM or PM   |
    +----+------------------------------------+------------+
    ```
    See also https://day.js.org/docs/en/parse/string-format.
* **`hour_increment`** (int): The time steps between two hour options. Default is 1.
* **`minute_increment`** (int): The time steps between two minure options. Default is 1.
* **`mode`** (`Literal["digital", "analog", "auto"]`): Whether to render a digital or analog clock. By default automatically switches between digital clock on desktop to analog clock on mobile.
* **`label`** (str): The title of the widget
* **`second_increment`** (int): The time steps between two second options. Default is 1.
* **`seconds`** (bool): Allows to select seconds. By default, only hours and minutes are selectable, and AM/PM depending on the `clock` option. Default is False.

##### Styling

- **`color`** (str): A color variant `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.
* **`variant`** (`Literal["filled", "outlined", "standard"]`): The variant of the input field.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

##### Unsupported

Options implemented by the `panel.widgets.TimePicker` widget but not `panel_material_ui.TimePicker`:

- **`hour_step`** (int): Defines the granularity of hour value increments in the UI.
- **`minute_step`** (int): Defines the granularity of minute value increments in the UI.
- **`seconds_step`** (int): Defines the granularity of second value increments in the UI.

___

### Basic Usage

The `TimePicker` widget allows selecting a time of day.


```python
time_picker = pmui.TimePicker(label='Time Picker', value=dt.datetime.now().time())

pmui.Column(time_picker, height=400)
```

Either `datetime.time` or `str` can be used as input and `TimePicker` can be bounded by a start and end time.


```python
time_picker = pmui.TimePicker(label='Time Picker', value="08:25", start='00:00', end='12:00')

pmui.Column(time_picker, height=380)
```

### 24-hour Clock

By default the `TimePicker` uses a 12-hour clock picker, but this may be changed to a '24h' clock.


```python
time_picker_12 = pmui.TimePicker(
    label='Time Picker (12h)', value="08:28", start='00:00', end='12:00', clock='12h'
)
time_picker_24 = pmui.TimePicker(
    label='Time Picker (24h)', value="08:28", start='00:00', end='12:00', clock='24h'
)

pmui.Row(time_picker_12, time_picker_24, height=380)
```

### Format

The formatting of the text field can be set independently from the clock. It follows the [day.js](https://day.js.org/docs/en/parse/string-format) string formatting options


```python
time_picker_leading_zero = pmui.TimePicker(
    label='Time Picker', value="08:28", start='00:00', end='12:00', format="HH:MM:ss", seconds=True
)
time_picker_no_zeros = pmui.TimePicker(
    label='Time Picker', value="08:28", start='00:00', end='12:00', format="H:M:s", seconds=True
)

pmui.Row(time_picker_leading_zero, time_picker_no_zeros, height=380)
```

### Mode

By default the `TimePicker` will render as a digital clock on desktop environments and switch to a clock popup in mobile environments.

To switch explicitly switch between the two set the `mode`:


```python
pmui.FlexBox(
    pmui.TimePicker(label='Analog', mode="analog"),
    pmui.TimePicker(label='Digital', mode="digital"),
    height=360
)
```

### Color Options

You can set the `color` parameter to visually distinguish the `TimePicker` when active. Available options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":


```python
pmui.FlexBox(
    *[pmui.TimePicker(label=color, color=color) for color in pmui.TimePicker.param.color.objects]
)
```

### Variant

The `variant` parameter controls the visual style of the input. Choose from "filled", "outlined" (default), or "standard":


```python
pmui.FlexBox(
    pmui.TimePicker(label='Filled', variant="filled"),
    pmui.TimePicker(label='Outlined', variant="outlined"),
    pmui.TimePicker(label='Standard', variant="standard"),
    height=360
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_label_picker = pmui.TimePicker(label=":material/zoom_out_map: Meeting time", value="09:30")

icon_label_picker
```

### API Reference

The `TimePicker` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.TimePicker(label='TimePicker').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI TimePicker:**

- [Material UI TimePicker Reference](https://mui.com/x/api/date-pickers/date-time-picker/) - Complete documentation for the underlying Material UI component
- [Material UI TimePicker API](https://mui.com/x/api/date-pickers/date-time-picker/) - Detailed API reference and configuration options
