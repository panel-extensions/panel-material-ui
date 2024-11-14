import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import ToggleButton from "@mui/material/ToggleButton"

export function render({model}) {
  const [variant] = model.useState("variant")
  const [color] = model.useState("color")
  const [size] = model.useState("size")
  const [orientation] = model.useState("orientation")
  const [disabled] = model.useState("disabled")
  const [disableElevation] = model.useState("disableElevation")
  const [options] = model.useState("options")
  const [value, setValue] = model.useState("value")
  const exclusive = model.esm_constants.exclusive
  return (
    <ToggleButtonGroup
      color={color}
      disabled={disabled}
      orientation={orientation}
      size={size}
      value={value}
      variant={variant}
    >
      {options.map((option, index) => {
        return (
          <ToggleButton
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
