import IconButton from "@mui/material/IconButton"
import InputAdornment from "@mui/material/InputAdornment"
import TextField from "@mui/material/TextField"
import Visibility from "@mui/icons-material/Visibility"
import VisibilityOff from "@mui/icons-material/VisibilityOff"
import {render_description} from "./description"
import {render_icon_text, useDraftInput} from "./utils"

export function render({model, host}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [helper_text] = model.useState("helper_text")
  const [label] = model.useState("label")
  const [max_length] = model.useState("max_length")
  const [placeholder] = model.useState("placeholder")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const {draft, commit, inputProps} = useDraftInput(model)
  const [showPassword, setShowPassword] = React.useState(false)

  const ref = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    return model.on("msg", focus_cb)
  }, [])

  return (
    <TextField
      color={color}
      disabled={disabled}
      error={error_state}
      fullWidth
      helperText={helper_text ? render_icon_text(helper_text) : undefined}
      inputRef={ref}
      label={model.description ? <>{render_icon_text(label)}{render_description({model, host})}</> : render_icon_text(label)}
      {...inputProps}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          model.send_event("enter", event)
          commit()
        }
      }}
      maxLength={max_length}
      size={size}
      slotProps={{
        htmlInput: {maxLength: max_length},
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
      value={draft}
    />
  )
}
