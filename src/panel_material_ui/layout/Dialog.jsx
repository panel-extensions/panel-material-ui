import Dialog from "@mui/material/Dialog"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"

export function render({model, view}) {
  const [full_screen] = model.useState("full_screen")
  const [open] = model.useState("open")
  const [title] = model.useState("title")
  const [scroll] = model.useState("scroll")
  const [sx] = model.useState("sx")
  const [width_option] = model.useState("width_option")
  const objects = model.get_child("objects")

  return (
    <Dialog
      container={view.container}
      fullScreen={full_screen}
      fullWidth={view.model.sizing_mode === "stretch_width" || view.model.sizing_mode === "stretch_both"}
      maxWidth={width_option}
      open={open}
      scroll={scroll}
      sx={sx}
    >
      <DialogTitle>
        {title}
      </DialogTitle>
      <DialogContent sx={{display: "flex", flexDirection: "column"}}>
        {objects}
      </DialogContent>
    </Dialog>
  )
}
