import Box from "@mui/material/Box"
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")
  const direction = model.esm_constants.direction

  return (
    <Box
      sx={{height: "100%", width: "100%", display: "flex", flexDirection: direction, ...sx}}
    >
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), direction)
        return object
      })}
    </Box>
  )
}
