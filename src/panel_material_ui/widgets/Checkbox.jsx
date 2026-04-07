import Checkbox from "@mui/material/Checkbox"
import FormControlLabel from "@mui/material/FormControlLabel"
import {render_description} from "./description"
import {render_icon_text} from "./utils"

const CHECKBOX_BASE_SX = {p: "6px"}

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [indeterminate] = model.useState("indeterminate")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [checked, setChecked] = model.useState("value")
  const checkboxSx = React.useMemo(() => (sx ? [CHECKBOX_BASE_SX, sx] : CHECKBOX_BASE_SX), [sx])

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
          inputRef={ref}
          size={size}
          onChange={(event) => setChecked(event.target.checked)}
          sx={checkboxSx}
        />
      }
      label={model.description ? <>{render_icon_text(label)}{render_description({model, el, view})}</> : render_icon_text(label)}
    />
  )
}
