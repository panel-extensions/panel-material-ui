import Alert from "@mui/material/Alert"
import AlertTitle from "@mui/material/AlertTitle"
import Collapse from "@mui/material/Collapse"

function html_decode(input) {
  const doc = new DOMParser().parseFromString(input, "text/html")
  return doc.documentElement.textContent
}

export function render({model}) {
  const [closed, setClosed] = model.useState("closed")
  const [closeable] = model.useState("closeable")
  const [severity] = model.useState("severity")
  const [title] = model.useState("title")
  const [object] = model.useState("object")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const objects = model.get_child("objects")

  const props = {}
  if (closeable) {
    props.onClose = () => { setClosed(true) }
  }

  const defaultSx = {
    "& .MuiAlert-icon": {paddingBottom: 0},
    "& .MuiAlert-message": {paddingBottom: 0},
    "& .MuiAlert-action": {paddingBottom: 0},
  }
  const mergedSx = {...defaultSx, ...sx}

  return (
    <Collapse in={!closed}>
      <Alert severity={severity} variant={variant} {...props} sx={mergedSx}>
        <AlertTitle>{title}</AlertTitle>
        <span dangerouslySetInnerHTML={{__html: html_decode(object)}} />
        {objects}
      </Alert>
    </Collapse>
  );
}
