import ToggleButton from "@mui/material/ToggleButton"
import {render_icon} from "./utils"

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [end_icon] = model.useState("end_icon")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = React.useRef(null)
  }
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  return (
    <ToggleButton
      color={color}
      disabled={disabled}
      fullWidth
      selected={value}
      onChange={() => setValue(!value)}
      ref={ref}
      sx={{...sx}}
      value={value}
      variant={variant}
      {...other}
    >
      {icon && render_icon(icon, null, null, icon_size)}
      {label}
      {end_icon && render_icon(end_icon, null, null, icon_size)}
    </ToggleButton>
  )
}
