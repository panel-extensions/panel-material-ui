import Box from "@mui/material/Box"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import IconButton from "@mui/material/IconButton"
import InputAdornment from "@mui/material/InputAdornment"
import RemoveIcon from "@mui/icons-material/Remove"
import AddIcon from "@mui/icons-material/Add"
import Slider from "@mui/material/Slider"
import TextField from "@mui/material/TextField"
import dayjs from "dayjs"
import {int_regex, float_regex} from "./utils"

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
  let [end, setEnd] = model.useState("end")
  let [start, setStart] = model.useState("start")

  const date = model.esm_constants.date
  const datetime = model.esm_constants.datetime
  const discrete = model.esm_constants.discrete
  const editable = model.esm_constants.editable

  let labels = null
  if (discrete) {
    const [labels_state] = model.useState("options")
    labels = labels_state === undefined ? [] : labels_state
    start = 0
    end = labels.length - 1
  }

  let editableValue = null
  let handleKeyDown = null
  let increment = null
  let decrement = null
  let setFocused = null
  let focused = false
  let handleChange = null
  if (editable) {
    const [fixed_start] = model.useState("fixed_start")
    const [fixed_end] = model.useState("fixed_end")
    const [oldValue, setOldValue] = React.useState(value)
    const [focus, set_focused] = React.useState(false)

    const [editable_value, setEditableValue] = React.useState()

    editableValue = editable_value ?? editable_value
    setFocused = set_focused ?? setFocused
    focused = focus ?? focused
    React.useEffect(() => {
      setEditableValue(format && !focused ? format_value(value, value, true) : value)
    }, [format, value, focused])

    const validate = (value) => {
      const regex = model.mode == "int" ? int_regex : float_regex
      if (value === "") {
        return null
      } else if (regex.test(value)) {
        return Number(value)
      } else {
        return oldValue
      }
    }

    handleChange = (event) => {
      if (event.target.value === "-" || event.target.value === "") {
        setEditableValue(event.target.value)
        return
      }
      const newValue = validate(event.target.value)
      setOldValue(value)
      if (fixed_start != null && newValue < fixed_start) {
        setValue(fixed_start)
      } else if (fixed_end != null && newValue > fixed_end) {
        setValue(fixed_end)
      } else if (newValue != null) {
        let clipped = fixed_start != null ? Math.max(fixed_start, newValue) : newValue
        clipped = fixed_end != null ? Math.min(fixed_end, clipped) : clipped
        setValue(clipped)
        if (clipped < start) {
          setStart(clipped)
        } else if (clipped > end) {
          setEnd(clipped)
        }
      }
    }

    handleKeyDown = (e) => {
      if (e.key === "ArrowUp") {
        e.preventDefault()
        increment()
      } else if (e.key === "ArrowDown") {
        e.preventDefault()
        decrement()
      } else if (e.key === "PageUp") {
        e.preventDefault()
        increment(1)
      } else if (e.key === "PageDown") {
        e.preventDefault()
        decrement(1)
      }
    }

    increment = (multiplier = 1) => {
      setOldValue(value)
      if (value === null) {
        setValue(fixed_start != null ? fixed_start : 0)
      } else {
        const incremented = Math.round((value + (step * multiplier)) * 100000000000) / 100000000000
        setValue(fixed_end != null ? Math.min(fixed_end, incremented) : incremented)
      }

    }
    decrement = (multiplier = 1) => {
      setOldValue(value)
      if (value === null) {
        setValue(fixed_end != null ? fixed_end : 0)
      } else {
        const decremented = Math.round((value - (step * multiplier)) * 100000000000) / 100000000000
        setValue(fixed_start != null ? Math.max(fixed_start, decremented) : decremented)
      }
    }
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
    <FormControl disabled={disabled} fullWidth sx={orientation === "vertical" ? {height: "100%", ...sx} : {...sx}}>
      {editable ? (
        <Box sx={{display: "flex", flexDirection: "row", alignItems: "center", width: "100%"}}>
          <FormLabel>
            {label && `${label}: `}
          </FormLabel>
          <TextField
            color={color}
            disabled={disabled}
            onBlur={() => setFocused(false)}
            onChange={handleChange}
            onFocus={() => setFocused(true)}
            onKeyDown={handleKeyDown}
            size="small"
            sx={{width: "100%"}}
            value={editableValue}
            variant="standard"
            InputProps={{
              disableUnderline: true,
              inputMode: "decimal",
              sx: {ml: "0.5em", mt: "0.2em", flexGrow: 1},
              startAdornment: (
                <InputAdornment position="start">
                  <IconButton onClick={(e) => { decrement(); e.stopPropagation(); e.preventDefault(); }} size="small" color="default">
                    <RemoveIcon fontSize="small" />
                  </IconButton>
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton onClick={(e) => { increment(); e.stopPropagation(); e.preventDefault(); }} size="small" color="default">
                    <AddIcon fontSize="small" />
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
        </Box>
      ) : (
        <FormLabel>
          {label && `${label}: `}
          { show_value &&
          <strong>
            {value_label}
          </strong>
          }
        </FormLabel>)}
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
