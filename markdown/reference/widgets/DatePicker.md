```python
import datetime as dt

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DatePicker` component provides an intuitive interface for date selection in your Panel applications. Whether you're building scheduling interfaces, data filtering controls, or time-based analytics dashboards, the DatePicker offers a polished and accessible solution for date input.

The `DatePicker` component is built on the powerful [Material UI `DatePicker`](https://mui.com/x/react-date-pickers/date-picker/), ensuring a consistent and professional user experience across all platforms.

#### Parameters:

For comprehensive customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`clearable`** (`boolean`, `default=False`): Whether users can clear the selected date, returning the value to `None`.
* **`disabled`** (`boolean`, `default=False`): Whether the widget is interactive or read-only.
* **`disabled_dates`** (`list[datetime.date | datetime.datetime | str]`): dates to make unavailable for selection; others will be available. Specified as list of `datetime`, `date` or `str` objects in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`disable_future`** (`boolean`): When `True`, prevents selection of future dates.
* **`disable_past`** (`boolean`): When `True`, prevents selection of past dates.
* **`enabled_dates`** (`list[datetime.date | datetime.datetime | str]`): Dates to make available for selection; others will be unavailable. Specified as list of `datetime`, `date` or `str` objects in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`format`** (`str`, `default='YYYY-MM-DD'`): The display format of the date shown in the input field.
* **`end`** (`datetime.date | datetime.date | str`): The latest selectable date in the calendar range  as a `date` or `datetime` object or `str` in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`open_to`** (`str`): The default calendar view to display when opened (e.g., 'year', 'month', 'day').
* **`show_today_button`** (`boolean`, `default=False`): Whether to display a "Today" button for quick date selection.
* **`start`** (`datetime.date | datetime.date | str`): The earliest selectable date in the calendar range as a `date` or `datetime` object or `str` in [ISO format](https://en.wikipedia.org/wiki/ISO_8601).
* **`value`** (`datetime.date | datetime.date | str`): The currently selected date as a `date` or `datetime` object or `str` in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). Always returns a `date` object.
* **`views`** (`list[str]`, `default=['year', 'month', 'day']`): Available calendar views for navigation and selection.

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

`DatePicker` allows selecting a date. The date can be provided as a `date` or `datetime` object or as an ISO string:


```python
date_picker = pmui.DatePicker(label='Date Picker', value=dt.date(2024, 4, 14), start="2024-04-01")

pmui.Row(date_picker, height=425)
```

To ensure the calendar dropdown is fully visible in a notebook environment, we've placed it in a `Row` with a fixed height.

The `DatePicker.value` always returns a `datetime.date` object that can be read or programmatically set like other Panel widgets:


```python
date_picker.value
```

### Date Range Restrictions

Control the selectable date range by setting `start` and/or `end` parameters. This is particularly useful for booking systems, event planning, or any scenario where date selection needs boundaries:


```python
dt_picker = pmui.DatePicker(
    label='Date Picker',
    start=dt.date(2024, 4, 1),
    end=dt.date(2024, 4, 7),
    value=dt.date(2024, 4, 1)
)

pmui.Row(dt_picker, height=425)
```

### Disable Past or Future Dates

The `disable_past` and `disable_future` options provide convenient ways to limit date selection relative to today. Perfect for scheduling future appointments or selecting historical dates:


```python
disable_past = pmui.DatePicker(
    disable_past=True,
    label='Date Picker (disable_past)',
)

disable_future = pmui.DatePicker(
    disable_future=True,
    label='Date Picker (disable_future)',
)

pmui.Row(disable_past, disable_future, height=425)
```

### Enabled Dates

Use the `enabled_dates` parameter to restrict selection to specific dates only. This is ideal for availability calendars, appointment booking, or event-specific date selection:


```python
date_picker = pmui.DatePicker(
    label='Date Picker (enabled_dates)',
    enabled_dates=[dt.date(2024, 4, i) for i in range(1, 7)],
    value=dt.date(2024, 4, 1)
)

pmui.Column(date_picker, height=425)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.DatePicker(label='Start Date', helper_text='Select the project start date')
```

### Disabled Dates

The `disabled_dates` parameter allows you to exclude specific dates while keeping all others available. Useful for blocking holidays, maintenance days, or unavailable periods:


```python
date_picker = pmui.DatePicker(
    label='Date Picker (disabled_dates)',
    disabled_dates=[dt.date(2024, 4, i) for i in range(2, 7)],
    value=dt.date(2024, 4, 1)
)

pmui.Column(date_picker, height=425)
```

### Clearable Behavior

Control whether users can clear the selected date using the `clearable` parameter. When enabled, users can reset the value to `None` using the clear button:


```python
pmui.Row(
    pmui.DatePicker(label='Clearable', value="2024-04-01", clearable=True),
    pmui.DatePicker(label='Not Clearable', value="2024-04-01", clearable=False),
    height=425
)
```

### Date Format Display

Customize how dates appear in the input field using the `format` parameter. This affects only the display format, not the underlying value:


```python
pmui.Row(pmui.DatePicker(label='Custom Format', value="2024-04-01", format="MM/DD/YYYY"), height=425)
```

### Calendar Views

The DatePicker supports three navigation views: "day", "month", and "year". By default, all three views are enabled, allowing users to navigate efficiently between different time scales. Customize the available views using the `views` parameter:


```python
pmui.FlexBox(
    pmui.DatePicker(label='"year", "month" and "day"', value="2024-04-01", views=["year", "month", "day"]),
    pmui.DatePicker(label='"day"', value="2024-04-01", views=["day"]),
    pmui.DatePicker(label='"month" and "year"', value="2024-04-01", views=["month", "year"]),
    pn.Spacer(height=425)
)
```

### Initial Calendar View

By default, the calendar opens to the "day" view. Use the `open_to` parameter to change which view appears first when users open the calendar:


```python
pmui.Row(
    pmui.DatePicker(label='"year"', open_to="year"),
    pmui.DatePicker(label='"month"', open_to="month", views=["year", "month", "day"]),
    height=425
)
```

### Color Options

The `color` parameter allows you to visually distinguish the `DatePicker` component when it's active or focused. This helps create a cohesive visual hierarchy in your application. Available color options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":


```python
pmui.FlexBox(
    *[pmui.DatePicker(label=color, value="2024-04-01", color=color) for color in pmui.ColorPicker.param.color.objects], pn.Spacer(height=425)
)
```

### Variant Styles

The `variant` parameter controls the visual appearance of the input field, allowing you to match your application's design aesthetic. Choose from "filled", "outlined" (default), or "standard":


```python
pmui.FlexBox(
    pmui.DatePicker(label='Date Picker', value="2024-04-01", variant="filled"),
    pmui.DatePicker(label='Date Picker', value="2024-04-01", variant="outlined"),
    pmui.DatePicker(label='Date Picker', value="2024-04-01", variant="standard"),
)
```

### Disabled and Loading States

Like other widgets, the `DatePicker` can be disabled to prevent interaction and/or show a loading indicator:


```python
pmui.DatePicker(label='Disabled and Loading', value="2024-04-01", disabled=True, loading=True)
```

### Example


```python
import datetime as dt
import panel as pn
import panel_material_ui as pmui
pn.extension()

date_picker = pmui.DatePicker(label='Date Picker', value=dt.datetime(2024,7,1))

def create_message(selected_date):
    today = dt.date.today()
    days_diff = (selected_date - today).days
    weekday = selected_date.strftime("%A")

    if days_diff == 0:
        time_desc = "🎯 Today"
    elif days_diff == 1:
        time_desc = "⏭️ Tomorrow"
    elif days_diff == -1:
        time_desc = "⏮️ Yesterday"
    elif days_diff > 0:
        time_desc = f"⏳ In {days_diff} days"
    else:
        time_desc = f"⏪ {abs(days_diff)} days ago"

    return f"""
    ### Selected Date: {selected_date.strftime("%B %d, %Y")}

    **Day of the week:** {weekday}  
    **Relative to today:** {time_desc}  
    **ISO format:** {selected_date.isoformat()}
    """

message = pn.bind(create_message, date_picker)

pmui.Column(date_picker, message, height=425)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_date_picker = pmui.DatePicker(
    label=":material/event: Pick a date",
    value=dt.date(2024, 4, 14),
)

icon_date_picker
```

### API Reference

#### Parameters


```python
date_picker.api(jslink=False)
```

### References

**Panel Documentation:**
- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI DatePicker:**
- [Material UI DatePicker Reference](https://mui.com/x/react-date-pickers/date-picker/) - Complete documentation for the underlying Material UI component
- [Material UI DatePicker API](https://mui.com/x/api/date-pickers/date-picker/) - Detailed API reference and configuration options
