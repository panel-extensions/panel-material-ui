import Divider from "@mui/material/Divider";

export function render({model}) {
  const [orientation] = model.useState("orientation");
  const [variant] = model.useState("variant");
  const [sx] = model.useState("sx");
  const objects = model.get_child("objects");

  return (
    <Divider
      orientation={orientation}
      variant={variant}
      sx={sx}
    >
      {objects.length > 0 ? objects : null}
    </Divider>
  );
}
