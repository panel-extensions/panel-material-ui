import Alert from "@mui/material/Alert"
import AlertTitle from "@mui/material/AlertTitle"
import Collapse from "@mui/material/Collapse"

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

  return (
    <Collapse in={!closed}>
      <Alert severity={severity} variant={variant} {...props} sx={sx}>
        <AlertTitle>{title}</AlertTitle>
        {object}
        {objects}
      </Alert>
    </Collapse>
  );
}
