import { MuiColorInput } from 'mui-color-input'

export function render({model, el}) {
  const [value, setValue] = model.useState("value")
  const [alpha] = model.useState("alpha")
  const [format] = model.useState("format")
  const [variant] = model.useState("variant")
  const [size] = model.useState("size")
  const [disabled] = model.useState("disabled")
  const [color] = model.useState("color")
  return (
    <MuiColorInput
      disabled={disabled}
      color={color}
      format={format}
      value={value}
      onChange={setValue}
      isAlphaHidden={!alpha}
      variant={variant}
      size={size}
      PopoverProps={{
        container: el,
      }}
    />
  )
}
