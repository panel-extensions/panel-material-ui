import Paper from "@mui/material/Paper";

export function render({model}) {
  const [elevation] = model.useState("elevation");
  const objects = model.get_child("objects")
  return (
    <Paper elevation={elevation}>
      {objects}
    </Paper>
  );
}
