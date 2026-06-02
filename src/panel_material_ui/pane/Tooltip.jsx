import Tooltip from "@mui/material/Tooltip"
import Box from "@mui/material/Box"

export function render({model}) {
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

  const openProps = open === null ? {} : {open}

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
      <Box sx={{display: "inline-flex"}}>
        {object}
      </Box>
    </Tooltip>
  )
}
