import Skeleton from "@mui/material/Skeleton"

export function render({model}) {
  const [animation] = model.useState("animation")
  const [color] = model.useState("color")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")

  return (
    <Skeleton animation={animation ?? false} variant={variant} sx={{width: "100%", height: "100%", bgcolor: color, ...sx}}/>
  )
}
