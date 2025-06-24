import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import ToggleButton from "@mui/material/ToggleButton"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [label] = model.useState("label")
  const [options] = model.useState("options")
  const [orientation] = model.useState("orientation")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const exclusive = model.esm_constants.exclusive

  return (
    <FormControl component="fieldset" disabled={disabled} fullWidth>
      {label && <FormLabel id="toggle-buttons-group-label">{label}</FormLabel>}
      <ToggleButtonGroup
        aria-labelledby="toggle-buttons-group-label"
        aria-label={label}
        color={color}
        disabled={disabled}
        fullWidth
        orientation={orientation}
        value={value}
        sx={sx}
      >
        {options.map((option, index) => {
          return (
            <ToggleButton
              aria-label={option}
              key={option}
              onClick={(e) => {
                let newValue
                if (exclusive) {
                  newValue = option
                } else if (value.includes(option)) {
                  newValue = value.filter((v) => v !== option)
                } else {
                  newValue = [...value]
                  newValue.push(option)
                }
                setValue(newValue)
              }}
              selected={exclusive ? (value==option) : value.includes(option)}
              size={size}
              value={option}
            >
              {option}
            </ToggleButton>
          )
        })}
      </ToggleButtonGroup>
    </FormControl>
  )
}
