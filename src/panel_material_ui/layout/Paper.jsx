import Paper from "@mui/material/Paper"

export function render({model}) {
  const [direction] = model.useState("direction")
  const [elevation] = model.useState("elevation")
  const [square] = model.useState("square")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")

  return (
    <Paper
      elevation={elevation}
      square={square}
      sx={{height: "100%", width: "100%", display: "flex", flexDirection: direction, ...sx}}
      variant={variant}
    >
      {objects}
    </Paper>
  )
}
