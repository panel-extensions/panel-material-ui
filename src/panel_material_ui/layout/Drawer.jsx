import Drawer from "@mui/material/Drawer"
import Paper from "@mui/material/Paper"
import {apply_flex, render_icon} from "./utils"

const TAB_SIZE = 24
const TAB_LENGTH = 48

const anchorToChevron = {
  left: {open: "chevron_left", closed: "chevron_right"},
  right: {open: "chevron_right", closed: "chevron_left"},
  top: {open: "expand_less", closed: "expand_more"},
  bottom: {open: "expand_more", closed: "expand_less"},
}

function getPositionStyle(anchor, dockPosition) {
  const isHorizontal = anchor === "left" || anchor === "right"
  if (isHorizontal) {
    switch (dockPosition) {
      case "start": return {top: `${TAB_LENGTH}px`}
      case "end": return {bottom: `${TAB_LENGTH}px`}
      default: return {top: "50%", transform: "translateY(-50%)"}
    }
  } else {
    switch (dockPosition) {
      case "start": return {left: `${TAB_LENGTH}px`}
      case "end": return {right: `${TAB_LENGTH}px`}
      default: return {left: "50%", transform: "translateX(-50%)"}
    }
  }
}

function DockedTab({anchor, open, dockPosition, attached, inline, onClick, icon: customIcon}) {
  const isHorizontal = anchor === "left" || anchor === "right"
  const icon = customIcon || anchorToChevron[anchor][open ? "open" : "closed"]

  const positionStyles = (() => {
    if (inline) { return {} }
    if (attached) {
      const offsetSide = anchor === "left" ? "right" : anchor === "right" ? "left" : anchor === "top" ? "bottom" : "top"
      return {
        [offsetSide]: `-${TAB_SIZE + 1}px`,
        ...getPositionStyle(anchor, dockPosition),
      }
    }
    return {
      [anchor]: 0,
      ...getPositionStyle(anchor, dockPosition),
    }
  })()

  const tabStyle = {
    position: inline ? "relative" : "absolute",
    ...positionStyles,
    width: isHorizontal ? `${TAB_SIZE}px` : `${TAB_LENGTH}px`,
    height: isHorizontal ? `${TAB_LENGTH}px` : `${TAB_SIZE}px`,
    ...(inline && isHorizontal ? {height: "100%"} : {}),
    ...(inline && !isHorizontal ? {width: "100%"} : {}),
    minWidth: 0,
    minHeight: 0,
    padding: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    zIndex: 1,
    borderRadius: (() => {
      switch (anchor) {
        case "left": return "0 4px 4px 0"
        case "right": return "4px 0 0 4px"
        case "top": return "0 0 4px 4px"
        case "bottom": return "4px 4px 0 0"
      }
    })(),
  }

  return (
    <Paper
      elevation={2}
      sx={tabStyle}
      onClick={onClick}
      role="button"
      aria-label={open ? "Close drawer" : "Open drawer"}
    >
      {render_icon(icon, null, null, "1.2rem")}
    </Paper>
  )
}

export function render({model, view}) {
  const [anchor] = model.useState("anchor")
  const [dockIcon] = model.useState("dock_icon")
  const [dockPosition] = model.useState("dock_position")
  const [inline] = model.useState("inline")
  const [open, setOpen] = model.useState("open")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")

  const isDocked = variant === "docked"
  const isHorizontal = anchor === "left" || anchor === "right"

  let dims
  if (!["top", "bottom"].includes(anchor)) {
    dims = {width: `${size}px`}
    if (!inline && !["temporary", "docked"].includes(variant)) {
      view.el.style.width = `${open ? size : 0}px`
    }
  } else {
    dims = {height: `${size}px`}
    if (!inline && !["temporary", "docked"].includes(variant)) {
      view.el.style.height = `${open ? size : 0}px`
    }
  }

  React.useEffect(() => {
    const handler = () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    }
    model.on("lifecycle:update_layout", handler)
    return () => model.off("lifecycle:update_layout", handler)
  }, [])

  // Update view.el dimensions so Panel's layout system tracks our size when inline.
  React.useEffect(() => {
    if (!inline) { return }
    if (isDocked) {
      if (isHorizontal) {
        view.el.style.width = open ? `${size + TAB_SIZE}px` : "0px"
        view.el.style.height = "100%"
        view.el.style.overflow = "visible"
      } else {
        view.el.style.height = open ? `${size + TAB_SIZE}px` : "0px"
        view.el.style.width = "100%"
        view.el.style.overflow = "visible"
      }
    } else {
      if (isHorizontal) {
        view.el.style.width = `${open ? size : 0}px`
        view.el.style.height = "100%"
      } else {
        view.el.style.height = `${open ? size : 0}px`
        view.el.style.width = "100%"
      }
    }
  }, [inline, isDocked, open, size, isHorizontal])

  if (isDocked) {
    if (inline) {
      // Inline docked: container collapses to 0 when closed; the tab is absolutely
      // positioned so it overlays adjacent content rather than pushing it.
      const containerStyle = {
        position: "relative",
        [isHorizontal ? "width" : "height"]: open ? `${size + TAB_SIZE}px` : "0px",
        [isHorizontal ? "height" : "width"]: "100%",
        transition: "width 225ms cubic-bezier(0, 0, 0.2, 1), height 225ms cubic-bezier(0, 0, 0.2, 1)",
        overflow: "visible",
        pointerEvents: "none",
        flexShrink: 0,
      }

      const innerStyle = {
        position: "relative",
        width: "100%",
        height: "100%",
        pointerEvents: "auto",
      }

      const closedTabStyle = (() => {
        const offsetSide = anchor === "left" ? "right" : anchor === "right" ? "left" : anchor === "top" ? "bottom" : "top"
        return {
          position: "absolute",
          [offsetSide]: `-${TAB_SIZE}px`,
          ...getPositionStyle(anchor, dockPosition),
          width: isHorizontal ? `${TAB_SIZE}px` : `${TAB_LENGTH}px`,
          height: isHorizontal ? `${TAB_LENGTH}px` : `${TAB_SIZE}px`,
          pointerEvents: "auto",
          zIndex: 1200,
        }
      })()

      return (
        <div style={containerStyle}>
          <div style={innerStyle}>
            <Drawer
              anchor={anchor}
              open={open}
              onClose={() => setOpen(false)}
              slotProps={{paper: {sx: [dims, {overflow: "visible"}, sx || {}]}}}
              variant="persistent"
              sx={{"& .MuiDrawer-root": {position: "absolute"}, "& .MuiPaper-root": {position: "absolute"}}}
            >
              {objects.map((object, index) => {
                apply_flex(view.get_child_view(model.objects[index]), "column")
                return object
              })}
              <DockedTab anchor={anchor} open={open} dockPosition={dockPosition} attached onClick={() => setOpen(false)} />
            </Drawer>
            {!open && (
              <div style={closedTabStyle}>
                <DockedTab anchor={anchor} open={false} dockPosition={dockPosition} inline attached={false} onClick={() => setOpen(true)} />
              </div>
            )}
          </div>
        </div>
      )
    }

    // Fixed docked: tab strip fixed to the page edge.
    const containerStyle = {
      position: "fixed",
      top: 0,
      [anchor]: 0,
      [isHorizontal ? "width" : "height"]: open ? `${size + TAB_SIZE}px` : `${TAB_SIZE}px`,
      [isHorizontal ? "height" : "width"]: "100%",
      zIndex: 1200,
      pointerEvents: "none",
    }

    const innerStyle = {
      position: "relative",
      [isHorizontal ? "width" : "height"]: "100%",
      [isHorizontal ? "height" : "width"]: "100%",
      pointerEvents: "auto",
    }

    return (
      <div style={containerStyle}>
        <div style={innerStyle}>
          <Drawer
            anchor={anchor}
            open={open}
            onClose={() => setOpen(false)}
            slotProps={{paper: {sx: [dims, {overflow: "visible"}, sx || {}]}}}
            variant="persistent"
          >
            {objects.map((object, index) => {
              apply_flex(view.get_child_view(model.objects[index]), "column")
              return object
            })}
            <DockedTab anchor={anchor} open={open} dockPosition={dockPosition} attached onClick={() => setOpen(false)} icon={dockIcon} />
          </Drawer>
          {!open && (
            <DockedTab anchor={anchor} open={false} dockPosition={dockPosition} attached={false} onClick={() => setOpen(true)} icon={dockIcon} />
          )}
        </div>
      </div>
    )
  }

  // For temporary / persistent / permanent: use MUI Drawer directly.
  // When inline, render inside the parent's flow (position: relative container) so
  // siblings are pushed rather than overlaid.
  const slotProps = {paper: {sx: [dims, sx || {}]}}
  if (inline) {
    return (
      <div style={{position: "relative", overflow: "hidden", [isHorizontal ? "height" : "width"]: "100%"}}>
        <Drawer
          anchor={anchor}
          open={open}
          onClose={() => setOpen(false)}
          slotProps={slotProps}
          variant={variant === "temporary" ? "persistent" : variant}
          sx={{"& .MuiDrawer-root": {position: "absolute"}, "& .MuiPaper-root": {position: "absolute"}}}
        >
          {objects.map((object, index) => {
            apply_flex(view.get_child_view(model.objects[index]), "column")
            return object
          })}
        </Drawer>
      </div>
    )
  }

  return (
    <Drawer anchor={anchor} open={open} onClose={() => setOpen(false)} slotProps={slotProps} variant={variant}>
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </Drawer>
  )
}
