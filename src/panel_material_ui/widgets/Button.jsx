import Button from "@mui/material/Button"
import {parseIconName} from "./utils"

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

  const standard_size = ["small", "medium", "large"].includes(size)
  const font_size = standard_size ? icon_size : size
  const icon_font_size = ["small", "medium", "large"].includes(icon_size) ? icon_size : size

  return (
    <Button
      color={color}
      disableElevation={disable_elevation}
      disabled={disabled}
      endIcon={end_icon && (
        end_icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(end_icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: font_size,
            height: font_size,
            display: "inline-block"}}
          /> : (() => {
            const iconData = parseIconName(end_icon)
            return <Icon baseClassName={iconData.baseClassName} fontSize={icon_font_size} sx={icon_size ? {fontSize: icon_size} : {}}>{iconData.iconName}</Icon>
          })()
      )}
      fullWidth
      href={href}
      loading={loading}
      loadingPosition="start"
      onClick={() => model.send_event("click", {})}
      ref={ref}
      startIcon={icon && (
        icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: font_size,
            height: font_size,
            display: "inline-block"}}
          /> : (() => {
            const iconData = parseIconName(icon)
            return <Icon baseClassName={iconData.baseClassName} fontSize={icon_font_size} sx={icon_size ? {fontSize: icon_size} : {}}>{iconData.iconName}</Icon>
          })()
      )}
      size={size}
      sx={{height: "100%", ".MuiButton-startIcon": {mr: label.length ? "8px": 0}, ...sx}}
      target={target}
      variant={variant}
      {...other}
    >
      {label}
    </Button>
  )
}
