import TextField from "@mui/material/TextField"
import {render_description} from "./description"
import {render_icon_text, render_icon_text_as_string, denseSx} from "./utils"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [helper_text] = model.useState("helper_text")
  const [label] = model.useState("label")
  const [max_length] = model.useState("max_length")
  const [placeholder] = model.useState("placeholder")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [value_input, setValueInput] = model.useState("value_input")
  const [variant] = model.useState("variant")

  const ref = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  return (
    <TextField
      color={color}
      disabled={disabled}
      error={error_state}
      helperText={helper_text ? render_icon_text(helper_text) : undefined}
      inputRef={ref}
      fullWidth
      slotProps={{htmlInput: {maxLength: max_length}}}
      label={model.description ? <>{render_icon_text(label)}{render_description({model, el, view})}</> : render_icon_text(label)}
      multiline={model.esm_constants.multiline}
      placeholder={render_icon_text_as_string(placeholder)}
      onBlur={() => setValue(value_input)}
      onChange={(event) => setValueInput(event.target.value)}
      onKeyDown={(event) => {
        if (event.key === "Enter") {
          model.send_event("enter", event)
          setValue(value_input)
        }
      }}
      rows={4}
      size={size}
      // MUI's OutlinedInput/InputBase has no native size="large" variant
      // (only "small" is styled), so without this "large" would render
      // pixel-identical to "medium". "small" is left untouched here since
      // MUI's own <TextField> already wires size="small" through to
      // InputLabel/InputBase natively and gets it right out of the box.
      sx={size === "large" ? denseSx(size, sx) : sx}
      variant={variant}
      value={value_input}
    />
  )
}
