import Paper from "@mui/material/Paper"

export function render({model}) {
  const [elevation] = model.useState("elevation")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  return (
    <Paper elevation={elevation} sx={{height: "100%", width: "100%", ...sx}}>
      {objects}
    </Paper>
  )
}
