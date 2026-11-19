import Paper from "@mui/material/Paper"

const PAPER_BASE_SX = {
  height: "100%",
  width: "100%",
  display: "flex",
}

export function render({model, host}) {
  const [direction] = model.useState("direction")
  const [elevation] = model.useState("elevation")
  const [square] = model.useState("square")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.render_children("objects", {direction: "column"})

  const paperSx = React.useMemo(
    () => [PAPER_BASE_SX, {flexDirection: direction}, sx || {}],
    [direction, sx]
  )

  return (
    <Paper
      elevation={elevation}
      square={square}
      sx={paperSx}
      variant={variant}
    >
      {objects}
    </Paper>
  )
}
