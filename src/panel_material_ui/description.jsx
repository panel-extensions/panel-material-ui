import React from "react"
import InfoIcon from "@mui/icons-material/Info"
import Tooltip from "@mui/material/Tooltip"

export function render_description({model, el}) {
  const [description] =  model.useState("description")

  return (
    <Tooltip
      title={description}
      arrow
      placement="right"
      slotProps={{popper: {container: el}}}
    >
      <InfoIcon sx={{fontSize: "1.1em"}}/>
    </Tooltip>
  )
}
