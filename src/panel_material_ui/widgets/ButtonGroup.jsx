import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import ToggleButton from "@mui/material/ToggleButton"
import Tooltip from "@mui/material/Tooltip";

export function render({model}) {
  const [color] = model.useState("button_type")
  const [variant] = model.useState("button_style")
  const [size] = model.useState("size")
  const [orientation] = model.useState("orientation")
  const [disabled] = model.useState("disabled")
  const [options] = model.useState("options")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")
  const exclusive = model.esm_constants.exclusive
  return (
    <ToggleButtonGroup
      color={color}
      disabled={disabled}
      orientation={orientation}
      value={value}
      variant={variant}
      sx={sx}
    >
      {options.map((option, index) => {
        return (
          <ToggleButton
            size={size}
            aria-label={option}
            key={option}
            value={option}
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
