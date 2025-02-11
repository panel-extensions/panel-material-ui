import Box from "@mui/material/Box"
import TextField from "@mui/material/TextField";

export function render({model}) {
  const [value, setValue] = React.useState(model.value);
  const [color] = model.useState("color");
  const [disabled] = model.useState("disabled");
  const [format] = model.useState("format");
  const [label] = model.useState("label");
  const [step] = model.useState("step");
  const [min] = model.useState("start");
  const [max] = model.useState("end");
  const [variant] = model.useState("variant");

  const handleChange = (event) => {
    const newValue = event.target.value === "" ? null : Number(event.target.value);
    setValue(newValue)
  };

  const [value_label, setValueLabel] = React.useState()

  React.useEffect(() => {
    setValueLabel(format ? format.doFormat([value])[0] : value)
  }, [format, value])

  return (
    <TextField
      type="number"
      color={color}
      disabled={disabled}
      label={label}
      sx={{width: "100%"}}
      value={value}
      variant={variant}
      inputProps={{step, min, max}}
      onChange={handleChange}
    />
  );
}
