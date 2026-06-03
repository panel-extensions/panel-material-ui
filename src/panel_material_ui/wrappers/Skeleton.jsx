import Skeleton from "@mui/material/Skeleton"
import Box from "@mui/material/Box"

export function render({model}) {
  const [active] = model.useState("active")
  const [animation] = model.useState("animation")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const object = model.get_child("object")

  if (active) {
    return <Box sx={{display: "inline-flex"}}>{object}</Box>
  }

  return (
    <Skeleton
      animation={animation ?? false}
      variant={variant}
      sx={{width: "100%", height: "100%", ...sx}}
    >
      <Box sx={{display: "inline-flex", visibility: "hidden"}}>
        {object}
      </Box>
    </Skeleton>
  )
}
