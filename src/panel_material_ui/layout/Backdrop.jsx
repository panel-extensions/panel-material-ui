import Backdrop from "@mui/material/Backdrop"

export function render({model, view}) {
  const [open] = model.useState("open")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  return (
    <Backdrop open={open} sx={{zIndex: (theme) => theme.zIndex.drawer + 1, ...sx}}>
      {objects}
    </Backdrop>
  );
}
