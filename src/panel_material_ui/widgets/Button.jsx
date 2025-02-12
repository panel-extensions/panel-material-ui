import Button from "@mui/material/Button"

export function render({model, el}) {
  const [color] = model.useState("button_type")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [variant] = model.useState("button_style")

  return (
    <Button
      color={color}
      disabled={disabled}
      variant={variant}
      startIcon={icon && <Icon style={{fontSize: icon_size}}>{icon}</Icon>}
      onClick={() => model.send_event("click", {})}
    >
      {label}
    </Button>
  )
}
