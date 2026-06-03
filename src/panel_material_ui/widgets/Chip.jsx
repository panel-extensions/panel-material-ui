import Chip from "@mui/material/Chip"
import {render_icon, render_icon_text} from "./utils"

const SIZES = {
  small: "1.2em",
  medium: "2em",
}

export function render(props, ref) {
  const {model, ...other} = props

  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = React.useRef(null)
  }

  return (
    <Chip
      color={color}
      disabled={disabled}
      fullWidth
      icon={icon ? render_icon(icon, null, size, SIZES[size]) : null}
      label={render_icon_text(label)}
      onClick={(e) => model.send_event("click", e)}
      ref={ref}
      size={size}
      sx={sx}
      variant={variant}
      {...other}
    />
  )
}
