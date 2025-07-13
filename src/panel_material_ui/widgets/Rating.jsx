import Rating from "@mui/material/Rating";

export function render({model}) {
  const [value, setValue] = model.useState("value");
  const [end] = model.useState("end");
  const [only_selected] = model.useState("only_selected");
  const [size] = model.useState("size");
  const [sx] = model.useState("sx");
  const [precision] = model.useState("precision");
  const [disabled] = model.useState("disabled")
  const [readonly] = model.useState("readonly")
  return (
    <Rating
      highlightSelectedOnly={only_selected}
      max={end}
      value={value}
      precision={precision}
      size={size}
      onChange={(event, newValue) => setValue(newValue)}
      disabled={disabled}
      readOnly={readonly}
      sx={sx}
    />
  );
}
