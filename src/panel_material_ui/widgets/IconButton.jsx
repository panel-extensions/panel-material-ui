import IconButton from "@mui/material/IconButton";

export function render({model, el}) {
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("button_type")
  const [disabled] = model.useState("disabled")
  const [edge] = model.useState("edge")
  const [icon] = model.useState("icon")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [toggle_duration] = model.useState("toggle_duration")
  const [current_icon, setIcon] = React.useState(icon)

  const handleClick = (e) => {
    model.send_event("click", e)
    if (active_icon) {
      setIcon(active_icon)
      setTimeout(() => setIcon(icon), toggle_duration)
    }
  }

  return (
    <IconButton
      color={color}
      disabled={disabled}
      edge={edge}
      size={size}
      sx={sx}
      onClick={handleClick}
    >
      <Icon style={{fontSize: size}}>{current_icon}</Icon>
    </IconButton>
  )
}
