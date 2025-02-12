import Dialog from "@mui/material/Dialog";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";

export function render({model, view}) {
  const [full_screen] = model.useState("full_screen");
  const [open] = model.useState("open");
  const [title] = model.useState("title");
  const objects = model.get_child("objects");

  return (
    <Dialog open={open} fullScreen={full_screen} container={view.container}>
      <DialogTitle>
        {title}
      </DialogTitle>
      <DialogContent>
        {objects}
      </DialogContent>
    </Dialog>
  );
}
