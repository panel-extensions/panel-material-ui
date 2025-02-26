import TextField from "@mui/material/TextField"

export function render({model}) {
  const [autogrow] = model.useState("auto_grow")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [max_rows] = model.useState("max_rows")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [rows] = model.useState("rows")
  const [value_input, setValueInput] = model.useState("value_input")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  let props = {}
  if (autogrow) {
    props = {minRows: rows}
  } else {
    props = {rows}
  }

  return (
    <TextField
      fullWidth
      multiline
      color={color}
      disabled={disabled}
      error={error_state}
      label={label}
      maxRows={max_rows}
      onBlur={() => setValue(value_input)}
      onChange={(event) => setValueInput(event.target.value)}
      placeholder={placeholder}
      sx={sx}
      value={value_input}
      variant={variant}
      {...props}
    />
  )
}
