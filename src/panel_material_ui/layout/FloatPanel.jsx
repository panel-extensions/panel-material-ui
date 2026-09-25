import Box from "@mui/material/Box"
import Paper from "@mui/material/Paper"
import DragIndicator from "@mui/icons-material/DragIndicator"

export function render({model}) {
  const [elevation] = model.useState("elevation")
  const [position, setPosition] = model.useState("position")
  const [square] = model.useState("square")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")
  const [location, setLocation] = React.useState(position)
  const paper = React.useRef(null)
  const drag = React.useRef(null)
  const locationRef = React.useRef(position)

  React.useEffect(() => {
    if (drag.current) { return }
    locationRef.current = position
    setLocation(position)
  }, [position])

  const move = (x, y) => {
    const rect = paper.current.getBoundingClientRect()
    const next = [
      Math.max(0, Math.min(x, window.innerWidth - rect.width)),
      Math.max(0, Math.min(y, window.innerHeight - rect.height)),
    ]
    locationRef.current = next
    setLocation(next)
  }

  const startDrag = (event) => {
    if (event.button !== 0) { return }
    drag.current = {x: event.clientX, y: event.clientY, position: locationRef.current}
    event.currentTarget.setPointerCapture(event.pointerId)
    event.preventDefault()
  }

  const onPointerMove = (event) => {
    if (!drag.current) { return }
    const {x, y, position: origin} = drag.current
    move(origin[0] + event.clientX - x, origin[1] + event.clientY - y)
  }

  const endDrag = () => {
    if (!drag.current) { return }
    drag.current = null
    setPosition(locationRef.current)
  }

  const onKeyDown = (event) => {
    const offsets = {ArrowLeft: [-10, 0], ArrowRight: [10, 0], ArrowUp: [0, -10], ArrowDown: [0, 10]}
    const offset = offsets[event.key]
    if (!offset) { return }
    event.preventDefault()
    move(locationRef.current[0] + offset[0], locationRef.current[1] + offset[1])
    setPosition(locationRef.current)
  }

  return (
    <Paper
      ref={paper}
      elevation={elevation}
      square={square}
      variant={variant}
      sx={[{
        position: "fixed", left: location[0], top: location[1], zIndex: "modal",
        width: "max-content", maxWidth: "100vw", maxHeight: "100vh",
        display: "flex", flexDirection: "column", overflow: "auto",
      }, sx || {}]}
    >
      <Box
        aria-label="Drag floating panel"
        onPointerDown={startDrag}
        onPointerMove={onPointerMove}
        onPointerUp={endDrag}
        onPointerCancel={endDrag}
        onKeyDown={onKeyDown}
        role="button"
        tabIndex={0}
        sx={{display: "flex", justifyContent: "center", cursor: "grab", touchAction: "none", userSelect: "none"}}
      >
        <DragIndicator fontSize="small" sx={{pointerEvents: "none"}} />
      </Box>
      <Box sx={{display: "flex", flexDirection: "column", p: 1}}>{objects}</Box>
    </Paper>
  )
}
