import LinearProgress from "@mui/material/LinearProgress";

export function render({model}) {
  const [value] = model.useState("value");
  const [variant] = model.useState("variant");
  const [color] = model.useState("color");
  return (
    <LinearProgress color={color} variant={variant} value={value} />
  );
}
