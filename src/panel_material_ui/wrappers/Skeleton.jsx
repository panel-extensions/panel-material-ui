import Skeleton from "@mui/material/Skeleton"
import Box from "@mui/material/Box"

export function render({model, view}) {
  const [active] = model.useState("active")
  const [animation] = model.useState("animation")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const object = model.get_child("object")

  // When the wrapped child is responsively sized, fill the available space so
  // the child (and the placeholder) can stretch; otherwise hug the child's
  // intrinsic size. Mirrors the sizing_mode check used by other components.
  const obj_model = view.model.data.object
  const isResponsive = obj_model && obj_model.sizing_mode && (
    obj_model.sizing_mode.includes("width") || obj_model.sizing_mode.includes("both")
  )
  const fill = isResponsive ? {width: "100%", height: "100%"} : {}

  if (active) {
    return <Box sx={{display: "inline-flex", ...fill, ...sx}}>{object}</Box>
  }

  return (
    <Skeleton
      animation={animation ?? false}
      variant={variant}
      sx={{width: "100%", height: "100%", ...sx}}
    >
      <Box sx={{display: "inline-flex", ...fill, visibility: "hidden"}}>
        {object}
      </Box>
    </Skeleton>
  )
}
