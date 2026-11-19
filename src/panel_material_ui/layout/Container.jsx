import Container from "@mui/material/Container"

const CONTAINER_BASE_SX = {
  height: "100%",
  width: "100%",
  display: "flex",
  flexDirection: "column",
}

export function render({model, host}) {
  const [disableGutters] = model.useState("disable_gutters")
  const [fixed] = model.useState("fixed")
  const [widthOption] = model.useState("width_option")
  const [sx] = model.useState("sx")
  const objects = model.render_children("objects", {direction: "column"})

  const containerSx = React.useMemo(
    () => [CONTAINER_BASE_SX, {minHeight: host.layout.min_height}, sx || {}],
    [host.layout.min_height, sx]
  )

  return (
    <Container
      disableGutters={disableGutters}
      fixed={fixed}
      maxWidth={widthOption || undefined}
      sx={containerSx}
    >
      {objects}
    </Container>
  )
}
