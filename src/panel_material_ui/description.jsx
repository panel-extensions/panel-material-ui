import React from "react"
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined"
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
      <InfoOutlinedIcon sx={{fontSize: "1.1em"}}/>
    </Tooltip>
  )
}
