import Rating from "@mui/material/Rating";

export function render({model}) {
  const [value, setValue] = model.useState("value");
  const [end] = model.useState("end");
  const [only_selected] = model.useState("only_selected");
  const [size] = model.useState("size");
  const [sx] = model.useState("sx");
  return (
    <Rating
      highlightSelectedOnly={only_selected}
      max={end}
      value={value}
      size={size}
      onChange={(event, newValue) => setValue(newValue)}
      sx={sx}
    />
  );
}
