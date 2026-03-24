import Backdrop from "@mui/material/Backdrop"

const BACKDROP_BASE_SX = {zIndex: (theme) => theme.zIndex.drawer + 1}

export function render({model, view}) {
  const [open] = model.useState("open")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  return (
    <Backdrop open={open} sx={sx ? [BACKDROP_BASE_SX, sx] : BACKDROP_BASE_SX}>
      {objects}
    </Backdrop>
  );
}
