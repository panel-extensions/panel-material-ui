import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";

export function render({model}) {
  const [disabled] = model.useState("disabled");
  const [value, setValue] = model.useState("value");
  const [options] = model.useState("options");
  const [label] = model.useState("label");
  const [orientation] = model.useState("orientation");
  const [sx] = model.useState("sx");

  return (
    <FormControl component="fieldset" disabled={disabled} fullWidth>
      {label && <FormLabel id="radio-buttons-group-label">{label}</FormLabel>}
      <RadioGroup
        aria-labelledby="radio-buttons-group-label"
        row={orientation === "horizontal" ? true : false}
        value={value}
      >
        {options.map((option, index) => (
          <FormControlLabel
            key={option}
            value={option}
            label={option}
            control={<Radio onChange={(e) => setValue("option")}/>}
            sx={sx}
          />
        ))}
      </RadioGroup>
    </FormControl>
  );
}
