import ToggleButton from "@mui/material/ToggleButton"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")

  return (
    <ToggleButton
      color={color}
      disabled={disabled}
      fullWidth
      selected={value}
      onChange={() => setValue(!value)}
      sx={{...sx}}
      value={value}
      variant={variant}
    >
      {icon && (
        icon.trim().startsWith("<") ?
          <img src={`data:image/svg+xml;base64,${btoa(icon)}`} style={{width: icon_size, height: icon_size, paddingRight: "0.5em"}} /> :
          <Icon style={{fontSize: icon_size}}>{icon}</Icon>
      )}
      {label}
    </ToggleButton>
  )
}
