import Switch from "@mui/material/Switch"
import FormControlLabel from "@mui/material/FormControlLabel"
import {render_description} from "./description"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [checked, setChecked] = model.useState("value")
  const [disabled] = model.useState("disabled")
  const [edge] = model.useState("edge")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")

  return (
    <FormControlLabel
      control={
        <Switch
          color={color}
          checked={checked}
          disabled={disabled}
          edge={edge}
          onChange={(event) => setChecked(event.target.checked)}
          size={size}
          sx={sx}
        />
      }
      label={model.description ? <>{label}{render_description({model, el, view})}</> : label}
      sx={{mr: 0}}
    />
  )
}
