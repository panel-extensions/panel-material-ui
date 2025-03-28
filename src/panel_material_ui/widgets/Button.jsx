import Button from "@mui/material/Button"
import SvgIcon from "@mui/material/SvgIcon"

export function render({model, el}) {
  const [color] = model.useState("button_type")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [variant] = model.useState("button_style")
  const [sx] = model.useState("sx")

  return (
    <Button
      color={color}
      disabled={disabled}
      onClick={() => model.send_event("click", {})}
      startIcon={icon && icon.startsWith("<") ? <SvgIcon>{icon}</SvgIcon> : <Icon style={{fontSize: icon_size}}>{icon}</Icon>}
      sx={sx}
      variant={variant}
    >
      {label}
    </Button>
  )
}
