import Dialog from "@mui/material/Modal";
import Paper from "@mui/material/Paper";

export function render({model}) {
  const [open] = model.useState("open");
  const objects = model.get_child("objects");

  return (
    <Dialog open={open}>
      <Paper>
        {objects}
      </Paper>
    </Dialog>
  );
}
