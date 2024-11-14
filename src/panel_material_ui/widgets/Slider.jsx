import Box from "@mui/material/Box"
import Slider from "@mui/material/Slider"
import Typography from "@mui/material/Typography"

export function render({model}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [end] = model.useState("end")
  const [label] = model.useState("label")
  const [orientation] = model.useState("orientation")
  const [start] = model.useState("start")
  const [step] = model.useState("step")
  const [tooltips] = model.useState("tooltips")
  const [track] = model.useState("track")
  const [value, setValue] = model.useState("value")

  return (
    <Box>
      <Typography variant="body1">
        {label && `${label}: `}
        <strong>
          {Array.isArray(value) ? `${value[0]} .. ${value[1]}` : value }
        </strong>
      </Typography>
      <Slider
        value={value}
        min={start}
        max={end}
        step={step}
        disabled={disabled}
        color={color}
        track={track}
        orientation={orientation}
        valueLabelDisplay={tooltips ? "auto" : "off"}
        onChange={(event, newValue) => setValue(newValue)}
      />
    </Box>
  )
}
