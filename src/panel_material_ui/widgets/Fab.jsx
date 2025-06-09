import Fab from "@mui/material/Fab"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [href] = model.useState("href")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [target] = model.useState("target")
  const [variant] = model.useState("variant")

  const padding = variant === "extended" ? "1.2em" : "0"

  return (
    <Fab
      aria-label={label}
      color={color}
      disabled={disabled}
      href={href}
      onClick={() => model.send_event("click", {})}
      size={size}
      sx={sx}
      target={target}
      variant={variant}
    >
      {
        icon && (
          icon.trim().startsWith("<") ?
            <span style={{
              maskImage: `url("data:image/svg+xml;base64,${btoa(icon)}")`,
              backgroundColor: "currentColor",
              maskRepeat: "no-repeat",
              maskSize: "contain",
              width: icon_size,
              height: icon_size,
              paddingRight: padding,
              display: "inline-block"}}
            /> :
            <Icon style={{fontSize: icon_size}} sx={{pr: padding}}>{icon}</Icon>
        )
      }
      {variant === "extended" && label}
    </Fab>
  )
}
