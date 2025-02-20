import TextField from "@mui/material/TextField"
import Autocomplete from "@mui/material/Autocomplete"
import Popper from "@mui/material/Popper"

export function render({model, el}) {
  const [value, setValue] = model.useState("value")
  const [value_input, setValueInput] = model.useState("value_input")
  const [options] = model.useState("options")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [restrict] = model.useState("restrict")
  const [variant] = model.useState("variant")
  const [disabled] = model.useState("disabled")
  const [sx] = model.useState("sx")
  function CustomPopper(props) {
    return <Popper {...props} container={el} />
  }

  const filt_func = (options, state) => {
    let input = state.inputValue
    if (input.length < model.min_characters) {
      return []
    }
    return options.filter((opt) => {
      if (!model.case_sensitive) {
        opt = opt.toLowerCase()
        input = input.toLowerCase()
      }
      return model.search_strategy == "includes" ? opt.includes(input) : opt.startsWith(input)
    })
  }

  return (
    <Autocomplete
      value={value}
      onChange={(event, newValue) => setValue(newValue)}
      options={options}
      disabled={disabled}
      freeSolo={!restrict}
      filterOptions={filt_func}
      variant={variant}
      sx={sx}
      PopperComponent={CustomPopper}
      renderInput={(params) => (
        <TextField
          {...params}
          variant={variant}
          label={label}
          placeholder={placeholder}
          onChange={(event) => setValueInput(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              model.send_event("enter", event)
              setValue(value_input)
            }
          }}
        />
      )}
    />
  )
}
