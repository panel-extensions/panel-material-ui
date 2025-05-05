import Button from "@mui/material/Button"

export function render({model, el}) {
  const [color] = model.useState("color")
  const [disableElevation] = model.useState("disable_elevation")
  const [disabled] = model.useState("disabled")
  const [href] = model.useState("href")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  return (
    <Button
      color={color}
      disableElevation={disableElevation}
      disabled={disabled}
      fullWidth
      size={size}
      href={href}
      loading={loading}
      loadingPosition="start"
      onClick={() => model.send_event("click", {})}
      startIcon={icon && (
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
      sx={sx}
      variant={variant}
    >
      {label}
    </Button>
  )
}
