import Drawer from "@mui/material/Drawer"

export function render({model, view}) {
  const [anchor] = model.useState("anchor")
  const [open, setOpen] = model.useState("open")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")

  let dims
  if (!["top", "bottom"].includes(anchor)) {
    dims = {width: `${size}px`}
  } else {
    dims = {height: `${size}px`}
  }
  return (
    <Drawer anchor={anchor} open={open} onClose={() => setOpen(false)} PaperProps={{sx: dims}} variant={variant}>
      {objects}
    </Drawer>
  )
}
