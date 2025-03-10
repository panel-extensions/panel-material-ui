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
  const range = model.esm_constants.range;
  const time = model.esm_constants.time;

  const timeProps = {};
  if (time) {
    const [military_time] = model.useState("military_time");
    timeProps.ampm = !military_time;
  }

  function parseDate(d) {
    if (d === null || d === undefined) {
      return null;
    }

    // Handle array values (for range pickers)
    if (Array.isArray(d)) {
      return d.map(timestamp => dayjs(timestamp));
    }

    // Handle numeric timestamp (milliseconds since epoch)
    if (typeof d === "number") {
      // Create a dayjs date from the timestamp
      // For non-time components, use UTC parsing to avoid timezone issues
      if (!time) {
        // Create date from milliseconds, then extract only the date part
        const date = new Date(d);
        const year = date.getUTCFullYear();
        const month = date.getUTCMonth();
        const day = date.getUTCDate();

        // Set to noon to avoid timezone issues
        return dayjs().year(year).month(month).date(day).hour(12);
      } else {
        // For time components, use local timezone as expected
        return dayjs(d);
      }
    }

    // Handle string values
    if (typeof d === "string") {
      return dayjs(d);
    }

    return dayjs(d);
  }

  // Get the model value once on initialization
  const [modelValue] = model.useState("value");

  // Initialize with the model value
  const [value, setValue] = React.useState(() => parseDate(modelValue));

  // For tracking internal state changes vs. actual submission
  const [internalValue, setInternalValue] = React.useState(() => parseDate(modelValue));

  // Track whether the calendar is open
  const [isCalendarOpen, setIsCalendarOpen] = React.useState(false);

  // Track the last committed value timestamp to prevent duplicate updates
  const lastCommittedRef = React.useRef(null);

  // Update local state when model value changes from Python
  React.useEffect(() => {
    const parsedDate = parseDate(modelValue);
    setValue(parsedDate);
    setInternalValue(parsedDate);
  }, [modelValue]);

  // Format the date value for Python
  function formatDateForPython(date) {
    if (!date || !date.isValid()) {
      return null;
    }

    if (time) {
      // For DateTimePicker, format with time
      return date.format("YYYY-MM-DD HH:mm:ss");
    } else {
      // For DatePicker, manually construct the date string to avoid timezone issues
      const year = date.year();
      const month = date.month() + 1; // dayjs months are 0-indexed
      const day = date.date();

      // Format with leading zeros
      return `${year}-${month.toString().padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
    }
  }

  // Safely update the model value
  function updateModelValue(date) {
    // Only update if we have a valid date
    if (!date || !date.isValid()) { return; }

    const formattedDate = formatDateForPython(date);
    // Skip update if this is the same value we just committed
    const currentTimestamp = date.valueOf();
    if (lastCommittedRef.current === currentTimestamp) {
      return;
    }

    // Update our tracking reference
    lastCommittedRef.current = currentTimestamp;

    // Update the model
    setValue(date);
    model.value = formattedDate;
  }

  // Handle calendar open
  const handleOpen = () => {
    setIsCalendarOpen(true);
  };

  // Handle changes from the date picker UI
  const handleChange = (newValue) => {
    setInternalValue(newValue);

    // For direct calendar selection, update immediately
    if (isCalendarOpen && newValue && newValue.isValid()) {
      updateModelValue(newValue);
    }
  };

  // Handle explicit accept (enter key or click on today button)
  const handleAccept = (newValue) => {
    updateModelValue(newValue);
  };

  // Handle blur to catch manual edits
  const handleBlur = () => {
    if (!isCalendarOpen) {  // Don't update on blur if calendar is open
      updateModelValue(internalValue);
    }
  };

  // Handle calendar close
  const handleClose = () => {
    setIsCalendarOpen(false);

    // Don't update the model again on close - the change handler already did it
    // This prevents the issue where the value changes again on close
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

  const getDateOnly = (date) => dayjs(date).format("YYYY-MM-DD");

  // Check whether the given date (JS Date) is in a list of dates or ranges.
  function inList(date, list) {
    if (!list || list.length === 0) { return false; }
    for (const item of list) {
      if (Array.isArray(item) || (item && typeof item === "object" && ("from" in item || "to" in item))) {
        if (dateInRange(date, item)) {
          return true;
        }
      } else {
        // Compare single date values for a day-level match.
        if (getDateOnly(item) === getDateOnly(date)) {
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

  // Handle keyboard events (like Enter)
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && internalValue && internalValue.isValid()) {
      updateModelValue(internalValue);
      e.preventDefault();
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Component
        label={label}
        value={internalValue}
        onChange={handleChange}
        onAccept={handleAccept}
        onClose={handleClose}
        onOpen={handleOpen}
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
            onBlur: handleBlur,
            onKeyDown: handleKeyDown,
            InputProps: {
              onBlur: handleBlur
            }
          },
          popper: {container: view.container}
        }}
        {...timeProps}
      />
    </LocalizationProvider>
  );
}
