import ToggleButton from "@mui/material/ToggleButton"

export function render({model}) {
  const [button_style] = model.useState("button_style")
  const [color] = model.useState("button_type")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")

  return (
    <ToggleButton
      color={color}
      disabled={disabled}
      selected={value}
      onChange={(e, newValue) => setValue(!value)}
      sx={sx}
      variant={button_style}
    >
      {icon && <Icon style={{fontSize: icon_size}}>{icon}</Icon>}
      {label}
    </ToggleButton>
  )
}
