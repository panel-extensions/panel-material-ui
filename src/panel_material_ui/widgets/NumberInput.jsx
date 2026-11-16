import TextField from "@mui/material/TextField"
import InputAdornment from "@mui/material/InputAdornment"
import IconButton from "@mui/material/IconButton"
import AddIcon from "@mui/icons-material/Add"
import RemoveIcon from "@mui/icons-material/Remove"
import {float_regex, int_regex, render_icon_text, render_icon_text_as_string} from "./utils"
import {render_description} from "./description"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [format] = model.useState("format")
  const [helper_text] = model.useState("helper_text")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [step] = model.useState("step")
  const [min] = model.useState("start")
  const [max] = model.useState("end")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [, setValueThrottled] = model.useState("value_throttled")
  const [wheel_wait] = model.useState("wheel_wait")

  const [oldValue, setOldValue] = React.useState(value)
  const [focused, setFocused] = React.useState(false)
  const [editableValue, setEditableValue] = React.useState(value)

  const ref = React.useRef(null)
  const throttleTimer = React.useRef(null)
  React.useEffect(() => {
    const handler = () => {
      ref.current?.focus()
    }
    model.on("msg:custom", handler)
    return () => {
      model.off("msg:custom", handler)
      clearTimeout(throttleTimer.current)
    }
  }, [model])

  const clamp = (v) => {
    if (v === null) {
      return v
    }
    if (max != null && v > max) {
      return max
    }
    if (min != null && v < min) {
      return min
    }
    return v
  }

  // Steps (buttons, arrow and page keys) update value_throttled once they
  // pause for wheel_wait ms, typed values are committed immediately.
  const commit = (newValue, debounce = false) => {
    setValue(newValue)
    setEditableValue(newValue)
    clearTimeout(throttleTimer.current)
    if (debounce) {
      throttleTimer.current = setTimeout(() => setValueThrottled(newValue), wheel_wait ?? 0)
    } else {
      setValueThrottled(newValue)
    }
  }

  const validate = (value) => {
    const regex = model.mode == "int" ? int_regex : float_regex
    if (value === "" || ["", "-", ".", "-."].includes(value)) {
      return null
    } else if (regex.test(value)) {
      return clamp(Number(value))
    } else {
      return oldValue
    }
  }

  const commitTyped = () => commit(validate(editableValue))

  React.useEffect(() => {
    setEditableValue(value)
  }, [value])

  // Derived during render, since updating it in an effect leaves the input
  // showing the previous text for a render and drops fast keystrokes
  const valueLabel = (format && !focused ? format.doFormat([value], {loc: 0})[0] : editableValue) ?? ""

  // While focused, step from the typed text rather than the last committed value
  const current = () => (focused ? validate(editableValue) : value)

  const increment = (multiplier = 1) => {
    const base = current()
    setOldValue(value)
    if (base === null) {
      commit(min != null ? min : 0, true)
    } else {
      const incremented = Math.round((base + (step * multiplier)) * 100000000000) / 100000000000
      commit(max != null ? Math.min(max, incremented) : incremented, true)
    }
  }
  const decrement = (multiplier = 1) => {
    const base = current()
    setOldValue(value)
    if (base === null) {
      commit(max != null ? max : 0, true)
    } else {
      const decremented = Math.round((base - (step * multiplier)) * 100000000000) / 100000000000
      commit(min != null ? Math.max(min, decremented) : decremented, true)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      commitTyped()
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      increment();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      decrement();
    } else if (e.key === "PageUp") {
      e.preventDefault();
      increment(model.page_step_multiplier);
    } else if (e.key === "PageDown") {
      e.preventDefault();
      decrement(model.page_step_multiplier);
    }
  }
  return (
    <TextField
      color={color}
      disabled={disabled}
      error={error_state}
      fullWidth
      helperText={helper_text ? render_icon_text(helper_text) : undefined}
      inputRef={ref}
      label={model.description ? <>{render_icon_text(label)}{render_description({model, el, view})}</> : render_icon_text(label)}
      onBlur={() => {
        setFocused(false)
        commitTyped()
      }}
      onChange={(event) => { setEditableValue(event.target.value) }}
      onFocus={() => {
        setFocused(true)
        setOldValue(value)
      }}
      onKeyDown={handleKeyDown}
      placeholder={render_icon_text_as_string(placeholder)}
      size={size}
      sx={sx}
      value={valueLabel}
      variant={variant}
      slotProps={{
        input: {
          inputMode: "decimal",
          sx: {padding: 0},
          startAdornment: (
            <InputAdornment position="start">
              <IconButton onClick={() => decrement()} size="small" color="default" disabled={disabled}>
                <RemoveIcon fontSize="small" />
              </IconButton>
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              <IconButton onClick={() => increment()} size="small" color="default" disabled={disabled}>
                <AddIcon fontSize="small" />
              </IconButton>
            </InputAdornment>
          ),
        }
      }}
    />
  );
}
