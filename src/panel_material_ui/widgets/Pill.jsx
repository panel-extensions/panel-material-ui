import Box from "@mui/material/Box"
import Chip from "@mui/material/Chip"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import {render_description} from "./description"
import {render_icon_text} from "./utils"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [disabled_options] = model.useState("disabled_options", [])
  const [label] = model.useState("label")
  const [options] = model.useState("options")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")
  const multi = model.esm_constants.multi || false
  let max_items = null
  if (multi) {
    const [max_items_state] = model.useState("max_items")
    max_items = max_items_state === undefined ? null : max_items_state
  }

  const focusRef = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => focusRef.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

  const processOptions = () => {
    if (Array.isArray(options)) {
      return options.map((option) => {
        if (Array.isArray(option)) {
          return {label: option[0], value: option[1]}
        }
        return {label: option, value: option}
      })
    }
    if (options && typeof options === "object") {
      return Object.entries(options).map(([label, value]) => ({label, value}))
    }
    return []
  }

  const chipVariant = variant === "filled" ? "filled" : "outlined"
  const chipSize = size === "small" ? "small" : "medium"
  const largeChipSx = size === "large" ? {
    height: 36,
    fontSize: "0.95rem",
    px: 1.5,
    "& .MuiChip-label": {px: 1}
  } : {}
  const outlinedSx = chipVariant === "outlined"
    ? {
      borderColor: (theme) => (
        theme.palette.mode === "light" ? theme.palette.grey[300] : theme.palette.divider
      )
    }
    : {}

  const selectedValues = multi ? (Array.isArray(value) ? value : []) : value
  const items = processOptions()

  const handleSelect = (optionValue) => {
    if (disabled) {
      return
    }
    if (multi) {
      if (selectedValues.includes(optionValue)) {
        setValue(selectedValues.filter((item) => item !== optionValue))
        return
      }
      let nextValues = [...selectedValues, optionValue]
      if (max_items && nextValues.length > max_items) {
        nextValues = nextValues.slice(1)
      }
      setValue(nextValues)
    } else if (selectedValues !== optionValue) {
      setValue(optionValue)
    }
  }

  return (
    <FormControl component="fieldset" disabled={disabled} fullWidth>
      {label && (
        <FormLabel component="legend" sx={{mb: 0.5}}>
          {render_icon_text(label)}
          {model.description ? render_description({model, el, view}) : null}
        </FormLabel>
      )}
      <Box
        role="group"
        sx={{display: "flex", flexWrap: "wrap", gap: 1, alignItems: "center", ...sx}}
      >
        {items.map((item, index) => {
          const isSelected = multi
            ? selectedValues.includes(item.value)
            : selectedValues === item.value
          const isDisabled = disabled || disabled_options?.includes(item.value)
          return (
            <Chip
              key={`${index}-${item.label}`}
              color={isSelected ? color : "default"}
              disabled={isDisabled}
              clickable={!isDisabled}
              onClick={() => handleSelect(item.value)}
              ref={index === 0 ? focusRef : null}
              size={chipSize}
              sx={{...outlinedSx, ...largeChipSx}}
              label={render_icon_text(item.label)}
              variant={isSelected ? chipVariant : "outlined"}
            />
          )
        })}
      </Box>
    </FormControl>
  )
}
