import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import Icon from "@mui/material/Icon"
import Rating from "@mui/material/Rating"
import {render_icon} from "./utils"

const SIZES = {
  small: "1.5em",
  medium: "2.5em",
  large: "3.5em",
}

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [empty_icon] = model.useState("empty_icon")
  const [end] = model.useState("end")
  const [icon] = model.useState("icon")
  const [label] = model.useState("label")
  const [only_selected] = model.useState("only_selected")
  const [precision] = model.useState("precision")
  const [readonly] = model.useState("readonly")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")

  const ref = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  const empty = empty_icon || icon
  el.style.overflowY = "clip"

  return (
    <FormControl component="fieldset" disabled={disabled} fullWidth>
      {label && <FormLabel id="radio-group-label">{label}{model.description ? render_description({model, el, view}) : null}</FormLabel>}
      <Rating
        color={color}
        disabled={disabled}
        emptyIcon={empty ? render_icon(empty, null, size, SIZES[size]) : null}
        fullWidth
        highlightSelectedOnly={only_selected}
        icon={icon ? render_icon(icon, color, size, SIZES[size]) : null}
        ref={ref}
        max={end}
        onChange={(event, newValue) => setValue(newValue)}
        precision={precision}
        readOnly={readonly}
        size={size}
        sx={sx}
        value={value}
      />
    </FormControl>
  );
}
