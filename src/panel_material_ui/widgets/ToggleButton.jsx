import ToggleButton from "@mui/material/ToggleButton"

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
    ref = undefined
  }

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
      {icon && (
        icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: icon_size,
            height: icon_size,
            display: "inline-block"}}
          /> :
          <Icon style={{fontSize: icon_size}}>{icon}</Icon>
      )}
      {label}
      {end_icon && (
        end_icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(end_icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: icon_size,
            height: icon_size,
            display: "inline-block"}}
          /> :
          <Icon style={{fontSize: icon_size}}>{end_icon}</Icon>
      )}
    </ToggleButton>
  )
}
