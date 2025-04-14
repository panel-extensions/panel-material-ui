import IconButton from "@mui/material/IconButton"
import InputAdornment from "@mui/material/InputAdornment"
import TextField from "@mui/material/TextField"
import Visibility from "@mui/icons-material/Visibility"
import VisibilityOff from "@mui/icons-material/VisibilityOff"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [label] = model.useState("label")
  const [max_length] = model.useState("max_length")
  const [placeholder] = model.useState("placeholder")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const [showPassword, setShowPassword] = React.useState(false)

  return (
    <TextField
      color={color}
      disabled={disabled}
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
      fullWidth
      inputProps={{maxLength: max_length}}
      label={label}
      onChange={(event) => setValue(event.target.value)}
      placeholder={placeholder}
      sx={sx}
      type={showPassword ? "text" : "password"}
      variant={variant}
      value={value}
    />
  )
}
