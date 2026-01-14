import Fab from "@mui/material/Fab"
import {render_icon} from "./utils"

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [end_icon] = model.useState("end_icon")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [href] = model.useState("href")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [target] = model.useState("target")
  const [variant] = model.useState("variant")

  const padding = variant === "extended" ? "1.2em" : "0.2em"

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = React.useRef(null)
  }
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  return (
    <Fab
      aria-label={label}
      color={color}
      disabled={disabled}
      href={href}
      loading={loading}
      onClick={() => model.send_event("click", {})}
      ref={ref}
      size={size}
      sx={sx}
      target={target}
      variant={variant}
      {...other}
    >
      {icon && render_icon(icon, null, null, icon_size, null, {pr: padding})}
      {variant === "extended" && label}
      {end_icon && render_icon(end_icon, null, null, icon_size, null, {pl: padding})}
    </Fab>
  )
}
