```python
import datetime as dt

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DateRangePicker` allows selecting a date range using a calendar-based picker with two months displayed side by side. It provides an intuitive way to select start and end dates for filtering, scheduling, or analytics.

The `DateRangePicker` is built on [react-day-picker](https://daypicker.dev/) and styled to integrate with Material UI's theming system.

#### Parameters:

For comprehensive customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (`boolean`, `default=False`): Whether the widget is interactive or read-only.
* **`disabled_dates`** (`list[datetime.date | str]`): Dates to make unavailable for selection.
* **`enabled_dates`** (`list[datetime.date | str]`): Dates to make available for selection; others will be unavailable.
* **`end`** (`datetime.date | str`): The latest selectable date.
* **`format`** (`str`, `default='YYYY-MM-DD'`): The display format of the dates shown in the input field.
* **`start`** (`datetime.date | str`): The earliest selectable date.
* **`value`** (`tuple[datetime.date, datetime.date]`): The selected date range as a tuple of two dates.
* **`value_start`** (`datetime.date`, readonly): The lower value of the selected range.
* **`value_end`** (`datetime.date`, readonly): The upper value of the selected range.

##### Display

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

`DateRangePicker` allows selecting a date range by clicking a start and end date on the calendar:


```python
date_range_picker = pmui.DateRangePicker(
    label='Date Range Picker',
    value=(dt.date(2024, 4, 5), dt.date(2024, 4, 15)),
    start=dt.date(2024, 4, 1),
    end=dt.date(2024, 6, 30)
)

pmui.Row(date_range_picker, height=425)
```

To ensure the calendar dropdown is fully visible in a notebook environment, we've placed it in a `Row` with a fixed height.

The `DateRangePicker.value` returns a tuple of `datetime.date` objects:


```python
date_range_picker.value
```

You can also access the individual bounds via `value_start` and `value_end`:


```python
date_range_picker.value_start, date_range_picker.value_end
```

### Date Range Restrictions

Control the selectable date range by setting `start` and/or `end` parameters:


```python
restricted = pmui.DateRangePicker(
    label='Restricted Range',
    start=dt.date(2024, 4, 1),
    end=dt.date(2024, 4, 30),
    value=(dt.date(2024, 4, 5), dt.date(2024, 4, 20))
)

pmui.Row(restricted, height=425)
```

### Enabled Dates

Use the `enabled_dates` parameter to restrict selection to specific dates only:


```python
enabled = pmui.DateRangePicker(
    label='Only Weekdays',
    enabled_dates=[dt.date(2024, 4, i) for i in range(1, 30) if dt.date(2024, 4, i).weekday() < 5],
    value=(dt.date(2024, 4, 1), dt.date(2024, 4, 5))
)

pmui.Row(enabled, height=425)
```

### Disabled Dates

The `disabled_dates` parameter allows you to exclude specific dates while keeping all others available:


```python
disabled_picker = pmui.DateRangePicker(
    label='No Weekends',
    disabled_dates=[dt.date(2024, 4, i) for i in range(1, 30) if dt.date(2024, 4, i).weekday() >= 5],
    value=(dt.date(2024, 4, 1), dt.date(2024, 4, 12))
)

pmui.Row(disabled_picker, height=425)
```

### Date Format Display

Customize how dates appear in the input field using the `format` parameter:


```python
pmui.Row(
    pmui.DateRangePicker(label='Custom Format', value=(dt.date(2024, 4, 1), dt.date(2024, 4, 15)), format='MM/DD/YYYY'),
    height=425
)
```

### Color Options

The `color` parameter allows you to visually distinguish the `DateRangePicker` component:


```python
pmui.FlexBox(
    *[pmui.DateRangePicker(label=color, value=(dt.date(2024, 4, 1), dt.date(2024, 4, 15)), color=color)
      for color in ['primary', 'secondary', 'error', 'info', 'success', 'warning']],
    pn.Spacer(height=425)
)
```

### Variant Styles

The `variant` parameter controls the visual appearance of the input field:


```python
pmui.FlexBox(
    pmui.DateRangePicker(label='Filled', value=(dt.date(2024, 4, 1), dt.date(2024, 4, 15)), variant='filled'),
    pmui.DateRangePicker(label='Outlined', value=(dt.date(2024, 4, 1), dt.date(2024, 4, 15)), variant='outlined'),
    pmui.DateRangePicker(label='Standard', value=(dt.date(2024, 4, 1), dt.date(2024, 4, 15)), variant='standard'),
)
```

### Disabled State

The widget can be disabled with `disabled=True`:


```python
pmui.DateRangePicker(label='Disabled', value=(dt.date(2024, 4, 1), dt.date(2024, 4, 15)), disabled=True)
```

### API Reference

#### Parameters


```python
date_range_picker.api(jslink=False)
```

### References

**Panel Documentation:**
- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**react-day-picker:**
- [react-day-picker Documentation](https://daypicker.dev/) - Complete documentation for the underlying calendar component
