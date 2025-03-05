import TextField from "@mui/material/TextField"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [label] = model.useState("label")
  const [max_length] = model.useState("max_length")
  const [placeholder] = model.useState("placeholder")
  const [value_input, setValueInput] = model.useState("value_input")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  return (
    <TextField
      color={color}
      disabled={disabled}
      error={error_state}
      inputProps={{maxLength: max_length}}
      label={label}
      multiline={model.esm_constants.multiline}
      placeholder={placeholder}
      variant={variant}
      value={value_input}
      onBlur={() => setValue(value_input)}
      onChange={(event) => setValueInput(event.target.value)}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          model.send_event("enter", event)
          setValue(value_input)
        }
      }}
      rows={4}
      fullWidth
      sx={sx}
    />
  )
}
