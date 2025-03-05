import Box from "@mui/material/Box"
import TextField from "@mui/material/TextField";

export function render({model}) {
  const [color] = model.useState("color");
  const [disabled] = model.useState("disabled");
  const [format] = model.useState("format");
  const [label] = model.useState("label");
  const [placeholder] = model.useState("placeholder")
  const [step] = model.useState("step");
  const [min] = model.useState("start");
  const [max] = model.useState("end");
  const [size] = model.useState("size");
  const [variant] = model.useState("variant");
  const [sx] = model.useState("sx");
  const [value, setValue] = model.useState("value");

  const handleChange = (event) => {
    const newValue = event.target.value === "" ? null : Number(event.target.value);
    setValue(newValue)
  };

  const [_, setValueLabel] = React.useState()

  React.useEffect(() => {
    setValueLabel(format ? format.doFormat([value])[0] : value)
  }, [format, value])

  return (
    <TextField
      type="number"
      color={color}
      disabled={disabled}
      label={label}
      placeholder={placeholder}
      size={size}
      value={value}
      variant={variant}
      inputProps={{step, min, max}}
      sx={{
        width: "100%",
        ...sx
      }}
      onChange={handleChange}
    />
  );
}
