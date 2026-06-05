import Skeleton from "@mui/material/Skeleton"
import Box from "@mui/material/Box"

export function render({model}) {
  const [active] = model.useState("active")
  const [animation] = model.useState("animation")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const object = model.get_child("object")
  if (active) {
    return <Box sx={{display: "inline-flex", width: "100%", height: "100%", ...sx}}>{object}</Box>
  }

  // Pass width as a prop (not just sx): MUI forces maxWidth:fit-content when a
  // Skeleton has children and no explicit width prop, which would otherwise pin
  // the placeholder to the child's content width even on a stretched host.
  return (
    <Skeleton
      animation={animation ?? false}
      variant={variant}
      width="100%"
      sx={{width: "100%", height: "100%", ...sx}}
    >
      <Box sx={{display: "inline-flex", width: "100%", height: "100%", visibility: "hidden"}}>
        {object}
      </Box>
    </Skeleton>
  )
}
