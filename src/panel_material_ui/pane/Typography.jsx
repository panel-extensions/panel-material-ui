import {Typography} from "@mui/material"

function html_decode(input) {
  const doc = new DOMParser().parseFromString(input, "text/html")
  return doc.documentElement.textContent
}

export function render({model}) {
  const [sx] = model.useState("sx")
  const [text] = model.useState("object")
  const [variant] = model.useState("variant")

  return (
    <Typography
      sx={{...sx, "& p": {marginBlockStart: "0.25em", marginBlockEnd: "0.25em"}}}
      dangerouslySetInnerHTML={{__html: html_decode(text)}}
      variant={variant}
    />
  )
}
