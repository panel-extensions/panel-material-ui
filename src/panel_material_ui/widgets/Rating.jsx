import Rating from "@mui/material/Rating";

export function render({model}) {
  const [value, setValue] = model.useState("value");
  const [only_selected] = model.useState("only_selected");
  const [size] = model.useState("size");
  return (
    <Rating
      highlightSelectedOnly={only_selected}
      value={value}
      size={size}
      onChange={(event, newValue) => setValue(newValue)}
    />
  );
}
