import Checkbox from "@mui/material/Checkbox"

export function render({model, el}) {
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [size] = model.useState("size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")

  return (
    <Checkbox
      checked={value}
      color={color}
      disabled={disabled}
      selected={value}
      size={size}
      onClick={(e, newValue) => setValue(!value)}
      icon={
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
          <Icon color={color}>{icon}</Icon>
      }
      checkedIcon={
        active_icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(active_icon || icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: icon_size,
            height: icon_size,
            display: "inline-block"}}
          /> :
          <Icon color={color}>{active_icon || icon}</Icon>
      }
      sx={sx}
    />
  )
}
