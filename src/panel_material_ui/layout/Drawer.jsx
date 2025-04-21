import Drawer from "@mui/material/Drawer"

export function render({model}) {
  const [sx] = model.useState("sx")
  const [open, setOpen] = model.useState("open")
  const [anchor] = model.useState("anchor")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  return (
    <Drawer open={open} anchor={anchor} variant={variant} sx={{"& .MuiPaper-root": {padding: "5px"}, ...sx}} onClose={toggleDrawer(false)}>
      {objects}
    </Drawer>
  )
}
