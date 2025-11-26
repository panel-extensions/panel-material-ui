import Checkbox from "@mui/material/Checkbox"
import Radio from "@mui/material/Radio"
import RadioGroup from "@mui/material/RadioGroup"
import FormControlLabel from "@mui/material/FormControlLabel"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import {render_description} from "./description"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [inline] = model.useState("inline")
  const [label] = model.useState("label")
  const [label_placement] = model.useState("label_placement")
  const [options] = model.useState("options")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const exclusive = model.esm_constants.exclusive

  const ref = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  const RadioButton = exclusive ? Radio : Checkbox

  return (
    <FormControl component="fieldset" disabled={disabled} fullWidth>
      {label && <FormLabel id="radio-group-label">{label}{model.description ? render_description({model, el, view}) : null}</FormLabel>}
      <RadioGroup
        aria-labelledby="radio-group-label"
        fullWidth
        ref={ref}
        row={inline}
        sx={sx}
        value={value}
      >
        {options.map((option, index) => {
          return (
            <FormControlLabel
              key={option}
              value={option}
              label={option}
              labelPlacement={label_placement}
              control={
                <RadioButton
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
