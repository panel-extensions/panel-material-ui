import IconButton from "@mui/material/IconButton"
import {useTheme} from "@mui/material/styles"
import {render_icon} from "./utils"

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
    ref = React.useRef(null)
  }
  model.on("msg:custom", (msg) => {
    ref.current?.focus()
  })

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
      {render_icon(current_icon, null, size, icon_size)}
    </IconButton>
  )
}
