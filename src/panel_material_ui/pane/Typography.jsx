import {Typography} from "@mui/material"

function html_decode(input) {
  const doc = new DOMParser().parseFromString(input, "text/html")
  return doc.documentElement.textContent
}

export function render({model}) {
  const [sx] = model.useState("sx")
  const [text] = model.useState("object")

  return <Typography sx={sx} dangerouslySetInnerHTML={{__html: html_decode(text)}}/>
}
