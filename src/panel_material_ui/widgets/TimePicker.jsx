import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider"
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs"
import {TimePicker as MUITimePicker} from "@mui/x-date-pickers/TimePicker"
import TextField from "@mui/material/TextField"
import dayjs from "dayjs"

export function render({model, view}) {
  const [label] = model.useState("label")
  const [disabled] = model.useState("disabled")
  const [clock] = model.useState("clock")
  const [seconds] = model.useState("seconds")
  const [minute_increment] = model.useState("minute_increment")
  const [hour_increment] = model.useState("hour_increment")
  const [second_increment] = model.useState("second_increment")
  const [min_time] = model.useState("start")
  const [max_time] = model.useState("end")
  const [color] = model.useState("color")
  const [variant] = model.useState("variant")
  const [format] = model.useState("format")
  const [sx] = model.useState("sx")
  const [modelValue] = model.useState("value")

  // Parse the time value from Python
  function parseTime(timeString) {
    if (!timeString) return null;
    
    // Handle both datetime.time objects and string representations
    if (typeof timeString === 'string') {
      const [hours, minutes, seconds] = timeString.split(':').map(Number);
      // Create a dayjs object for today with the specified time
      return dayjs().hour(hours).minute(minutes).second(seconds || 0);
    } else {
      console.warn("Unexpected time format:", timeString);
      return null;
    }
  }

  // Initialize with the model value and keep it in sync
  const [value, setValue] = React.useState(() => parseTime(modelValue));

  // Update local state when model value changes
  React.useEffect(() => {
    const parsedTime = parseTime(modelValue);
    setValue(parsedTime);
  }, [modelValue]);

  // The ampm setting depends on the clock setting
  const ampm = clock === "12h";

  // Send the time value back to Python when it changes
  const handleChange = (newValue) => {
    setValue(newValue);
    if (newValue) {
      // Format as HH:MM:SS for Python's datetime.time
      const timeString = newValue.format('HH:mm:ss');
      model.value = timeString;
    } else {
      model.value = null;
    }
  };

  // Format the view options based on whether seconds are enabled
  const views = seconds ? ['hours', 'minutes', 'seconds'] : ['hours', 'minutes'];

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <MUITimePicker
        label={label}
        value={value}
        onChange={handleChange}
        disabled={disabled}
        ampm={ampm}
        minutesStep={minute_increment}
        secondsStep={second_increment}
        hoursStep={hour_increment}
        views={views}
        format={format}
        minTime={min_time ? parseTime(min_time) : undefined}
        maxTime={max_time ? parseTime(max_time) : undefined}
        slotProps={{textField: {variant, color}, popper: {container: view.container}}}
        sx={{width: "100%", ...sx}}
      />
    </LocalizationProvider>
  );
}