import Switch from "@mui/material/Switch"
import FormControlLabel from "@mui/material/FormControlLabel"
import {render_description} from "./description"
import {MUI_SIZE, denseLabelSx, denseSx, render_icon_text} from "./utils"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [checked, setChecked] = model.useState("value")
  const [disabled] = model.useState("disabled")
  const [edge] = model.useState("edge")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")

  const ref = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  return (
    <FormControlLabel
      control={
        <Switch
          color={color}
          checked={checked}
          disabled={disabled}
          edge={edge}
          onChange={(event) => setChecked(event.target.checked)}
          size={MUI_SIZE(size)}
          sx={[{m: 0}, denseSx(size), sx]}
          slotProps={{
            input: {
              ref
            }
          }}
        />
      }
      label={model.description ? <>{render_icon_text(label)}{render_description({model, el, view})}</> : render_icon_text(label)}
      sx={[denseLabelSx(size, "switch"), {mr: 0}]}
    />
  );
}
