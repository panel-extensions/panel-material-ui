import Dialog from "@mui/material/Dialog"
import DialogActions from "@mui/material/DialogActions"
import DialogContent from "@mui/material/DialogContent"
import DialogTitle from "@mui/material/DialogTitle"
import IconButton from "@mui/material/IconButton"
import CloseIcon from "@mui/icons-material/Close"
import Box from "@mui/material/Box"
import {apply_flex, child_model, render_icon_text, overlay_container} from "./utils"

const SMALL_SCREEN = "@media (max-width: 599.95px)"

function useOverflow(el, deps) {
  const [overflowing, setOverflowing] = React.useState(false)
  React.useEffect(() => {
    if (el == null) {
      return
    }
    const check = () => setOverflowing(el.scrollHeight - el.clientHeight > 1)
    const observer = new ResizeObserver(check)
    observer.observe(el)
    for (const child of el.children) {
      observer.observe(child)
    }
    check()
    return () => observer.disconnect()
  }, [el, ...deps])
  return overflowing
}

export function render({model, view}) {
  const [close_on_click] = model.useState("close_on_click")
  const [close_on_escape] = model.useState("close_on_escape")
  const [full_screen] = model.useState("full_screen")
  const [open, setOpen] = model.useState("open")
  const [title] = model.useState("title")
  const [scroll] = model.useState("scroll")
  const [show_close_button] = model.useState("show_close_button")
  const [sx] = model.useState("sx")
  const [title_variant] = model.useState("title_variant")
  const [width_option] = model.useState("width_option")
  const objects = model.get_child("objects")
  const actions = model.get_child("actions")

  const [content, setContent] = React.useState(null)
  // Dividers mark the edges of the content only while it scrolls inside the paper.
  const dividers = useOverflow(content, [objects.length]) && scroll === "paper"

  const fullWidth = view.model.sizing_mode === "stretch_width" || view.model.sizing_mode === "stretch_both"
  const has_header = Boolean(title) || show_close_button
  const has_actions = actions.length > 0

  const onClose = (event, reason) => {
    if ((reason === "backdropClick" && close_on_click) || (reason === "escapeKeyDown" && close_on_escape)) {
      setOpen(false)
    }
  }

  // MUI keeps a 32px margin around the paper; on phones that wastes a fifth of the width.
  const paperSx = full_screen ? {} : {
    minWidth: "min(360px, calc(100% - 64px))",
    [SMALL_SCREEN]: {
      margin: 2,
      minWidth: "calc(100% - 32px)",
      maxWidth: "calc(100% - 32px)",
      maxHeight: "calc(100% - 32px)",
      ...(fullWidth ? {width: "calc(100% - 32px)"} : {}),
    },
  }

  return (
    <Dialog
      container={overlay_container(view.container)}
      fullScreen={full_screen}
      fullWidth={fullWidth}
      maxWidth={width_option}
      open={open}
      onClose={onClose}
      scroll={scroll}
      slotProps={{paper: {sx: paperSx}}}
      sx={sx}
    >
      {has_header && (
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-end",
            gap: 1,
            pr: show_close_button ? 1.5 : 0,
            pt: title ? 0 : 1.5,
            borderBottom: dividers ? 1 : 0,
            borderColor: "divider",
          }}
        >
          {title && (
            <DialogTitle
              variant={title_variant}
              sx={{flex: "1 1 auto", minWidth: 0, pr: show_close_button ? 0 : 3, overflowWrap: "anywhere"}}
            >
              {render_icon_text(title)}
            </DialogTitle>
          )}
          {show_close_button && (
            <IconButton
              aria-label="close"
              onClick={() => setOpen(false)}
              size="small"
              sx={{flexShrink: 0, color: "text.secondary"}}
            >
              <CloseIcon />
            </IconButton>
          )}
        </Box>
      )}
      <DialogContent
        ref={setContent}
        sx={{
          display: "flex",
          flexDirection: "column",
          px: 2,
          pt: (has_header && !dividers) ? 0 : 1,
          pb: has_actions ? 0 : 2,
        }}
      >
        {objects}
      </DialogContent>
      {has_actions && (
        <DialogActions
          sx={{
            px: 2,
            pt: dividers ? 1 : 0.5,
            pb: 1.5,
            flexWrap: "wrap",
            "& > :not(style) ~ :not(style)": {ml: 0},
            borderTop: dividers ? 1 : 0,
            borderColor: "divider",
          }}
        >
          {actions.map((action, index) => {
            apply_flex(view.get_child_view(child_model(model.actions, action, index)), "row")
            return action
          })}
        </DialogActions>
      )}
    </Dialog>
  )
}
