import Box from "@mui/material/Box"
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")
  const flexDirection = model.esm_constants.direction

  let props = {}
  if (flexDirection === "flex") {
    const [alignItems] = model.useState("align_items")
    const [justifyContent] = model.useState("justify_content")
    const [gap] = model.useState("gap")
    const [flexWrap] = model.useState("flex_wrap")
    const [flex_direction] = model.useState("flex_direction")
    props = {
      alignItems,
      justifyContent,
      gap,
      flexWrap,
      flexDirection: flex_direction,
    }
  }

  React.useEffect(() => {
    model.on("lifecycle:update_layout", () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), flexDirection)
      })
    })
  }, [])

  return (
    <Box
      sx={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection,
        ...props,
        ...sx
      }}
    >
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), flexDirection)
        return object
      })}
    </Box>
  )
}
