import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import {DatePicker as MUIDatePicker} from "@mui/x-date-pickers/DatePicker";
import {DateTimePicker as MUIDateTimePicker} from "@mui/x-date-pickers/DateTimePicker";
import TextField from "@mui/material/TextField";
import dayjs from "dayjs";

export function render({model, view}) {
  const [label] = model.useState("label");
  const [color] = model.useState("color");
  const [variant] = model.useState("variant");
  const [disabled] = model.useState("disabled");
  const [views] = model.useState("views");
  const [min_date] = model.useState("start");
  const [max_date] = model.useState("end");
  const [disable_future] = model.useState("disable_future");
  const [disable_past] = model.useState("disable_past");
  const [open_to] = model.useState("open_to");
  const [show_today_button] = model.useState("show_today_button");
  const [clearable] = model.useState("clearable");
  const [format] = model.useState("format");
  const [sx] = model.useState("sx");
  const [modelValue] = model.useState("value");
  const range = model.esm_constants.range;
  const time = model.esm_constants.time;

  const timeProps = {};
  if (time) {
    const [military_time] = model.useState("military_time");
    timeProps.ampm = !military_time;
  }

  // Parse date from various formats
  function parseDate(d) {
    if (d === null || d === undefined) {
      return null;
    }

    // Handle array values (for range pickers)
    if (Array.isArray(d)) {
      return d.map(item => parseDate(item)).filter(Boolean);
    }

    // Handle timestamp or unix timestamp
    if (typeof d === 'number') {
      return dayjs.unix(d / 1000);
    }

    // Handle ISO string format
    if (typeof d === 'string') {
      const parsedDate = dayjs(d);
      return parsedDate;
    }

    // Default parsing for other formats
    return dayjs(d);
  }

  // Initialize state with model value
  const [value, setValue] = React.useState(() => parseDate(modelValue));

  // For tracking internal state changes vs. actual submission
  const [internalValue, setInternalValue] = React.useState(() => parseDate(modelValue));

  // Keep in sync with model changes
  React.useEffect(() => {
    const parsedDate = parseDate(modelValue);
    setValue(parsedDate);
    setInternalValue(parsedDate);
  }, [modelValue]);

  // Handle internal changes (typing, selecting from picker)
  const handleChange = (newValue) => {
    setInternalValue(newValue);
  };

  // Only update the model when input is complete (blur or selection confirmed)
  const handleAccept = (newValue) => {
    setValue(newValue);
    if (newValue) {
      // Update the model directly
      const formattedValue = newValue.format('YYYY-MM-DD HH:mm:ss');
      model.value = formattedValue;
    } else {
      model.value = null;
    }
  };

  // Also update on blur to catch manual edits
  const handleBlur = () => {
    if (internalValue) {
      setValue(internalValue);
      const formattedValue = internalValue.format('YYYY-MM-DD HH:mm:ss');
      model.value = formattedValue;
    }
  };

  const [disabled_dates] = model.useState("disabled_dates");
  const [enabled_dates] = model.useState("enabled_dates");

  // Check whether a given date falls within a specified range.
  function dateInRange(date, range) {
    let from, to;
    if (Array.isArray(range)) {
      from = parseDate(range[0]);
      to = parseDate(range[1]);
    } else if (range && typeof range === "object" && range.from && range.to) {
      from = parseDate(range.from);
      to = parseDate(range.to);
    } else {
      return false;
    }
    return date >= from && date <= to;
  }

  // Check whether the given date (JS Date) is in a list of dates or ranges.
  function inList(date, list) {
    if (!list || list.length === 0) { return false; }
    for (const item of list) {
      if (Array.isArray(item) || (item && typeof item === "object" && ("from" in item || "to" in item))) {
        if (dateInRange(date, item)) {
          return true;
        }
      } else {
        // Compare single date values (by toDateString for a day-level match).
        if (parseDate(item).toDateString() === date.toDateString()) {
          return true;
        }
      }
    }
    return false;
  }

  function shouldDisableDate(date) {
    if (enabled_dates && enabled_dates.length > 0) {
      // If enabled_dates is specified, disable if the date is NOT in the enabled list.
      return !inList(date, enabled_dates);
    }
    if (disabled_dates && disabled_dates.length > 0) {
      // Otherwise, if disabled_dates is specified, disable if the date is in that list.
      return inList(date, disabled_dates);
    }
    return false;
  }

  // Use the appropriate component based on whether we need date+time or just date
  const Component = time ? MUIDateTimePicker : MUIDatePicker;

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Component
        label={label}
        value={internalValue}
        onChange={handleChange}
        onAccept={handleAccept}
        onClose={handleBlur}
        views={views}
        disabled={disabled}
        format={format}
        minDate={min_date ? parseDate(min_date) : undefined}
        maxDate={max_date ? parseDate(max_date) : undefined}
        disableFuture={disable_future}
        disablePast={disable_past}
        shouldDisableDate={shouldDisableDate}
        openTo={open_to}
        showTodayButton={show_today_button}
        clearable={clearable}
        sx={{width: "100%", ...sx}}
        slotProps={{
          textField: {
            variant,
            color,
            onBlur: handleBlur
          },
          popper: {container: view.container}
        }}
        {...timeProps}
      />
    </LocalizationProvider>
  );
}
