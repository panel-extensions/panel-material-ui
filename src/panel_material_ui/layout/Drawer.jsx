import Drawer from "@mui/material/Drawer"

export function render({model, view}) {
  const [open, setOpen] = model.useState("open")
  const objects = model.get_child("objects")

  const anchorEl = view.parent.element_views.includes(view) ? view.parent.el : null

  return (
    <Drawer anchorEl={anchorEl} open={open} onOpen={() => setOpen(true)} onClose={() => setOpen(false)}>
      {objects}
    </Drawer>
  )
}
