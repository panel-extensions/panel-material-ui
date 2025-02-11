import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

export function render({model, el}) {
  const [value, setValue] = model.useState("value");
  const [options] = model.useState("options");
  const [label] = model.useState("label");
  const [variant] = model.useState("variant");
  const [disabled] = model.useState("disabled");
  const [disabled_options] = model.useState("disabled_options");
  return (
    <FormControl fullWidth disabled={disabled}>
      {label && <InputLabel>{label}</InputLabel>}
      <Select
        MenuProps={{
          container: el,
        }}
        disabled={disabled}
        value={value}
        label={label}
        variant={variant}
        onChange={(event) => setValue(event.target.value)}
      >
        {options.map((option, index) => (
          <MenuItem
            key={index}
            value={option}
            disabled={disabled_options?.includes(option)}
          >
            {option}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
