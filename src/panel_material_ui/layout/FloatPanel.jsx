import Paper from "@mui/material/Paper"
import Box from "@mui/material/Box"
import IconButton from "@mui/material/IconButton"
import Typography from "@mui/material/Typography"
import Close from "@mui/icons-material/Close"
import CropSquare from "@mui/icons-material/CropSquare"
import FilterNone from "@mui/icons-material/FilterNone"
import Minimize from "@mui/icons-material/Minimize"

export function render({model, view}) {
  const [contained] = model.useState("contained")
  const [controls] = model.useState("controls")
  const [elevation] = model.useState("elevation")
  const [name] = model.useState("name")
  const [offsetx] = model.useState("offsetx")
  const [offsety] = model.useState("offsety")
  const [position] = model.useState("position")
  const [square] = model.useState("square")
  const [status, setStatus] = model.useState("status")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")
  const [location, setLocation] = React.useState(null)
  const [size, setSize] = React.useState(null)
  const paper = React.useRef(null)
  const header = React.useRef(null)
  const drag = React.useRef(null)
  const resizing = React.useRef(null)

  React.useEffect(() => {
    setLocation(null)
  }, [position, offsetx, offsety, contained])

  const bounds = () => contained ? view.el.getBoundingClientRect() : {
    left: 0, top: 0, right: window.innerWidth, bottom: window.innerHeight,
    width: window.innerWidth, height: window.innerHeight,
  }
  const move = (x, y) => {
    const rect = paper.current.getBoundingClientRect()
    const container = bounds()
    const next = [
      Math.max(0, Math.min(x, Math.max(0, container.width - rect.width))),
      Math.max(0, Math.min(y, Math.max(0, container.height - rect.height))),
    ]
    setLocation(next)
  }

  const startDrag = (event) => {
    if (event.button !== 0 || (event.target !== paper.current && event.target !== header.current)) { return }
    const rect = paper.current.getBoundingClientRect()
    const container = bounds()
    drag.current = {x: event.clientX, y: event.clientY, left: rect.left - container.left, top: rect.top - container.top}
    event.currentTarget.setPointerCapture(event.pointerId)
    event.preventDefault()
  }

  const onPointerMove = (event) => {
    if (!drag.current) { return }
    const {x, y, left, top} = drag.current
    move(left + event.clientX - x, top + event.clientY - y)
  }

  const endDrag = () => { drag.current = null }

  const startResize = (event) => {
    if (event.button !== 0) { return }
    const rect = paper.current.getBoundingClientRect()
    const container = bounds()
    resizing.current = {x: event.clientX, y: event.clientY, width: rect.width, height: rect.height}
    setLocation([rect.left - container.left, rect.top - container.top])
    event.currentTarget.setPointerCapture(event.pointerId)
    event.stopPropagation()
    event.preventDefault()
  }

  const onResize = (event) => {
    if (!resizing.current) { return }
    const {x, y, width: initialWidth, height: initialHeight} = resizing.current
    const rect = paper.current.getBoundingClientRect()
    const container = bounds()
    setSize([
      Math.max(180, Math.min(initialWidth + event.clientX - x, Math.max(180, container.right - rect.left))),
      Math.max(40, Math.min(initialHeight + event.clientY - y, Math.max(40, container.bottom - rect.top))),
    ])
  }

  const endResize = () => { resizing.current = null }

  const onKeyDown = (event) => {
    const offsets = {ArrowLeft: [-10, 0], ArrowRight: [10, 0], ArrowUp: [0, -10], ArrowDown: [0, 10]}
    const delta = offsets[event.key]
    if (!delta || event.target !== paper.current) { return }
    event.preventDefault()
    const rect = paper.current.getBoundingClientRect()
    const container = bounds()
    move(rect.left - container.left + delta[0], rect.top - container.top + delta[1])
  }

  const [horizontal, vertical] = position.split("-")
  const maximized = status === "maximized" || status === "smallifiedmax"
  const collapsed = status === "minimized" || status.startsWith("smallified")
  const positioned = location ? {left: location[0], top: location[1]} : {
    left: horizontal === "left" ? offsetx : horizontal === "center" || !vertical ? `calc(50% + ${offsetx}px)` : undefined,
    right: horizontal === "right" ? offsetx : undefined,
    top: vertical === "top" ? offsety : vertical === "center" || !vertical ? `calc(50% + ${offsety}px)` : undefined,
    bottom: vertical === "bottom" ? offsety : undefined,
    transform: `translate(${horizontal === "center" || !vertical ? "-50%" : "0"}, ${vertical === "center" || !vertical ? "-50%" : "0"})`,
  }

  view.el.style.position = contained ? "relative" : "static"
  view.el.style.width = contained ? "100%" : "0px"
  view.el.style.height = contained ? "100%" : "0px"

  return status === "closed" ? null : (
    <Paper
      ref={paper}
      aria-label="Floating panel"
      elevation={elevation}
      onPointerDown={startDrag}
      onPointerMove={onPointerMove}
      onPointerUp={endDrag}
      onPointerCancel={endDrag}
      onKeyDown={onKeyDown}
      role="group"
      square={square}
      tabIndex={0}
      variant={variant}
      sx={[{
        position: contained ? "absolute" : "fixed", zIndex: "modal",
        ...(maximized ? {inset: 0, transform: "none"} : positioned),
        width: maximized ? "100%" : (size ? size[0] : model.width || "max-content"), minWidth: 180,
        height: maximized ? "100%" : (size ? size[1] : model.height || undefined),
        maxWidth: "100%", maxHeight: "100%", overflow: "auto",
        display: "flex", flexDirection: "column", cursor: "grab",
        touchAction: "none",
      }, sx || {}]}
    >
      <Box ref={header} sx={{display: "flex", alignItems: "center", minHeight: 36, px: 1}}>
        <Typography variant="subtitle2" sx={{flex: 1, pointerEvents: "none"}}>{name}</Typography>
        {controls.includes("minimize") && <IconButton size="small" aria-label={collapsed ? "Restore floating panel" : "Minimize floating panel"}
          onClick={() => setStatus(collapsed ? "normalized" : "minimized")}
        >
          <Minimize fontSize="small" />
        </IconButton>}
        {controls.includes("maximize") && <IconButton size="small" aria-label={maximized ? "Restore size" : "Maximize floating panel"}
          onClick={() => setStatus(maximized ? "normalized" : "maximized")}
        >
          {maximized ? <FilterNone fontSize="small" /> : <CropSquare fontSize="small" />}
        </IconButton>}
        {controls.includes("close") && <IconButton size="small" aria-label="Close floating panel" onClick={() => setStatus("closed")}>
          <Close fontSize="small" />
        </IconButton>}
      </Box>
      {!collapsed && <Box sx={{display: "flex", flexDirection: "column", gap: 1, p: 1}}>{objects}</Box>}
      {!maximized && !collapsed && <Box
        aria-label="Resize floating panel"
        onPointerDown={startResize}
        onPointerMove={onResize}
        onPointerUp={endResize}
        onPointerCancel={endResize}
        sx={{position: "absolute", right: 0, bottom: 0, width: 16, height: 16, cursor: "nwse-resize", touchAction: "none"}}
      />}
    </Paper>
  )
}
