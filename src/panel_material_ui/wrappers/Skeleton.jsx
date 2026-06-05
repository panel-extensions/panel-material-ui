import Skeleton from "@mui/material/Skeleton"
import Box from "@mui/material/Box"

export function render({model, view}) {
  const [active] = model.useState("active")
  const [animation] = model.useState("animation")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const object = model.get_child("object")

  // Fill the available space along whichever axes the wrapped child is
  // responsively sized, otherwise hug its intrinsic size. Mirrors the
  // child sizing_mode check used in ChatMessage/Details/Page.
  const sizing = (view.model.data.object || {}).sizing_mode || ""
  const fill = {
    ...(sizing.includes("width") || sizing.includes("both") ? {width: "100%"} : {}),
    ...(sizing.includes("height") || sizing.includes("both") ? {height: "100%"} : {}),
  }

  if (active) {
    return <Box sx={{display: "inline-flex", ...fill, ...sx}}>{object}</Box>
  }

  // Pass width/height as props (not just sx): MUI forces maxWidth:fit-content
  // when a Skeleton has children and no explicit width prop, which would
  // otherwise collapse the placeholder to the child's content width.
  return (
    <Skeleton
      animation={animation ?? false}
      variant={variant}
      {...fill}
      sx={{width: "100%", height: "100%", ...sx}}
    >
      <Box sx={{display: "inline-flex", ...fill, visibility: "hidden"}}>
        {object}
      </Box>
    </Skeleton>
  )
}
