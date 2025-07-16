import Chip from "@mui/material/Chip"
import Icon from "@mui/material/Icon"

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

  const standard_size = ["small", "medium"].includes(size)
  const font_size = standard_size ? null : size
  const text_size = standard_size ? SIZES[size] : font_size

  return (
    <Chip
      color={color}
      icon={
        icon ? (icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: text_size,
            height: text_size,
            display: "inline-block"}}
          /> :
          <Icon
            baseClassName={"material-icons-outlined"}
            style={{fontSize: font_size}}
          >
            {icon}
          </Icon>) : null
      }
      label={label}
      size={size}
      sx={sx}
      variant={variant}
      onClick={(e) => model.send_event("click", e)}
    />
  )
}
