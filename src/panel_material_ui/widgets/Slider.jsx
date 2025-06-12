import Box from "@mui/material/Box"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import IconButton from "@mui/material/IconButton"
import InputAdornment from "@mui/material/InputAdornment"
import RemoveIcon from "@mui/icons-material/Remove"
import AddIcon from "@mui/icons-material/Add"
import Slider from "@mui/material/Slider"
import TextField from "@mui/material/TextField"
import Typography from "@mui/material/Typography"
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
  const int = model.esm_constants.int

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
  let setFocused = null
  let focused = false
  let handleChange = null
  let commitValue = null
  if (editable) {
    const [fixed_start] = model.useState("fixed_start")
    const [fixed_end] = model.useState("fixed_end")
    const [focus, set_focused] = React.useState(false)

    const [editable_value, setEditableValue] = React.useState()

    editableValue = editable_value ?? editableValue
    setFocused = set_focused ?? setFocused
    focused = focus ?? focused
    React.useEffect(() => {
      if (Array.isArray(value)) {
        setEditableValue(format && !focused ? value.map((v) => format_value(v, v, true)) : value)
      } else {
        setEditableValue(format && !focused ? format_value(value, value, true) : value)
      }
    }, [format, value, focused])

    const validate = (new_value, index) => {
      const regex = int ? int_regex : float_regex
      if (new_value === "") {
        return null
      } else if (regex.test(new_value)) {
        return int ? Math.round(Number(new_value)) : Number(new_value)
      } else if (Array.isArray(value)) {
        return value[index]
      } else {
        return value
      }
    }

    handleChange = (event, index) => {
      if (Array.isArray(value)) {
        setEditableValue(index === 0 ? [event.target.value, value[1]] : [value[0], event.target.value])
      } else {
        setEditableValue(event.target.value)
      }
    }

    handleKeyDown = (e, index) => {
      if (e.key === "Enter") {
        setFocused(false)
        commitValue(index)
      } else if (e.key === "ArrowUp") {
        e.preventDefault()
        increment(index, 1)
      } else if (e.key === "ArrowDown") {
        e.preventDefault()
        increment(index, -1)
      } else if (e.key === "PageUp") {
        e.preventDefault()
        increment(index, 1)
      } else if (e.key === "PageDown") {
        e.preventDefault()
        increment(index, -1)
      }
    }

    commitValue = (index) => {
      if (!focus) { return }
      let edited_value = Array.isArray(value) ? editableValue[index] : editableValue
      edited_value = int ? Math.round(Number(edited_value)) : edited_value
      if (Array.isArray(value)) {
        if (index === 0 && edited_value > value[1]) {
          edited_value = value[1]
        } else if (index == 1 && edited_value < value[0]) {
          edited_value = value[0]
        }
      }
      if (fixed_start != null && edited_value < fixed_start) {
        edited_value = fixed_start
      } else if (fixed_end != null && edited_value > fixed_end) {
        edited_value = fixed_end
      }
      let new_value
      if (Array.isArray(value)) {
        new_value = index === 0 ? [validate(edited_value, 0), value[1]] : [value[0], validate(edited_value, 1)]
        setValue(new_value)
        new_value = new_value[index]
      } else {
        new_value = validate(edited_value, 0)
        setValue(new_value)
      }
      if (new_value < start) {
        setStart(new_value)
      } else if (new_value > end) {
        setEnd(new_value)
      }
    }

    increment = (index, multiplier = 1) => {
      if (Array.isArray(value)) {
        let val = value[index]
        const fixed = index === 0 ? fixed_start : fixed_end
        if (val === null) {
          val = fixed != null ? fixed : 0
        } else {
          val = Math.round((val + (step * multiplier)) * 100000000000) / 100000000000
        }
        if (index === 0) {
          setValue([val, value[1]])
        } else {
          setValue([value[0], val])
        }
      } else if (value === null) {
        setValue(fixed_start != null ? fixed_start : 0)
      } else {
        const incremented = Math.round((value + (step * multiplier)) * 100000000000) / 100000000000
        setValue(fixed_end != null ? Math.min(fixed_end, incremented) : incremented)
      }
    }
  }

  function format_value(d, _, useLabel=true) {
    if (valueLabel && useLabel) {
      return valueLabel
    } else if (discrete) {
      return labels[d]
    } else if (datetime) {
      return dayjs.unix(d / 1000).format(format || "YYYY-MM-DD HH:mm:ss")
    } else if (date) {
      return dayjs.unix(d / 1000).format(format || "YYYY-MM-DD")
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
          if (date || datetime) {
            tick = {...tick, value: dayjs.unix(tick.value / 1000)}
          }
          return tick
        }
        return {
          value: date || datetime ? dayjs.unix(tick / 1000) : tick,
          label: format_value(tick, tick, false)
        }
      })
    }
  }, [marks, format, labels])

  return (
    <FormControl disabled={disabled} fullWidth sx={orientation === "vertical" ? {height: "100%", ...sx} : {...sx}}>
      {editable ? (
        <Box sx={{display: "flex", flexDirection: "row", alignItems: "center", width: "100%"}}>
          <FormLabel sx={{whiteSpace: "nowrap"}}>
            {label && `${label}: `}
          </FormLabel>
          <Box sx={{display: "flex", flexDirection: "row", flexGrow: 1}}>
            <TextField
              color={color}
              disabled={disabled}
              onBlur={() => { setFocused(false); commitValue(0) }}
              onChange={(e) => handleChange(e, 0)}
              onFocus={() => setFocused(true)}
              onKeyDown={(e) => handleKeyDown(e, 0)}
              size="small"
              sx={{flexGrow: 1, minWidth: 0}}
              value={Array.isArray(value) ? (editableValue ? editableValue[0] : "") : editableValue}
              variant="standard"
              InputProps={{
                disableUnderline: true,
                sx: {ml: "0.5em", mt: "0.2em"},
                startAdornment: (
                  <InputAdornment position="start">
                    <IconButton onClick={(e) => { increment(0, -1); e.stopPropagation(); e.preventDefault(); }} size="small" color="default" sx={{p: 0}}>
                      <RemoveIcon fontSize="small" />
                    </IconButton>
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={(e) => { increment(0, 1); e.stopPropagation(); e.preventDefault(); }} size="small" color="default" sx={{p: 0}}>
                      <AddIcon fontSize="small" />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
            {Array.isArray(value) && (
              <>
                <Typography sx={{alignSelf: "end", fontWeight: 600}}>...</Typography>
                <TextField
                  color={color}
                  disabled={disabled}
                  onBlur={() => { setFocused(false); commitValue(1) }}
                  onChange={(e) => handleChange(e, 1)}
                  onFocus={() => setFocused(true)}
                  onKeyDown={(e) => handleKeyDown(e, 1)}
                  size="small"
                  sx={{flexGrow: 1, minWidth: 0, mr: "0.5em"}}
                  value={Array.isArray(value) ? (editableValue ? editableValue[1] : "") : editableValue}
                  variant="standard"
                  InputProps={{
                    disableUnderline: true,
                    sx: {ml: "0.5em", mt: "0.2em"},
                    startAdornment: (
                      <InputAdornment position="start">
                        <IconButton onClick={(e) => { increment(1, -1); e.stopPropagation(); e.preventDefault(); }} size="small" color="default" sx={{p: 0}}>
                          <RemoveIcon fontSize="small" />
                        </IconButton>
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={(e) => { increment(1, 1); e.stopPropagation(); e.preventDefault(); }} size="small" color="default" sx={{p: 0}}>
                          <AddIcon fontSize="small" />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </>
            )}
          </Box>
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
