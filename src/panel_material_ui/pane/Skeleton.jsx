import Skeleton from "@mui/material/Skeleton";

export function render({model}) {
  const [variant] = model.useState("variant");
  return (
    <Skeleton variant={variant} width={model.width} height={model.height}/>
  );
}
