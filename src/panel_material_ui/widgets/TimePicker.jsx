import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider";
import {AdapterDayjs} from "@mui/x-date-pickers/AdapterDayjs";
import {TimePicker as MUITimePicker} from "@mui/x-date-pickers/TimePicker";
import TextField from "@mui/material/TextField";

export function render({model}) {
  const [value, setValue] = React.useState(model.value ? new Date(model.value) : null);
  const [label] = model.useState("label");
  const [disabled] = model.useState("disabled");
  //const [time_format] = model.useState("time_format");
  const [clock] = model.useState("clock");
  const [minutes_increment] = model.useState("minute_increment");
  const [min_time] = model.useState("start");
  const [max_time] = model.useState("end");
  const [color] = model.useState("color");
  const [variant] = model.useState("variant");

  const handleChange = (newValue) => {
    setValue(newValue);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <MUITimePicker
        label={label}
        value={value}
        onChange={handleChange}
        disabled={disabled}
        ampm={clock === "12h"}
        minutesStep={minutes_increment}
        minTime={min_time ? new Date(min_time) : undefined}
        maxTime={max_time ? new Date(max_time) : undefined}
        slotProps={{textField: {variant, color}}}
        sx={{width: "100%"}}
      />
    </LocalizationProvider>
  );
}
