import Checkbox from "@mui/material/Checkbox"
import FormControlLabel from "@mui/material/FormControlLabel"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [indeterminate] = model.useState("indeterminate")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [checked, setChecked] = model.useState("value")
  return (
    <FormControlLabel
      control={
        <Checkbox
          color={color}
          checked={checked}
          disabled={disabled}
          indeterminate={indeterminate}
          size={size}
          onChange={(event) => setChecked(event.target.checked)}
          sx={{p: "6px", ...sx}}
        />
      }
      label={label}
    />
  )
}
