import Popover from "@mui/material/Popover"
import {apply_flex} from "./utils"

export function render({model, view}, ref) {
  const [anchor_origin] = model.useState("anchor_origin")
  const [anchor_position] = model.useState("anchor_position")
  const [close_on_click] = model.useState("close_on_click")
  const [elevation] = model.useState("elevation")
  const [enforce_focus] = model.useState("enforce_focus")
  const [hide_backdrop] = model.useState("hide_backdrop")
  const [open, setOpen] = model.useState("open")
  const [sx] = model.useState("sx")
  const [transform_origin] = model.useState("transform_origin")
  const objects = model.get_child("objects")

  const anchorEl = view.parent?.child_views.includes(view) ? view.parent.el : null

  React.useEffect(() => {
    model.on("lifecycle:update_layout", () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    })
  }, [])

  return (
    <Popover
      anchorEl={anchorEl}
      anchorOrigin={anchor_origin}
      anchorPosition={anchor_position ? {left: anchor_position[1], top: anchor_position[0]} : undefined}
      anchorReference={anchor_position == null ? "anchorEl" : "anchorPosition"}
      container={view.container}
      disableEnforceFocus={!enforce_focus}
      elevation={elevation}
      marginThreshold={0}
      hideBackdrop={hide_backdrop}
      onClose={() => close_on_click && setOpen(false)}
      open={open}
      sx={sx}
      transformOrigin={transform_origin ?? undefined}
    >
      {objects}
    </Popover>
  )
}
