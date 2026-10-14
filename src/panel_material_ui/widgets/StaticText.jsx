import * as React from "react"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import Typography from "@mui/material/Typography"
import {render_description} from "../description"
import {render_icon_text} from "../utils"

export function render({model, el, view}) {
  const [disabled] = model.useState("disabled")
  const [label] = model.useState("label")
  const [sx] = model.useState("sx")
  const [value] = model.useState("value")

  return (
    <FormControl disabled={disabled} fullWidth sx={sx}>
      {label && (
        <FormLabel sx={{fontSize: "0.75rem"}}>
          {render_icon_text(label)}
          {model.description ? render_description({model, el, view}) : null}
        </FormLabel>
      )}
      <Typography
        color={disabled ? "text.disabled" : "text.primary"}
        component="div"
        dangerouslySetInnerHTML={{__html: value}}
        variant="body1"
      />
    </FormControl>
  )
}
