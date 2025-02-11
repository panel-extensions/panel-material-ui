import Box from "@mui/material/Box"
import Slider from "@mui/material/Slider"
import Typography from "@mui/material/Typography"

export function render({model}) {
  const [bar_color] = model.useState("bar_color")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [end] = model.useState("end")
  const [format] = model.useState("format")
  const [label] = model.useState("label")
  const [orientation] = model.useState("orientation")
  const [show_value] = model.useState("show_value")
  const [start] = model.useState("start")
  const [step] = model.useState("step")
  const [tooltips] = model.useState("tooltips")
  const [track] = model.useState("track")
  const [value, setValue] = model.useState("value")
  const [value_throttled, setValueThrottled] = model.useState("value_throttled")

  const [value_label, setValueLabel] = React.useState()

  React.useEffect(() => {
    if (Array.isArray(value)) {
      let [v1, v2] = value
      if (format) {
        [v1, v2] = format.doFormat([v1, v2])
      }
      setValueLabel(`${v1} .. ${v2}`)
    } else {
      setValueLabel(format ? format.doFormat([value])[0] : value)
    }
  }, [format, value])

  return (
    <Box sx={{height: "100%"}}>
      <Typography variant="body1">
        {label && `${label}: `}
        { show_value &&
          <strong>
            {value_label}
          </strong>
        }
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
        onChangeCommitted={(event, newValue) => setValueThrottled(newValue)}
        sx={{
          "& .MuiSlider-track": {
            backgroundColor: bar_color,
            borderColor: bar_color
          },
          "& .MuiSlider-rail": {
            backgroundColor: bar_color,
          },
        }}
      />
    </Box>
  )
}
