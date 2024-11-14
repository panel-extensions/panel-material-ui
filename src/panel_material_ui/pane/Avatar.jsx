import Avatar from "@mui/material/Avatar";

export function render({model}) {
  const [alt_text] = model.useState("alt_text");
  const [color] = model.useState("color");
  const [object] = model.useState("object");
  const [size] = model.useState("size");
  const [variant] = model.useState("variant");

  return (
    <Avatar
      alt={alt_text}
      sx={{bgColor: color}}
      size={size}
      src={object}
      variant={variant}
      onClick={(e) => model.send_event("click", e)}
    />
  );
}