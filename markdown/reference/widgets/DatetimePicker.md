```python
import datetime as dt

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DatetimePicker` widget allows selecting selecting a datetime value using a text box and the browser's datetime-picking utility.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`clearable`** (`boolean`, `default=False`): If true, allows the date to be cleared.
* **`disabled`** (`boolean`, `default=False`): Whether the widget is editable
* **`disabled_dates`** (`list[datetime.date | datetime.datetime | str]`): dates to make unavailable for selection; others will be available. Specified as list of `datetime`, `date` or `str` objects in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`disable_future`** (`boolean`): If true, future dates are disabled.
* **`disable_past`** (`boolean`): If true, past dates are disabled.
* **`enabled_dates`** (`list[datetime.date | datetime.datetime | str]`): Dates to make available for selection; others will be unavailable. Specified as list of `datetime`, `date` or `str` objects in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`enable_time`** (`boolean`): Enable editing of the time in the widget, default is True
* **`enable_seconds`** (`boolean`): Enable editing of seconds in the widget, default is True
* **`end`** (`datetime.date | datetime.datetime | str`): Inclusive upper bound of the allowed date selection as a `datetime` or `str` in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`format`** (`str`):The format of the datetime displayed in the input (by default depends on `military_time`).
* **`military_time`** (`boolean`): Enable 24 hours time in the widget, default is True
* **`start`** (`datetime.datetime | datetime.date | str`): Inclusive lower bound of the allowed date selection as a datetime or `str` in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`value`** (`datetime.datetime | datetime.date | str`): The selected value as a `datetime` or `str` in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). Always returns a `datetime` object.

##### Display

* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The title of the widget
* **`visible`** (boolean): Whether the widget is visible

##### Styling

- **`color` (str)**: Choose from "default" (default), "primary", "secondary", "error", "info", "success", "warning", "light", "dark", or "danger".
- **`sx`** (dict): Component-level styling options.
- **`theme_config`** (dict): Theming options.
- **`variant`** (str): Choose from "filled", "outlined" (default), or "standard".

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`

___

### Basic Usage

`DatetimePicker` allows selecting a date and time. The datetime can be provided as a datetime object or as an ISO string and supports optional `start` and `end` bounds:


```python
datetime_picker = pmui.DatetimePicker(
    label='Datetime Picker', value=dt.datetime(2021, 3, 2, 12, 10), start='2021-03-01 00:00', end='2021-03-31 00:00'
)

pmui.Column(datetime_picker, height=450)
```

To ensure it is visible in a notebook we have placed it in a `Column` with a fixed height.

`DatetimePicker.value` always returns a `datetime` type that can be read out or set like other widgets:


```python
datetime_picker.value
```

### Time format

The time format is controlled by the `format` and `military_time` options. The former controls how the time is displayed once selected while the latter controls whether the picker displays a 12 hour or 24 hour clock:


```python
datetime_12h = pmui.DatetimePicker(
    label='Datetime Picker', military_time=False, value=dt.datetime(2021, 3, 2, 12, 10)
)

datetime_24h = pmui.DatetimePicker(
    label='Datetime Picker', military_time=False, value=dt.datetime(2021, 3, 2, 12, 10), format='YY-MM-DD hh:mm a'
)

datetime_seconds = pmui.DatetimePicker(
    label='Datetime Picker', enable_seconds=True, value=dt.datetime(2021, 3, 2, 12, 10, 32)
)

pmui.Row(datetime_picker, datetime_24h, datetime_seconds, height=450)
```

### Limiting to a calendar range

The range of selectable dates can be limited by setting `start` and/or `end`:


```python
dt_picker = pmui.DatetimePicker(
    label='Date Time Picker',
    start=dt.datetime(2024, 4, 1, 0, 0),
    end=dt.datetime(2024, 4, 7, 0, 0),
    value=dt.datetime(2024, 4, 1, 11, 37)
)

pmui.Row(dt_picker, height=400)
```

### Disable Past or Future

The `disable_past` and `disable_future` options make it easy to limit the selectable dates:


```python
disable_past = pmui.DatetimePicker(
    disable_past=True,
    label='Date Time Picker (disable_past)',
)

disable_future = pmui.DatetimePicker(
    disable_future=True,
    label='Date Time Picker (disable_future)',
)

pmui.Row(disable_past, disable_future, height=400)
```

### Enabled Dates

The `enabled_dates` option allows limiting the dates that can be selected to a specific subset:


```python
date_picker = pmui.DatetimePicker(
    label='Date Time Picker (enabled_dates)',
    enabled_dates=[dt.datetime(2024, 4, i, 12, 37) for i in range(1, 7)],
    value=dt.datetime(2024, 4, 1, 11, 37)
)

pmui.Column(date_picker, height=400)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.DatetimePicker(label='Event', helper_text='Select date and time')
```

### Disabled Dates

The `disabled_dates` option allows excluding specific dates:


```python
date_picker = pmui.DatetimePicker(
    label='Date Time Picker (disabled_dates)',
    disabled_dates=[dt.datetime(2024, 4, i, 12, 37) for i in range(2, 7)],
    value=dt.datetime(2024, 4, 1, 11, 37)
)

pmui.Column(date_picker, height=400)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_datetime_picker = pmui.DatetimePicker(
    label=":material/event: Schedule",
    value=dt.datetime(2021, 3, 2, 12, 10),
)

icon_datetime_picker
```

### Controls

The `DatetimePicker` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(datetime_picker.api(jslink=True), datetime_picker)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI DatetimePicker:**

- [Material UI TimePicker Reference](https://mui.com/x/api/date-pickers/date-time-picker/) - Complete documentation for the underlying Material UI component
- [Material UI TimePicker API](https://mui.com/x/api/date-pickers/date-time-picker/) - Detailed API reference and configuration options
