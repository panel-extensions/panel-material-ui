import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider"
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs"
import {TimePicker} from "@mui/x-date-pickers/TimePicker"
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
  const [modelValue, setModelValue] = model.useState("value")

  function parseTime(timeString) {
    if (!timeString) { return null; }

    if (typeof timeString === "string") {
      dayjs(timeString, format)
      const [hours, minutes, seconds] = timeString.split(":").map(Number);
      return dayjs().hour(hours).minute(minutes).second(seconds || 0);
    } else {
      console.warn("Unexpected time format:", timeString);
      return null;
    }
  }

  const [value, setValue] = React.useState(parseTime(modelValue))
  React.useEffect(() => {
    const parsedTime = parseTime(modelValue)
    setValue(parsedTime)
  }, [modelValue])

  const handleChange = (newValue) => {
    if (newValue) {
      const timeString = newValue.format("HH:mm:ss")
      setModelValue(timeString)
    } else {
      setModelValue(null)
    }
  };

  const views = seconds ? ["hours", "minutes", "seconds"] : ["hours", "minutes"];

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <TimePicker
        label={label}
        value={value}
        onChange={handleChange}
        disabled={disabled}
        ampm={clock === "12h"}
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
