import TextField from "@mui/material/TextField"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")
  return (
    <TextField
      multiline={model.esm_constants.multiline}
      color={color}
      error={error_state}
      label={label}
      placeholder={placeholder}
      variant={variant}
      value={value}
      disabled={disabled}
      onChange={(event) => setValue(event.target.value)}
      rows={4}
      fullWidth
    />
  )
}
