import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider"
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs"
import {TimePicker} from "@mui/x-date-pickers/TimePicker"
import dayjs from "dayjs"

export function render({model, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [clock] = model.useState("clock")
  const [format] = model.useState("format")
  const [label] = model.useState("label")
  const [max_time] = model.useState("end")
  const [min_time] = model.useState("start")
  const [mode] = model.useState("mode")
  const [seconds] = model.useState("seconds")
  const [sx] = model.useState("sx")
  const [modelValue, setModelValue] = model.useState("value")
  const [variant] = model.useState("variant")

  function parseTime(timeString) {
    if (!timeString) { return null; }

    if (typeof timeString === "string") {
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
  const media_query = mode === "auto" ? "@media (pointer:fine)" : (mode === "digital" ? "@media all" : "@media (width: 0px)");

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <TimePicker
        ampm={clock === "12h"}
        desktopModeMediaQuery={media_query}
        disabled={disabled}
        format={format}
        label={label}
        onChange={handleChange}
        minTime={min_time ? parseTime(min_time) : undefined}
        maxTime={max_time ? parseTime(max_time) : undefined}
        slotProps={{textField: {variant, color}, popper: {container: view.container}}}
        sx={{width: "100%", ...sx}}
        value={value}
        views={views}
      />
    </LocalizationProvider>
  );
}
