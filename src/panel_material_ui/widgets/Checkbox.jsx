import Checkbox from "@mui/material/Checkbox"
import FormControlLabel from "@mui/material/FormControlLabel"
import {MUI_SIZE, denseLabelSx, denseSx} from "./utils"
import {render_description} from "./description"
import {render_icon_text} from "./utils"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [indeterminate] = model.useState("indeterminate")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [checked, setChecked] = model.useState("value")
  const checkboxSx = denseSx(size, sx)

  const ref = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  return (
    <FormControlLabel
      control={
        <Checkbox
          color={color}
          checked={checked}
          disabled={disabled}
          indeterminate={indeterminate}
          slotProps={{input: {ref}}}
          size={MUI_SIZE(size)}
          onChange={(event) => setChecked(event.target.checked)}
          sx={checkboxSx}
        />
      }
      sx={denseLabelSx(size)}
      label={model.description ? <>{render_icon_text(label)}{render_description({model, el, view})}</> : render_icon_text(label)}
    />
  )
}
