import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import ToggleButton from "@mui/material/ToggleButton"
import Tooltip from "@mui/material/Tooltip";

export function render({model}) {
  const [color] = model.useState("color")
  const [variant] = model.useState("button_style")
  const [size] = model.useState("size")
  const [orientation] = model.useState("orientation")
  const [disabled] = model.useState("disabled")
  const [disableElevation] = model.useState("disableElevation")
  const [options] = model.useState("options")
  const [value, setValue] = model.useState("value")
  const exclusive = model.esm_constants.exclusive
  return (
    <ToggleButtonGroup
      disabled={disabled}
      orientation={orientation}
      value={value}
    >
      {options.map((option, index) => {
        return (
          <ToggleButton
            color={color}
            size={size}
            aria-label={option}
            key={option}
            value={option}
	    variant={variant}
            selected={exclusive ? (value==option) : value.includes(option)}
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
          >
            {option}
          </ToggleButton>
        )
      })}
    </ToggleButtonGroup>
  )
}
