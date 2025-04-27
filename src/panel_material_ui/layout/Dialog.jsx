import Dialog from "@mui/material/Dialog"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [full_screen] = model.useState("full_screen")
  const [open] = model.useState("open")
  const [title] = model.useState("title")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  return (
    <Dialog open={open} fullScreen={full_screen} container={view.container} sx={sx}>
      <DialogTitle>
        {title}
      </DialogTitle>
      <DialogContent sx={{display: "flex", flexDirection: "column"}}>
        {objects.map((object, index) => {
          apply_flex(view.get_child_view(model.objects[index]), "column")
          return object
        })}
      </DialogContent>
    </Dialog>
  )
}
