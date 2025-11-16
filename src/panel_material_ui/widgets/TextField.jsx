import TextField from "@mui/material/TextField"
import {render_description} from "./description"

export function render({model, el, view}) {
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

  return (
    <TextField
      color={color}
      disabled={disabled}
      error={error_state}
      fullWidth
      inputProps={{maxLength: max_length}}
      label={model.description ? <>{label}{render_description({model, el, view})}</> : label}
      multiline={model.esm_constants.multiline}
      placeholder={placeholder}
      onBlur={() => setValue(value_input)}
      onChange={(event) => setValueInput(event.target.value)}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          model.send_event("enter", event)
          setValue(value_input)
        }
      }}
      rows={4}
      size={size}
      sx={sx}
      variant={variant}
      value={value_input}
    />
  )
}
