import Button from "@mui/material/Button"
import {render_badge, render_icon, render_icon_text, useAria} from "./utils"

const BADGE_SX = {width: "100%", height: "100%"}

const BUTTON_BASE_SX = {
  height: "100%",
  ".MuiButton-startIcon": {mr: "var(--pmui-starticon-mr, 8px)"},
  "&.MuiButton-sizeSmall": {py: "6px"}
}

export function render(props, ref) {
  const {model, ...other} = props
  const [badge] = model.useState("badge")
  const [badge_color] = model.useState("badge_color")
  const [badge_max] = model.useState("badge_max")
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
  const aria = useAria(model)
  const buttonSx = React.useMemo(
    () => (sx ? [BUTTON_BASE_SX, sx] : BUTTON_BASE_SX),
    [sx]
  )

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = React.useRef(null)
  }
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  const button = (
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
      sx={buttonSx}
      style={{"--pmui-starticon-mr": label.length ? "8px" : "0px"}}
      target={target}
      variant={variant}
      {...aria}
      {...other}
    >
      {render_icon_text(label)}
    </Button>
  )
  // The badge sits on the button's top-right corner rather than over its icon.
  return render_badge(button, badge, badge_color, badge_max, "rectangular", BADGE_SX)
}
