import Collapse from "@mui/material/Collapse"
import Fade from "@mui/material/Fade"
import Grow from "@mui/material/Grow"
import Slide from "@mui/material/Slide"
import Zoom from "@mui/material/Zoom"
import Box from "@mui/material/Box"

const VARIANTS = {
  collapse: Collapse,
  fade: Fade,
  grow: Grow,
  slide: Slide,
  zoom: Zoom,
}

export function render({model}) {
  const [active] = model.useState("active")
  const [duration] = model.useState("duration")
  const [orientation] = model.useState("orientation")
  const [placement] = model.useState("placement")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const object = model.get_child("object")

  const Transition = VARIANTS[variant]

  const timeoutProp = duration != null ? {timeout: duration} : {}
  const extraProps = {}
  if (variant === "slide") {
    extraProps.direction = placement
  }
  if (variant === "collapse") {
    extraProps.orientation = orientation
  }

  return (
    <Transition in={active} {...timeoutProp} {...extraProps} sx={sx}>
      <Box sx={{display: "inline-flex"}}>
        {object}
      </Box>
    </Transition>
  )
}
