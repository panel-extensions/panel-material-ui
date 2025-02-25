import Radio from "@mui/material/Radio"
import RadioGroup from "@mui/material/RadioGroup"
import FormControlLabel from "@mui/material/FormControlLabel"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"

export function render({model}) {
  const [disabled] = model.useState("disabled");
  const [color] = model.useState("color");
  const [options] = model.useState("options");
  const [label] = model.useState("label");
  const [inline] = model.useState("inline");
  const [value, setValue] = model.useState("value");
  const [sx] = model.useState("sx");
  const exclusive = model.esm_constants.exclusive
  return (
    <FormControl component="fieldset" disabled={disabled}>
      {label && <FormLabel id="radio-buttons-group-label">{label}</FormLabel>}
      <RadioGroup
        aria-labelledby="radio-buttons-group-label"
        value={value}
        row={inline}
        sx={sx}
      >
        {options.map((option, index) => {
          return (
            <FormControlLabel
              key={option}
              value={option}
              label={option}
              labelPlacement={inline ? "bottom" : "right"}
              control={
                <Radio
                  checked={exclusive ? (value==option) : value.includes(option)}
                  color={color}
                  onClick={(e) => {
                    let newValue
                    if (exclusive) {
                      newValue = option
                    } else if (value.includes(option)) {
                      newValue = value.filter((v) => v !== option)
                    } else {
                      newValue = [...value]
                      newValue.push(option)
                    }
                    setValue(newValue)
                  }}
                />
              }
            />
          )
        })}
      </RadioGroup>
    </FormControl>
  );
}
