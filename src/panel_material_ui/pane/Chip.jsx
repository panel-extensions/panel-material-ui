import Chip from "@mui/material/Chip"
import {render_icon} from "./utils"

const SIZES = {
  small: "1.2em",
  medium: "2em",
}

export function render({model}) {
  const [color] = model.useState("color")
  const [icon] = model.useState("icon")
  const [label] = model.useState("object")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  return (
    <Chip
      color={color}
      icon={icon ? render_icon(icon, null, size, SIZES[size]) : null}
      label={label}
      size={size}
      sx={sx}
      variant={variant}
      onClick={(e) => model.send_event("click", e)}
    />
  )
}
