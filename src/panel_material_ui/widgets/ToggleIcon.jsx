import Box from "@mui/material/Box"
import Checkbox from "@mui/material/Checkbox"
import Typography from "@mui/material/Typography"

const SIZES = {
  small: "1.5em",
  medium: "2.5em",
  large: "3.5em",
}

export function render({model, el}) {
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [size] = model.useState("size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")

  const standard_size = ["small", "medium", "large"].includes(size)
  const font_size = standard_size ? null : size
  const color_state = disabled ? "disabled" : color
  const text_size = standard_size ? SIZES[size] : font_size

  return (
    <Box sx={{display: "flex", alignItems: "center", flexDirection: "row"}}>
      <Checkbox
        checked={value}
        color={color_state}
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
              width: text_size,
              height: text_size,
              display: "inline-block"}}
            /> :
            <Icon
              baseClassName={"material-icons-outlined"}
              color={color_state}
              style={{fontSize: font_size}}
            >
              {icon}
            </Icon>
        }
        checkedIcon={
          active_icon.trim().startsWith("<") ?
            <span style={{
              maskImage: `url("data:image/svg+xml;base64,${btoa(active_icon || icon)}")`,
              backgroundColor: "currentColor",
              maskRepeat: "no-repeat",
              maskSize: "contain",
              width: text_size,
              height: text_size,
              display: "inline-block"}}
            /> :
            <Icon color={color_state} style={{fontSize: font_size}}>{active_icon || icon}</Icon>
        }
        sx={sx}
      />
      {label && <Typography sx={{color: "text.primary", fontSize: `calc(${text_size} / 2)`}}>{label}</Typography>}
    </Box>
  )
}
