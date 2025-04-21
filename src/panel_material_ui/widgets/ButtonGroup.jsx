import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import ToggleButton from "@mui/material/ToggleButton"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [options] = model.useState("options")
  const [orientation] = model.useState("orientation")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")
  const exclusive = model.esm_constants.exclusive

  return (
    <ToggleButtonGroup
      color={color}
      disabled={disabled}
      fullWidth
      orientation={orientation}
      value={value}
      variant={variant}
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
  )
}
