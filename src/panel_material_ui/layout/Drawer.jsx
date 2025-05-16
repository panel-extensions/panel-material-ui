import Drawer from "@mui/material/Drawer"
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [anchor] = model.useState("anchor")
  const [open, setOpen] = model.useState("open")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")

  let dims
  if (!["top", "bottom"].includes(anchor)) {
    dims = {width: `${size}px`}
    if (variant !== "temporary") {
      view.el.style.width = `${open ? size : 0}px`
    }
  } else {
    dims = {height: `${size}px`}
    if (variant !== "temporary") {
      view.el.style.width = `${open ? size : 0}px`
    }
  }

  React.useEffect(() => {
    model.on("lifecycle:update_layout", () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    })
  }, [])

  return (
    <Drawer anchor={anchor} open={open} onClose={() => setOpen(false)} PaperProps={{sx: {...dims, ...sx}}} variant={variant}>
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </Drawer>
  )
}
