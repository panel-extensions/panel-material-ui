import TextField from "@mui/material/TextField"
import InputAdornment from "@mui/material/InputAdornment"
import IconButton from "@mui/material/IconButton"
import AddIcon from "@mui/icons-material/Add"
import RemoveIcon from "@mui/icons-material/Remove"
import {int_regex, float_regex} from "./utils"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [format] = model.useState("format")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [step] = model.useState("step")
  const [min] = model.useState("start")
  const [max] = model.useState("end")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")

  const [oldValue, setOldValue] = React.useState(value)
  const [focused, setFocused] = React.useState(false)

  const validate = (value) => {
    const regex = model.mode == "int" ? int_regex : float_regex
    if (value === "") {
      return null
    } else if (regex.test(value)) {
      return Number(value)
    } else {
      return oldValue
    }
  }

  const handleChange = (event) => {
    const newValue = validate(event.target.value)
    setOldValue(value)
    setValue(newValue)
  }

  const [valueLabel, setValueLabel] = React.useState()

  React.useEffect(() => {
    setValueLabel(format && !focused ? format.doFormat([value], {loc: 0})[0] : value)
  }, [format, value, focused])

  const increment = (multiplier = 1) => {
    setOldValue(value)
    if (value === null) {
      setValue(min != null ? min : 0)
    } else {
      const incremented = Math.round((value + (step * multiplier)) * 100000000000) / 100000000000
      setValue(max != null ? Math.min(max, incremented) : incremented)
    }
  }
  const decrement = (multiplier = 1) => {
    setOldValue(value)
    if (value === null) {
      setValue(max != null ? max : 0)
    } else {
      const decremented = Math.round((value - (step * multiplier)) * 100000000000) / 100000000000
      setValue(min != null ? Math.max(min, decremented) : decremented)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "ArrowUp") {
      e.preventDefault();
      increment();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      decrement();
    } else if (e.key === "PageUp") {
      e.preventDefault();
      increment(model.page_step_multiplier);
    } else if (e.key === "PageDown") {
      e.preventDefault();
      decrement(model.page_step_multiplier);
    }
  }
  return (
    <TextField
      color={color}
      disabled={disabled}
      fullWidth
      label={label}
      onBlur={() => setFocused(false)}
      onChange={handleChange}
      onFocus={() => setFocused(true)}
      onKeyDown={handleKeyDown}
      placeholder={placeholder}
      size={size}
      sx={sx}
      value={valueLabel}
      variant={variant}
      InputProps={{
        inputMode: "decimal",
        sx: {padding: 0},
        startAdornment: (
          <InputAdornment position="start">
            <IconButton onClick={() => decrement()} size="small" color="default">
              <RemoveIcon fontSize="small" />
            </IconButton>
          </InputAdornment>
        ),
        endAdornment: (
          <InputAdornment position="end">
            <IconButton onClick={() => increment()} size="small" color="default">
              <AddIcon fontSize="small" />
            </IconButton>
          </InputAdornment>
        ),
      }}
    />
  );
}
