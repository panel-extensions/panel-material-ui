import Box from "@mui/material/Box"
import Checkbox from "@mui/material/Checkbox"
import Typography from "@mui/material/Typography"
import {render_icon} from "./utils"

const SIZES = {
  small: "1.5em",
  medium: "2.5em",
  large: "3.5em",
}

const PADDING = {
  small: "5px",
  medium: "8px",
  large: "12px"
}

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [size] = model.useState("size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")

  const standard_size = ["small", "medium", "large"].includes(size)
  const font_size = standard_size ? icon_size : size
  const color_state = disabled ? "disabled" : color
  const text_size = standard_size ? SIZES[size] : font_size

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = React.useRef(null)
  }

  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  return (
    <Box sx={{display: "flex", alignItems: "center", flexDirection: "row"}}>
      <Checkbox
        checked={value}
        checkedIcon={render_icon(active_icon || icon, color_state, size, icon_size)}
        color={color_state}
        disabled={disabled}
        icon={render_icon(icon, color_state, size, icon_size, "-outlined")}
        ref={ref}
        selected={value}
        size={size}
        onClick={(e, newValue) => setValue(!value)}
        sx={{p: PADDING[size], ...sx}}
        {...other}
      />
      {label && <Typography sx={{color: "text.primary", fontSize: `calc(${text_size} / 2)`}}>{label}</Typography>}
    </Box>
  )
}
