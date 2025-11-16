import {MuiColorInput} from "mui-color-input"
import {render_description} from "./description"

export function render({model, el, view}) {
  const [alpha] = model.useState("alpha")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [format] = model.useState("format")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const [value, setValue] = model.useState("value")

  return (
    <MuiColorInput
      color={color}
      disabled={disabled}
      format={alpha && format === "hex" ? "hex8" : format}
      fullWidth
      isAlphaHidden={!alpha}
      label={model.description ? <>{label}{render_description({model, el, view})}</> : label}
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
