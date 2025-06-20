import TextField from "@mui/material/TextField"
import Autocomplete from "@mui/material/Autocomplete"
import Popper from "@mui/material/Popper"

export function render({model, el}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [value_input, setValueInput] = model.useState("value_input")
  const [options] = model.useState("options")
  const [placeholder] = model.useState("placeholder")
  const [restrict] = model.useState("restrict")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  function CustomPopper(props) {
    return <Popper {...props} container={el} />
  }

  const filter_op = (input) => {
    return (opt) => {
      if (!model.case_sensitive) {
        opt = opt.toLowerCase()
        input = input.toLowerCase()
      }
      return model.search_strategy == "includes" ? opt.includes(input) : opt.startsWith(input)
    }
  }

  const filt_func = (options, state) => {
    const input = state.inputValue
    if (input.length < model.min_characters) {
      return []
    }
    return options.filter(filter_op(input))
  }

  return (
    <Autocomplete
      color={color}
      disabled={disabled}
      filterOptions={filt_func}
      freeSolo={!restrict}
      fullWidth
      inputValue={value_input || ""}
      onChange={(event, newValue) => setValue(newValue)}
      options={options}
      renderInput={(params) => (
        <TextField
          {...params}
          color={color}
          label={label}
          placeholder={placeholder}
          onChange={(event) => {
            setValueInput(event.target.value)
          }}
          onKeyDown={(event) => {
            if (restrict && ((value_input || "").length < model.min_characters)) {
              return
            } else if (event.key === "Enter") {
              let new_value = value_input
              if (restrict) {
                const filtered = options.filter(filter_op(new_value))
                if (filtered.length > 0) {
                  new_value = filtered[0]
                  setValueInput(filtered[0])
                } else {
                  return
                }
              }
              event.target.value = new_value
              model.send_event("enter", event)
              setValue(new_value)
            }
          }}
          size={size}
          variant={variant}
        />
      )}
      size={size}
      sx={sx}
      value={value}
      variant={variant}
      PopperComponent={CustomPopper}
    />
  )
}
