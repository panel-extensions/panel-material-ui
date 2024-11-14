import TextField from "@mui/material/TextField"

export function render({model}) {
  const [autogrow] = model.useState("auto_grow")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [max_rows] = model.useState("max_rows")
  const [label] = model.useState("label")
  const [rows] = model.useState("rows")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  let props = {}
  if (autogrow) {
    props = {minRows: rows}
  } else {
    props = {rows}
  }

  return (
    <TextField
      multiline
      color={color}
      error={error_state}
      label={label}
      variant={variant}
      value={value}
      disabled={disabled}
      onChange={(event) => setValue(event.target.value)}
      maxRows={max_rows}
      fullWidth
      {...props}
    />
  )
}
