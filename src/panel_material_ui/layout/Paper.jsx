import Paper from "@mui/material/Paper"
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [direction] = model.useState("direction")
  const [elevation] = model.useState("elevation")
  const [square] = model.useState("square")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")

  React.useEffect(() => {
    model.on("lifecycle:update_layout", () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    })
  }, [])

  return (
    <Paper
      elevation={elevation}
      square={square}
      sx={{height: "100%", width: "100%", display: "flex", flexDirection: direction, ...sx}}
      variant={variant}
    >
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </Paper>
  )
}
