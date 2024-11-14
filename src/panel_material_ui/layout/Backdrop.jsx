import Backdrop from "@mui/material/Backdrop";

export function render({model}) {
  const [open] = model.useState("open");
  const objects = model.get_child("objects");

  return (
    <Backdrop open={open}>
      {objects}
    </Backdrop>
  );
}
