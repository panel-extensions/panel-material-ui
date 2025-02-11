import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import {DateTimePicker as MUIDateTimePicker} from "@mui/x-date-pickers/DateTimePicker";
import TextField from "@mui/material/TextField";
import dayjs from "dayjs";

export function render({model}) {
  const [value, setValue] = React.useState(model.value ? dayjs(model.value) : null);
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
  const [military_time] = model.useState("military_time");

  const handleChange = (newValue) => {
    setValue(newValue);
    model.send_event("onChange", {value: newValue});
  };

  const [disabled_dates] = model.useState("disabled_dates");
  const [enabled_dates] = model.useState("enabled_dates");

  // Helper to convert a value to a Date.
  function parseDate(d) {
    return new Date(d);
  }

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

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <MUIDateTimePicker
        label={label}
        value={value}
        onChange={handleChange}
        views={views}
        disabled={disabled}
        format={format}
        minDate={min_date ? new Date(min_date) : undefined}
        maxDate={max_date ? new Date(max_date) : undefined}
        disableFuture={disable_future}
        disablePast={disable_past}
        shouldDisableDate={shouldDisableDate}
        openTo={open_to}
        showTodayButton={show_today_button}
        clearable={clearable}
        ampm={!military_time}
        sx={{width: "100%"}}
        slotProps={{textField: {variant, color}}}
      />
    </LocalizationProvider>
  );
}
