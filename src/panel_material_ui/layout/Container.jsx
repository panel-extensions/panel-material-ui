import Container from "@mui/material/Container"
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [disableGutters] = model.useState("disable_gutters")
  const [fixed] = model.useState("fixed")
  const [widthOption] = model.useState("width_option")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  React.useEffect(() => {
    model.on("lifecycle:update_layout", () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    })
  }, [])

  return (
    <Container
      disableGutters={disableGutters}
      fixed={fixed}
      maxWidth={widthOption}
      sx={{height: "100%", minHeight: model.min_height, width: "100%", display: "flex", flexDirection: "column", ...sx}}
    >
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </Container>
  )
}
