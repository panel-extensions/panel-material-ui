import Button from "@mui/material/Button"
import {render_icon} from "./utils"

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [color] = model.useState("color")
  const [disable_elevation] = model.useState("disable_elevation")
  const [disabled] = model.useState("disabled")
  const [end_icon] = model.useState("end_icon")
  const [href] = model.useState("href")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const [target] = model.useState("target")

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = React.useRef(null)
  }
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  return (
    <Button
      color={color}
      disableElevation={disable_elevation}
      disabled={disabled}
      endIcon={end_icon && render_icon(end_icon, null, size, icon_size)}
      fullWidth
      href={href}
      loading={loading}
      loadingPosition="start"
      onClick={() => model.send_event("click", {})}
      ref={ref}
      size={size}
      startIcon={icon && render_icon(icon, null, size, icon_size)}
      sx={{height: "100%", ".MuiButton-startIcon": {mr: label.length ? "8px": 0}, ...sx}}
      target={target}
      variant={variant}
      {...other}
    >
      {label}
    </Button>
  )
}
