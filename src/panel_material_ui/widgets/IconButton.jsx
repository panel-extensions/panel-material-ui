import IconButton from "@mui/material/IconButton"
import {useTheme} from "@mui/material/styles"
import {render_icon} from "./utils"

const BASE_ICON_BUTTON_SX = {
  width: "100%",
  color: "var(--pmui-iconbutton-color, inherit)"
}

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
  const timeoutRef = React.useRef(null)
  const iconButtonSx = React.useMemo(
    () => (sx ? [BASE_ICON_BUTTON_SX, sx] : BASE_ICON_BUTTON_SX),
    [sx]
  )

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = React.useRef(null)
  }

  React.useEffect(() => {
    const handler = () => {
      ref.current?.focus()
    }
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [model, ref])

  React.useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  const handleClick = (e) => {
    model.send_event("click", e)
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }
    if (active_icon || active_icon === icon) {
      setIcon(active_icon)
      timeoutRef.current = setTimeout(() => setIcon(icon), toggle_duration)
    } else {
      const paletteEntry = theme.palette[color] || theme.palette.primary
      setColorVariant(paletteEntry.dark)
      timeoutRef.current = setTimeout(() => setColorVariant(null), toggle_duration)
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
      sx={iconButtonSx}
      style={{"--pmui-iconbutton-color": color_variant || "inherit"}}
      target={target}
      {...other}
    >
      {render_icon(current_icon, null, size, icon_size)}
    </IconButton>
  )
}
