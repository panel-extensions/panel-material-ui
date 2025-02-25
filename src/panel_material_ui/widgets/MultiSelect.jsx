import InputLabel from "@mui/material/InputLabel";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import OutlinedInput from "@mui/material/OutlinedInput";
import FilledInput from "@mui/material/FilledInput";
import Input from "@mui/material/Input";

export function render({model, view}) {
  const [color] = model.useState("color");
  const [disabled] = model.useState("disabled");
  const [label] = model.useState("label");
  const [max_items] = model.useState("max_items");
  const [options] = model.useState("options");
  const [value, setValue] = model.useState("value");
  const [variant] = model.useState("variant");
  const [sx] = model.useState("sx");
  const handleChange = (event) => {
    const {options} = event.target;
    const newSelections = [];
    for (let i = 0, l = options.length; i < l; i += 1) {
      if (options[i].selected) {
        newSelections.push(options[i].value);
      }
    }
    if (!max_items) {
      setValue(newSelections);
      return;
    }

    // Find the newly added item (if any) by comparing with previous value
    const added = newSelections.find(item => !value.includes(item));

    if (added) {
      // If we're adding a new item
      const newValue = [...value, added];
      if (max_items && newValue.length > max_items) {
        // Remove the oldest item (first in array)
        newValue.shift();
      }
      setValue(newValue);
    } else {
      // If we're removing items, just set the new selections
      setValue(newSelections);
    }
  };

  const inputId = `select-multiple-native-${model.id}`;
  return (
    <FormControl sx={{m: 1, width: 300}}>
      <InputLabel id={`select-multiple-label-${model.id}`} shrink htmlFor={inputId}>
        {label}
      </InputLabel>
      <Select
        multiple
        native
        color={color}
        disabled={disabled}
        value={value}
        onChange={handleChange}
        labelId={`select-multiple-label-${model.id}`}
        input={variant === "outlined" ?
          <OutlinedInput id={inputId}/> :
          variant === "filled" ?
            <FilledInput id={inputId}/> :
            <Input id={inputId}/>
        }
        sx={sx}
        variant={variant}
      >
        {options.map((name) => (
          <option
            key={name}
            value={name}
          >
            {name}
          </option>
        ))}
      </Select>
    </FormControl>
  );
}
