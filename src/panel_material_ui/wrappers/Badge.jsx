import Badge from "@mui/material/Badge"
import {render_icon_text} from "./utils"

const PLACEMENT_TO_ANCHOR = {
  "top-right": {vertical: "top", horizontal: "right"},
  "top-left": {vertical: "top", horizontal: "left"},
  "bottom-right": {vertical: "bottom", horizontal: "right"},
  "bottom-left": {vertical: "bottom", horizontal: "left"},
}

export function render({model, host}) {
  const [placement] = model.useState("placement")
  const [badgeContent] = model.useState("content")
  const [color] = model.useState("color")
  const [max] = model.useState("max")
  const [offset] = model.useState("offset")
  const [overlap] = model.useState("overlap")
  const [showZero] = model.useState("show_zero")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  // Zero out child margin so the badge sits tightly on the child's visual edge
  const object = model.render_children("object", {style: {margin: "0px"}})

  // Position the badge as an (x, y) pixel offset from its anchor point on the
  // object (raw translate: +x shifts right, +y shifts down), and fill the host
  // (sized by the wrapper's own sizing_mode) so a stretched child stretches
  // while a fixed one hugs.
  const mergedSx = React.useMemo(() => {
    const [ox, oy] = offset ?? [0, -4]
    return {
      "& .MuiBadge-badge": {transform: `scale(1) translate(${ox}px, ${oy}px)`},
      width: "100%",
      height: "100%",
      ...sx,
    }
  }, [offset, sx])

  const anchorOrigin = PLACEMENT_TO_ANCHOR[placement]

  return (
    <Badge
      anchorOrigin={anchorOrigin}
      badgeContent={render_icon_text(badgeContent)}
      color={color}
      max={max}
      overlap={overlap}
      showZero={showZero}
      sx={mergedSx}
      variant={variant}
    >
      {object || null }
    </Badge>
  )
}
