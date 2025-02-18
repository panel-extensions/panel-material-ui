import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import ListSubheader from "@mui/material/ListSubheader";

export function render({model, el}) {
  const [value, setValue] = model.useState("value");
  const [options] = model.useState("options");
  const [color] = model.useState("color");
  const [label] = model.useState("label");
  const [variant] = model.useState("variant");
  const [disabled] = model.useState("disabled");
  const [disabled_options] = model.useState("disabled_options");

  let option_list;
  if (Array.isArray(options)) {
    option_list = options.map((opt, index) => (
      <MenuItem
        key={index}
        value={Array.isArray(opt) ? opt[1]: opt}
        disabled={disabled_options?.includes(opt)}
      >
        {Array.isArray(opt) ? opt[0]: opt}
      </MenuItem>
    ));
  } else if (typeof options === "object" && options !== null) {
    option_list = Object.entries(options).map(([groupLabel, groupOptions]) => (
      // Use a fragment to group the ListSubheader and its MenuItems.
      <React.Fragment key={groupLabel}>
        <ListSubheader>{groupLabel}</ListSubheader>
        {groupOptions.map((option, idx) => (
          <MenuItem
            key={`${groupLabel}-${idx}`}
            value={Array.isArray(option) ? option[1] : option}
            disabled={disabled_options?.includes(option)}
          >
            {Array.isArray(option) ? option[0]: option}
          </MenuItem>
        ))}
      </React.Fragment>
    ));
  }
  return (
    <FormControl fullWidth disabled={disabled}>
      {label && <InputLabel>{label}</InputLabel>}
      <Select
        MenuProps={{
          container: el,
        }}
        color={color}
        disabled={disabled}
        value={value}
        label={label}
        variant={variant}
        onChange={(event) => { setValue(event.target.value) }}
      >
        {option_list}
      </Select>
    </FormControl>
  );
}
