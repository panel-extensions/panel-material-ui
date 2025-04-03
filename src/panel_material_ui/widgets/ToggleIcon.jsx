import Checkbox from "@mui/material/Checkbox"
import SvgIcon from "@mui/material/SvgIcon"

export function render({model, el}) {
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [size] = model.useState("size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")

  return (
    <Checkbox
      checked={value}
      color={color}
      disabled={disabled}
      selected={value}
      size={size}
      onClick={(e, newValue) => setValue(!value)}
      icon={icon.trim().startsWith("<") ? <SvgIcon>{icon}</SvgIcon> : <Icon>{icon}</Icon>}
      checkedIcon={active_icon.trim().startsWith("<") ? <SvgIcon>{active_icon}</SvgIcon> : <Icon>{active_icon}</Icon>}
      sx={sx}
    />
  )
}
