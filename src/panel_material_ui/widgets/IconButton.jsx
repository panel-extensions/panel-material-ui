import IconButton from "@mui/material/IconButton"
import {useTheme} from "@mui/material/styles"

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [edge] = model.useState("edge")
  const [href] = model.useState("href")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [target] = model.useState("target")
  const [toggle_duration] = model.useState("toggle_duration")

  const theme = useTheme()
  const [current_icon, setIcon] = React.useState(icon)
  const [color_variant, setColorVariant] = React.useState(null)

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = undefined
  }

  const handleClick = (e) => {
    model.send_event("click", e)
    if (active_icon || active_icon === icon) {
      setIcon(active_icon)
      setTimeout(() => setIcon(icon), toggle_duration)
    } else {
      setColorVariant(theme.palette[color].dark)
      setTimeout(() => setColorVariant(null), toggle_duration)
    }
  }

  const standard_size = ["small", "medium", "large"].includes(size)
  const font_size = standard_size ? icon_size : size
  const icon_font_size = ["small", "medium", "large"].includes(icon_size) ? icon_size : size

  return (
    <IconButton
      color={color}
      disabled={disabled}
      edge={edge}
      href={href}
      onClick={handleClick}
      ref={ref}
      size={size}
      sx={{color: color_variant, width: "100%", ...sx}}
      target={target}
      {...other}
    >
      {current_icon.trim().startsWith("<") ?
        <span style={{
          maskImage: `url("data:image/svg+xml;base64,${btoa(current_icon)}")`,
          backgroundColor: "currentColor",
          maskRepeat: "no-repeat",
          maskSize: "contain",
          width: font_size,
          height: font_size,
          display: "inline-block"}}
        /> :
        <Icon fontSize={icon_font_size} sx={icon_size ? {fontSize: icon_size} : {}}>{current_icon}</Icon>
      }
    </IconButton>
  )
}
