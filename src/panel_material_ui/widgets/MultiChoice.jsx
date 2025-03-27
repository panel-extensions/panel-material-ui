import Box from "@mui/material/Box"
import InputLabel from "@mui/material/InputLabel"
import MenuItem from "@mui/material/MenuItem"
import FormControl from "@mui/material/FormControl"
import Select from "@mui/material/Select"
import Chip from "@mui/material/Chip"
import OutlinedInput from "@mui/material/OutlinedInput"
import FilledInput from "@mui/material/FilledInput"
import Input from "@mui/material/Input"

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;

const MenuProps = {
  disablePortal: true, // Ensures menu doesn't render outside of shadow DOM
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
    },
  },
};

export function render({model}) {
  const [color] = model.useState("color");
  const [delete_button] = model.useState("delete_button");
  const [disabled] = model.useState("disabled");
  const [label] = model.useState("label");
  const [max_items] = model.useState("max_items");
  const [option_limit] = model.useState("option_limit");
  const [options] = model.useState("options");
  const [placeholder] = model.useState("placeholder");
  const [search_option_limit] = model.useState("search_option_limit");
  const [solid] = model.useState("solid");
  const [value, setValue] = model.useState("value");
  const [variant] = model.useState("variant");
  const [sx] = model.useState("sx");
  const handleChange = (event) => {
    const new_value = event.target.value;
    // On autofill we get a stringified value.
    const values = typeof new_value === "string" ? new_value.split(",") : new_value
    if (values && max_items && (values.length > max_items)) {
      return
    }
    setValue(values)
  };

  return (
    <FormControl sx={{width: "100%"}}>
      <InputLabel id={`chip-label-${model.id}`}>{label}</InputLabel>
      <Select
        fullWidth
        multiple
        color={color}
        disabled={disabled}
        input={variant === "outlined" ?
          <OutlinedInput id="select-multiple-chip" label={label}/> :
          variant === "filled" ?
            <FilledInput id="select-multiple-chip" label={label}/> :
            <Input id="select-multiple-chip" label={label}/>
        }
        labelId={`chip-label-${model.id}`}
        onChange={handleChange}
        sx={sx}
        variant={variant}
        renderValue={(selected) => (
          <Box sx={{display: "flex", flexWrap: "wrap", gap: 0.5}}>
            {selected.map((selected_value) => (
              <Chip
                color={color}
                variant={solid ? "filled" : "outlined"}
                key={selected_value}
                label={selected_value}
                onMouseDown={(event) => event.stopPropagation()}
                onDelete={delete_button ? (event) => {
                  setValue(value.filter(v => v !== selected_value));
                } : undefined}
              />
            ))}
          </Box>
        )}
        value={value}
        MenuProps={MenuProps}
      >
        {options.map((name) => (
          <MenuItem
            key={name}
            value={name}
          >
            {name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
