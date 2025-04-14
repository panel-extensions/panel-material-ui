import Button from "@mui/material/Button"

export function render({model, el}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [href] = model.useState("href")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  return (
    <Button
      color={color}
      disabled={disabled}
      fullWidth
      href={href}
      onClick={() => model.send_event("click", {})}
      startIcon={icon && (
        icon.trim().startsWith("<") ?
          <img src={`data:image/svg+xml;base64,${btoa(icon)}`} style={{width: icon_size, height: icon_size, paddingRight: "0.5em"}} /> :
          <Icon style={{fontSize: icon_size}}>{icon}</Icon>
      )}
      sx={sx}
      variant={variant}
    >
      {label}
    </Button>
  )
}
