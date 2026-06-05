import Tooltip from "@mui/material/Tooltip"
import Box from "@mui/material/Box"

export function render({model, view}) {
  const [arrow] = model.useState("arrow")
  const [describeChild] = model.useState("describe_child")
  const [enterDelay] = model.useState("enter_delay")
  const [followCursor] = model.useState("follow_cursor")
  const [leaveDelay] = model.useState("leave_delay")
  const [open] = model.useState("open")
  const [placement] = model.useState("placement")
  const [sx] = model.useState("sx")
  const [title] = model.useState("title")
  const object = model.get_child("object")

  // Fill the available space along whichever axes the wrapped child is
  // responsively sized, otherwise hug its intrinsic size.
  const sizing = (view.model.data.object || {}).sizing_mode || ""
  const fill = {
    ...(sizing.includes("width") || sizing.includes("both") ? {width: "100%"} : {}),
    ...(sizing.includes("height") || sizing.includes("both") ? {height: "100%"} : {}),
  }

  const openProps = open === null ? {} : {open}

  // Fill the host (sized by the wrapper's own sizing_mode); a content-sized
  // host hugs the child, a stretched host stretches it.
  return (
    <Tooltip
      arrow={arrow}
      describeChild={describeChild}
      enterDelay={enterDelay}
      followCursor={followCursor}
      leaveDelay={leaveDelay}
      placement={placement}
      sx={sx}
      title={title}
      {...openProps}
    >
      <Box sx={{display: "inline-flex", width: "100%", height: "100%"}}>
        {object}
      </Box>
    </Tooltip>
  )
}
