import Paper from "@mui/material/Paper"
import {apply_flex} from "./utils"

const PAPER_BASE_SX = {
  height: "100%",
  width: "100%",
  display: "flex",
}

export function render({model, view}) {
  const [direction] = model.useState("direction")
  const [elevation] = model.useState("elevation")
  const [square] = model.useState("square")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
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
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </Paper>
  )
}
