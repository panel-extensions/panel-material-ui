import Dialog from "@mui/material/Dialog"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"

export function render({model, view}) {
  const [full_screen] = model.useState("full_screen")
  const [open] = model.useState("open")
  const [title] = model.useState("title")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  React.useEffect(() => view.update_layout(), [open])

  if (open) {
    return (
      <Dialog open={open} fullScreen={full_screen} container={view.container} sx={sx}>
        <DialogTitle>
          {title}
        </DialogTitle>
        <DialogContent>
          {objects}
        </DialogContent>
      </Dialog>
    )
  } else {
    return null
  }
}
