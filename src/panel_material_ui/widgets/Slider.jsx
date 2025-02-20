import Box from "@mui/material/Box"
import Slider from "@mui/material/Slider"
import Typography from "@mui/material/Typography"
import dayjs from "dayjs";

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
  const [sx] = model.useState("sx")
  const [ticks] = model.useState("ticks")
  const [tooltips] = model.useState("tooltips")
  const [track] = model.useState("track")
  const [value, setValue] = model.useState("value")
  const [_, setValueThrottled] = model.useState("value_throttled")
  const [value_label, setValueLabel] = React.useState()
  const date = model.esm_constants.date
  const datetime = model.esm_constants.datetime

  function format_value(d) {
    if (datetime) {
      return dayjs.unix(d / 1000).format(format || "YYYY-MM-DD HH:mm:ss");
    } else if (date) {
      return dayjs.unix(d / 1000).format(format || "YYYY-MM-DD");
    } else if (format) {
      return format.doFormat([d])[0]
    } else {
      return d
    }
  }

  React.useEffect(() => {
    if (Array.isArray(value)) {
      let [v1, v2] = value;
      [v1, v2] = [format_value(v1), format_value(v2)];
      setValueLabel(`${v1} .. ${v2}`)
    } else {
      setValueLabel(format_value(value))
    }
  }, [format, value])

  const marks = React.useMemo(() => {
    if (!ticks) {
      return undefined
    }
    return ticks.map(tick => ({
      value: tick,
      label: format_value(tick)
    }))
  }, [ticks, format, date])

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
        getAriaLabel={() => label}
        getAriaValueText={format_value}
        step={date ? step*86400000 : (datetime ? step*1000 : step)}
        marks={marks}
        disabled={disabled}
        color={color}
        track={track}
        orientation={orientation}
        valueLabelDisplay={tooltips ? "auto" : "off"}
        onChange={(_, newValue) => setValue(newValue)}
        onChangeCommitted={(_, newValue) => setValueThrottled(newValue)}
        sx={{
          "& .MuiSlider-track": {
            backgroundColor: bar_color,
            borderColor: bar_color
          },
          "& .MuiSlider-rail": {
            backgroundColor: bar_color,
          },
          ...sx
        }}
        valueLabelFormat={format_value}
      />
    </Box>
  )
}
