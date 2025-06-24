import IconButton from "@mui/material/IconButton"
import InputAdornment from "@mui/material/InputAdornment"
import TextField from "@mui/material/TextField"
import Visibility from "@mui/icons-material/Visibility"
import VisibilityOff from "@mui/icons-material/VisibilityOff"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [label] = model.useState("label")
  const [max_length] = model.useState("max_length")
  const [placeholder] = model.useState("placeholder")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [value_input, setValueInput] = model.useState("value_input")
  const [variant] = model.useState("variant")
  const [showPassword, setShowPassword] = React.useState(false)

  return (
    <TextField
      color={color}
      disabled={disabled}
      error={error_state}
      fullWidth
      inputProps={{maxLength: max_length}}
      label={label}
      onBlur={() => setValue(value_input)}
      onChange={(event) => setValueInput(event.target.value)}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          model.send_event("enter", event)
          setValue(value_input)
        }
      }}
      maxLength={max_length}
      size={size}
      slotProps={{
        input: {
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                aria-label={
                  showPassword ? "hide the password" : "display the password"
                }
                onClick={() => setShowPassword((show) => !show)}
                onMouseDown={(event) => event.preventDefault()}
                onMouseUp={(event) => event.preventDefault()}
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          )
        }
      }}
      sx={sx}
      type={showPassword ? "text" : "password"}
      variant={variant}
      value={value_input}
    />
  )
}
