import Badge from "@mui/material/Badge"

const PLACEMENT_TO_ANCHOR = {
  "top-right": {vertical: "top", horizontal: "right"},
  "top-left": {vertical: "top", horizontal: "left"},
  "bottom-right": {vertical: "bottom", horizontal: "right"},
  "bottom-left": {vertical: "bottom", horizontal: "left"},
}

export function render({model, view}) {
  const [placement] = model.useState("placement")
  const [badgeContent] = model.useState("content")
  const [color] = model.useState("color")
  const [max] = model.useState("max")
  const [offset] = model.useState("offset")
  const [overlap] = model.useState("overlap")
  const [showZero] = model.useState("show_zero")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const object = model.get_child("object")

  // Zero out child margin so the badge sits tightly on the child's visual edge
  React.useEffect(() => {
    if (model.object) {
      const childView = view.get_child_view(model.object)
      if (childView) {
        childView.parent_style.append(":host", {margin: "0px"})
      }
    }
  }, [object])

  // Fill the available space along whichever axes the wrapped child is
  // responsively sized, otherwise hug its intrinsic size (the default for a
  // badge anchored to an icon/avatar/button).
  const sizing = (view.model.data.object || {}).sizing_mode || ""

  // Position the badge as an (x, y) pixel offset from its anchor point
  // on the object. Raw translate: +x shifts right, +y shifts down.
  // Fill the host (sized by the wrapper's own sizing_mode); a content-sized
  // host hugs the child, a stretched host stretches it.
  const mergedSx = React.useMemo(() => {
    const [ox, oy] = offset ?? [0, -4]
    const fill = {
      ...(sizing.includes("width") || sizing.includes("both") ? {width: "100%"} : {}),
      ...(sizing.includes("height") || sizing.includes("both") ? {height: "100%"} : {}),
    }
    return {
      "& .MuiBadge-badge": {transform: `scale(1) translate(${ox}px, ${oy}px)`},
      width: "100%",
      height: "100%",
      ...sx,
    }
  }, [offset, sx, sizing])

  const anchorOrigin = PLACEMENT_TO_ANCHOR[placement]

  return (
    <Badge
      anchorOrigin={anchorOrigin}
      badgeContent={badgeContent}
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
