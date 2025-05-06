import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import Slider from "@mui/material/Slider"
import dayjs from "dayjs"

export function render({model}) {
  const [bar_color] = model.useState("bar_color")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [direction] = model.useState("direction")
  const [format] = model.useState("format")
  const [label] = model.useState("label")
  const [marks] = model.useState("marks")
  const [orientation] = model.useState("orientation")
  const [show_value] = model.useState("show_value")
  const [size] = model.useState("size")
  const [step] = model.useState("step")
  const [sx] = model.useState("sx")
  const [tooltips] = model.useState("tooltips")
  const [track] = model.useState("track")
  const [value, setValue] = model.useState("value")
  const [valueLabel] = model.useState("value_label")
  const [_, setValueThrottled] = model.useState("value_throttled")
  const [value_label, setValueLabel] = React.useState()
  let [end] = model.useState("end")
  let [start] = model.useState("start")

  const date = model.esm_constants.date
  const datetime = model.esm_constants.datetime
  const discrete = model.esm_constants.discrete

  let labels = null
  if (discrete) {
    const [labels_state] = model.useState("options")
    labels = labels_state === undefined ? [] : labels_state
    start = 0
    end = labels.length - 1
  }

  function format_value(d, _, useLabel=true) {
    if (valueLabel && useLabel) {
      return valueLabel
    } else if (discrete) {
      return labels[d]
    } else if (datetime) {
      return dayjs.unix(d / 1000).format(format || "YYYY-MM-DD HH:mm:ss");
    } else if (date) {
      return dayjs.unix(d / 1000).format(format || "YYYY-MM-DD");
    } else if (format) {
      if (typeof format === "string") {
        const tickers = window.Bokeh.require("models/formatters")
        return new tickers.NumeralTickFormatter({format}).doFormat([d])[0]
      } else {
        return format.doFormat([d])[0]
      }
    } else {
      return d
    }
  }

  React.useEffect(() => {
    if (valueLabel) {
      setValueLabel(valueLabel)
    } else if (discrete) {
      setValueLabel(labels[value])
    } else if (Array.isArray(value)) {
      let [v1, v2] = value;
      [v1, v2] = [format_value(v1), format_value(v2)];
      setValueLabel(`${v1} .. ${v2}`)
    } else {
      setValueLabel(format_value(value))
    }
  }, [format, value, labels])

  const ticks = React.useMemo(() => {
    if (!marks) {
      return undefined
    } else if (typeof marks === "boolean") {
      return true
    } else if (Array.isArray(marks)) {
      return marks.map(tick => {
        if (typeof tick === "object" && tick !== null) {
          return tick
        }
        return {
          value: tick,
          label: format_value(tick, tick, false)
        }
      })
    }
  }, [marks, format, labels])

  return (
    <FormControl disabled={disabled} fullWidth sx={orientation === "vertical" ? {height: "100%"} : {}}>
      <FormLabel>
        {label && `${label}: `}
        { show_value &&
          <strong>
            {value_label}
          </strong>
        }
      </FormLabel>
      <Slider
        color={color}
        dir={direction}
        disabled={disabled}
        getAriaLabel={() => label}
        getAriaValueText={format_value}
        marks={ticks}
        max={end}
        min={start}
        orientation={orientation}
        onChange={(_, newValue) => setValue(newValue)}
        onChangeCommitted={(_, newValue) => setValueThrottled(newValue)}
        size={size}
        step={date ? step*86400000 : (datetime ? step*1000 : step)}
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
        track={track}
        value={value}
        valueLabelDisplay={tooltips === "auto" ? "auto" : tooltips ? "on" : "off"}
        valueLabelFormat={format_value}
      />
    </FormControl>
  )
}
