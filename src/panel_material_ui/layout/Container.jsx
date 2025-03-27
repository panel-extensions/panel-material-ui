import Container from "@mui/material/Container"

export function render({model}) {
  const [disableGutters] = model.useState("disable_gutters")
  const [fixed] = model.useState("fixed")
  const [widthOption] = model.useState("width_option")
  const [objects] = model.get_child("objects")

  return (
    <Container disableGutters={disableGutters} fixed={fixed} maxWidth={widthOption}>
      {objects}
    </Container>
  )
}
