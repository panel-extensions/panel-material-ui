import Fab from "@mui/material/Fab"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [href] = model.useState("href")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")

  return (
    <Fab
      aria-label={label}
      color={color}
      disabled={disabled}
      href={href}
      onClick={() => model.send_msg({type: "click"})}
      size={size}
      sx={sx}
      variant={variant}
    >
      {
        icon && (
          icon.trim().startsWith("<") ?
            <img src={`data:image/svg+xml;base64,${btoa(icon)}`} style={{width: "66%", height: "66%"}} /> :
            <Icon>{icon}</Icon>
        )
      }
      {variant === "extended" && label}
    </Fab>
  )
}
