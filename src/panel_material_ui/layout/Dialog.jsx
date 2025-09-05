import Dialog from "@mui/material/Dialog"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"
import IconButton from "@mui/material/IconButton"
import CloseIcon from "@mui/icons-material/Close"
import Box from "@mui/material/Box"

export function render({model, view}) {
  const [close_on_click] = model.useState("close_on_click")
  const [full_screen] = model.useState("full_screen")
  const [open, setOpen] = model.useState("open")
  const [title] = model.useState("title")
  const [scroll] = model.useState("scroll")
  const [show_close_button] = model.useState("show_close_button")
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
      onClose={() => close_on_click && setOpen(false)}
      scroll={scroll}
      sx={sx}
    >
      {(title || show_close_button) &&
      <Box sx={{display: "flex", alignItems: "center", justifyContent: "space-between"}}>
        {title && <DialogTitle variant="h3">{title}</DialogTitle>}
        {show_close_button && (
          <IconButton
            aria-label="close"
            onClick={() => setOpen(false)}
            size="small"
            sx={title ? {alignSelf: "start"} : {ml: "auto"}}
          >
            <CloseIcon />
          </IconButton>
        )}
      </Box>}
      <DialogContent sx={{display: "flex", flexDirection: "column", p: "0 1em 0.5em"}}>
        {objects}
      </DialogContent>
    </Dialog>
  )
}
