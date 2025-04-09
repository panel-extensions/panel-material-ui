import IconButton from "@mui/material/IconButton"
import {useTheme} from "@mui/material/styles"

export function render({model, el}) {
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [edge] = model.useState("edge")
  const [icon] = model.useState("icon")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [toggle_duration] = model.useState("toggle_duration")
  const [current_icon, setIcon] = React.useState(icon)
  const [color_variant, setColorVariant] = React.useState(color)

  const theme = useTheme()

  const handleClick = (e) => {
    model.send_event("click", e)
    if (active_icon || active_icon === icon) {
      setIcon(active_icon)
      setTimeout(() => setIcon(icon), toggle_duration)
    } else {
      setColorVariant(theme.palette[color].dark)
      setTimeout(() => setColorVariant(color), toggle_duration)
    }
  }

  return (
    <IconButton
      color={color_variant}
      disabled={disabled}
      edge={edge}
      size={size}
      sx={sx}
      onClick={handleClick}
    >
      {current_icon.trim().startsWith("<") ?
        <img src={`data:image/svg+xml;base64,${btoa(current_icon)}`} style={{width: size, height: size}} /> :
        <Icon style={{fontSize: size}}>{current_icon}</Icon>
      }
    </IconButton>
  )
}
