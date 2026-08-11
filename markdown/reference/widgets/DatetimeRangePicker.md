```python
import datetime as dt

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DatetimeRangePicker` allows selecting a datetime range using a calendar-based picker with two months displayed side by side and time inputs for the start and end times. It extends the `DateRangePicker` with time selection capabilities.

The `DatetimeRangePicker` is built on [react-day-picker](https://daypicker.dev/) and styled to integrate with Material UI's theming system.

#### Parameters:

For comprehensive customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (`boolean`, `default=False`): Whether the widget is interactive or read-only.
* **`disabled_dates`** (`list[datetime.date | str]`): Dates to make unavailable for selection.
* **`enable_seconds`** (`boolean`, `default=True`): Enable editing of seconds in the time inputs.
* **`enabled_dates`** (`list[datetime.date | str]`): Dates to make available for selection; others will be unavailable.
* **`end`** (`datetime.datetime | str`): The latest selectable datetime.
* **`format`** (`str`): The display format of the datetimes shown in the input field. Auto-set based on `military_time`.
* **`military_time`** (`boolean`, `default=True`): Whether to display time in 24-hour format.
* **`start`** (`datetime.datetime | str`): The earliest selectable datetime.
* **`value`** (`tuple[datetime.datetime, datetime.datetime]`): The selected datetime range as a tuple.
* **`value_start`** (`datetime.date`, readonly): The lower value of the selected range.
* **`value_end`** (`datetime.date`, readonly): The upper value of the selected range.

##### Display

* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The descriptive text displayed above the input field.

##### Styling

- **`color`** (str): Visual theme color. Choose from "default" (default), "primary", "secondary", "error", "info", "success", "warning", "light", "dark", or "danger".
- **`sx`** (dict): Component-level styling API for fine-grained customization.
- **`theme_config`** (dict): Theming API for consistent design system integration.
- **`variant`** (str): Input field style variant. Choose from "filled", "outlined" (default), or "standard".

##### Aliases

For compatibility with existing Panel code, certain parameters have aliases:

- **`name`**: Alias for `label`

___

`DatetimeRangePicker` allows selecting a datetime range by clicking dates and setting times:


```python
datetime_range_picker = pmui.DatetimeRangePicker(
    label='Datetime Range Picker',
    value=(dt.datetime(2024, 4, 5, 9, 0), dt.datetime(2024, 4, 15, 17, 30)),
    start=dt.datetime(2024, 4, 1),
    end=dt.datetime(2024, 6, 30),
    width=400
)

pmui.Row(datetime_range_picker, height=475)
```

The `DatetimeRangePicker.value` returns a tuple of `datetime.datetime` objects:


```python
datetime_range_picker.value
```

### Military Time

By default, the time inputs use 24-hour format. Set `military_time=False` for 12-hour (AM/PM) display:


```python
ampm_picker = pmui.DatetimeRangePicker(
    label='12-Hour Format',
    value=(dt.datetime(2024, 4, 5, 9, 0), dt.datetime(2024, 4, 15, 17, 30)),
    military_time=False
)

pmui.Row(ampm_picker, height=475)
```

### Enable Seconds

Control whether seconds are editable with `enable_seconds`:


```python
no_seconds = pmui.DatetimeRangePicker(
    label='Without Seconds',
    value=(dt.datetime(2024, 4, 5, 9, 0), dt.datetime(2024, 4, 15, 17, 30)),
    enable_seconds=False
)

pmui.Row(no_seconds, height=475)
```

### Date Range Restrictions

Control the selectable date range by setting `start` and/or `end` parameters:


```python
restricted = pmui.DatetimeRangePicker(
    label='Restricted Range',
    start=dt.datetime(2024, 4, 1),
    end=dt.datetime(2024, 4, 30, 23, 59, 59),
    value=(dt.datetime(2024, 4, 5, 8, 0), dt.datetime(2024, 4, 20, 18, 0))
)

pmui.Row(restricted, height=475)
```

### Color Options

The `color` parameter allows you to visually distinguish the `DatetimeRangePicker` component:


```python
pmui.FlexBox(
    *[pmui.DatetimeRangePicker(
        label=color,
        value=(dt.datetime(2024, 4, 1, 9, 0), dt.datetime(2024, 4, 15, 17, 0)),
        color=color
    ) for color in ['primary', 'secondary', 'error', 'info', 'success', 'warning']],
    pn.Spacer(height=475)
)
```

### Variant Styles

The `variant` parameter controls the visual appearance of the input field:


```python
pmui.FlexBox(
    pmui.DatetimeRangePicker(label='Filled', value=(dt.datetime(2024, 4, 1, 9, 0), dt.datetime(2024, 4, 15, 17, 0)), variant='filled'),
    pmui.DatetimeRangePicker(label='Outlined', value=(dt.datetime(2024, 4, 1, 9, 0), dt.datetime(2024, 4, 15, 17, 0)), variant='outlined'),
    pmui.DatetimeRangePicker(label='Standard', value=(dt.datetime(2024, 4, 1, 9, 0), dt.datetime(2024, 4, 15, 17, 0)), variant='standard'),
)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.DatetimeRangePicker(label='Period', helper_text='Select start and end datetimes')
```

### Disabled State

The widget can be disabled with `disabled=True`:


```python
pmui.DatetimeRangePicker(
    label='Disabled',
    value=(dt.datetime(2024, 4, 1, 9, 0), dt.datetime(2024, 4, 15, 17, 0)),
    disabled=True
)
```

### API Reference

#### Parameters


```python
datetime_range_picker.api(jslink=False)
```

### References

**Panel Documentation:**
- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**react-day-picker:**
- [react-day-picker Documentation](https://daypicker.dev/) - Complete documentation for the underlying calendar component
