import LinearProgress from "@mui/material/LinearProgress";

export function render({model}) {
  const [color] = model.useState("color")
  const [sx] = model.useState("sx")
  const [value] = model.useState("value")
  const [variant] = model.useState("variant")
  const [valueBuffer] = model.useState("value_buffer")

  return (
    <LinearProgress color={color} variant={variant} value={value} valueBuffer={valueBuffer} sx={sx} />
  )
}
