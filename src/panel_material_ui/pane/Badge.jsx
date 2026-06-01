import Badge from "@mui/material/Badge"
import Box from "@mui/material/Box"

const BADGE_SX = {
  "& .MuiBadge-badge": {
    transform: "scale(1) translate(0px, -4px)",
  },
}

export function render({model, view}) {
  const [anchorOrigin] = model.useState("anchor_origin")
  const [badgeContent] = model.useState("badge_content")
  const [color] = model.useState("color")
  const [max] = model.useState("max")
  const [overlap] = model.useState("overlap")
  const [showZero] = model.useState("show_zero")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const object = model.get_child("object")
  const [visible, setVisible] = React.useState(view.model.visible)
  React.useEffect(() => {
    const cb = () => setVisible(view.model.visible)
    view.model.properties.visible.change.connect(cb)
    return () => view.model.properties.visible.change.disconnect(cb)
  }, [])

  // Zero out child margin so the badge sits tightly on the child's visual edge
  React.useEffect(() => {
    if (model.object) {
      const childView = view.get_child_view(model.object)
      if (childView) {
        childView.parent_style.append(":host", {margin: "0px"})
      }
    }
  }, [object])

  const mergedSx = React.useMemo(() => ({...BADGE_SX, ...sx}), [sx])

  return (
    <Badge
      anchorOrigin={anchorOrigin ?? undefined}
      badgeContent={badgeContent}
      color={color}
      invisible={!visible}
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
