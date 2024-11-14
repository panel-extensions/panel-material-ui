import Modal from "@mui/material/Modal";
import Paper from "@mui/material/Paper";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
};

export function render({model}) {
  const [open] = model.useState("open");
  const objects = model.get_child("objects");

  return (
    <Modal open={open}>
      <Paper sx={style} elevation={4}>
        {objects}
      </Paper>
    </Modal>
  );
}
