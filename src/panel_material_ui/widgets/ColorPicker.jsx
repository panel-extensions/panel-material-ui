import { MuiColorInput } from 'mui-color-input'

export function render({model, el}) {
  const [alpha] = model.useState("alpha")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [format] = model.useState("format")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [value, setValue] = model.useState("value")

  return (
    <MuiColorInput
      color={color}
      disabled={disabled}
      format={format}
      isAlphaHidden={!alpha}
      onChange={setValue}
      size={size}
      value={value}
      variant={variant}
      PopoverProps={{
        container: el,
      }}
    />
  )
}
