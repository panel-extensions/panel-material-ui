import {MuiColorInput} from "mui-color-input"
import {render_description} from "./description"
import {render_icon_text} from "./utils"

export function render({model, el, view}) {
  const [alpha] = model.useState("alpha")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [format] = model.useState("format")
  const [helper_text] = model.useState("helper_text")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const [value, setValue] = model.useState("value")

  return (
    <MuiColorInput
      color={color}
      disabled={disabled}
      error={error_state}
      format={alpha && format === "hex" ? "hex8" : format}
      fullWidth
      helperText={helper_text || undefined}
      isAlphaHidden={!alpha}
      label={model.description ? <>{render_icon_text(label)}{render_description({model, el, view})}</> : render_icon_text(label)}
      onChange={setValue}
      size={size}
      sx={sx}
      value={value || ""}
      variant={variant}
      PopoverProps={{
        container: el,
      }}
    />
  )
}
