import LinearProgress from "@mui/material/LinearProgress";

export function render({model}) {
  const [color] = model.useState("color")
  const [max] = model.useState("max")
  const [sx] = model.useState("sx")
  const [value] = model.useState("value")
  const [variant] = model.useState("variant")
  const [valueBuffer] = model.useState("value_buffer")

  return (
    <LinearProgress color={color} variant={variant} value={value < 0 ? 0 : Math.min(value / max * 100, 100)} valueBuffer={valueBuffer < 0 ? 0 : Math.min(valueBuffer / max * 100, 100)} sx={sx} />
  )
}
