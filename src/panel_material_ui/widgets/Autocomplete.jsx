import TextField from "@mui/material/TextField"
import Autocomplete from "@mui/material/Autocomplete"
import Popper from "@mui/material/Popper"

export function render({model, el}) {
  const [value, setValue] = model.useState("value")
  const [options] = model.useState("options")
  const [label] = model.useState("label")
  const [variant] = model.useState("variant")
  const [disabled] = model.useState("disabled")
  function CustomPopper(props) {
    return <Popper {...props} container={el} />
  }
  return (
    <Autocomplete
      value={value}
      onChange={(event, newValue) => setValue(newValue)}
      options={options}
      disabled={disabled}
      variant={variant}
      PopperComponent={CustomPopper}
      renderInput={(params) => <TextField {...params} variant={variant} label={label} />}
    />
  )
}
