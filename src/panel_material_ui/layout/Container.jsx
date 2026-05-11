import Container from "@mui/material/Container"
import {apply_flex} from "./utils"

const CONTAINER_BASE_SX = {
  height: "100%",
  width: "100%",
  display: "flex",
  flexDirection: "column",
}

export function render({model, view}) {
  const [disableGutters] = model.useState("disable_gutters")
  const [fixed] = model.useState("fixed")
  const [widthOption] = model.useState("width_option")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  React.useEffect(() => {
    const handler = () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    }
    model.on("lifecycle:update_layout", handler)
    return () => model.off("lifecycle:update_layout", handler)
  }, [])

  const containerSx = React.useMemo(
    () => [CONTAINER_BASE_SX, {minHeight: model.min_height}, sx || {}],
    [model.min_height, sx]
  )

  return (
    <Container
      disableGutters={disableGutters}
      fixed={fixed}
      maxWidth={widthOption || undefined}
      sx={containerSx}
    >
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </Container>
  )
}
