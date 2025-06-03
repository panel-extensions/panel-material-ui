import Box from "@mui/material/Box"
import Chip from "@mui/material/Chip"
import Button from "@mui/material/Button"
import IconButton from "@mui/material/IconButton"
import InputAdornment from "@mui/material/InputAdornment"
import FilterListIcon from "@mui/icons-material/FilterList"
import ClearIcon from "@mui/icons-material/Clear"
import Checkbox from "@mui/material/Checkbox"
import TextField from "@mui/material/TextField"
import MenuItem from "@mui/material/MenuItem"
import ListItemText from "@mui/material/ListItemText"
import FormControl from "@mui/material/FormControl"
import InputLabel from "@mui/material/InputLabel"
import Select from "@mui/material/Select"
import OutlinedInput from "@mui/material/OutlinedInput"
import FilledInput from "@mui/material/FilledInput"
import Input from "@mui/material/Input"
import Typography from "@mui/material/Typography"
import ListSubheader from "@mui/material/ListSubheader"
import {findNotebook} from "./utils"

export function render({model, el}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [label] = model.useState("label")
  const [options] = model.useState("options")
  const [sx] = model.useState("sx")
  const [size] = model.useState("size")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  // SelectSearch specific props
  const [bookmarks] = model.useState("bookmarks", [])
  const [dropdown_height] = model.useState("dropdown_height")
  const [filterStr, setFilterStr] = model.useState("filter_str")
  const [filter_on_search] = model.useState("filter_on_search")
  const [open, setOpen] = model.useState("dropdown_open")
  const [searchable] = model.useState("searchable")
  const [value_label] = model.useState("value_label")

  // MultiChoice specific props
  const multi = model.esm_constants.multi || false
  let chip = false
  let delete_button = false
  let max_items = 1
  let solid = false
  let placeholder = null
  if (multi) {
    const [chip_state] = model.useState("chip")
    const [delete_button_state] = model.useState("delete_button")
    const [max_items_state] = model.useState("max_items")
    const [placeholder_state] = model.useState("placeholder")
    const [solid_state] = model.useState("solid")
    chip = chip_state === undefined ? true : chip_state
    delete_button = delete_button_state === undefined ? true : delete_button_state
    max_items = max_items_state === undefined ? null : max_items_state
    solid = solid_state === undefined ? true : solid_state
    placeholder = placeholder_state === undefined ? null : placeholder_state
  }

  // Offset notebook node
  const [notebook, feed] = findNotebook(el)
  let nb_menu_props = {}
  if (notebook !== null) {
    const {x, y} = notebook.getBoundingClientRect()
    let [left, top] = [-x, feed.scrollTop - y]
    const [position, setPosition] = React.useState([left, top])
    nb_menu_props = {
      PaperProps: {
        style: {transform: `translate(${position[0]}px, ${position[1]}px)`}
      },
      TransitionComponent: React.Fragment
    }
    React.useEffect(() => {
      if (open) {
        feed.style.overflow = "hidden"
        const {x, y, height} = notebook.getBoundingClientRect()
        left = -x
        top = ((feed.scrollTop > (0.67*height)) ? y : (feed.scrollTop - y))
        setPosition([left, top])
      } else {
        feed.style.overflow = "auto"
      }
    }, [open])
  }

  // Select specific props
  const [disabled_options] = model.useState("disabled_options", [])

  const matches = (label) => {
    return label.toLowerCase().includes(filterStr.toLowerCase())
  }

  const processOptions = () => {
    if (Array.isArray(options)) {
      return options.map((opt) => {
        const option = options.find((o) => (Array.isArray(o) ? o[0] === opt : o === opt))
        const value = Array.isArray(option) ? option[1] : option
        const label = Array.isArray(option) ? option[0] : option
        return {value, label}
      })
    }
    return []
  }

  const menuRef = React.useRef(null)

  const items = processOptions().filter(({label}) => (!filter_on_search || filterStr === "" || matches(label)))
  const bookmarkedOptions = items.filter(({value}) => bookmarks.includes(value))
  const filteredOptions = items.filter(({value}) => !bookmarks.includes(value))
  let matchedOptions = [...bookmarkedOptions, ...filteredOptions].filter(({label}) => matches(label))

  if (!multi) {
    matchedOptions = matchedOptions.slice(0, 1)
  }

  const matched_count = matchedOptions.length

  // Checkbox logic for multi-select
  const isChecked = () => filteredOptions.length > 0 &&
    (filterStr ? (
      matchedOptions.every(item => value.includes(item.value))
    ) : (
      filteredOptions.every(item => value.includes(item.value))
    ))

  const isIndeterminate = () => filteredOptions.length > 0 &&
    (filterStr ? (
      matchedOptions.some(item => value.includes(item.value)) &&
      !matchedOptions.every(item => value.includes(item.value))
    ) : (
      filteredOptions.some(item => value.includes(item.value)) &&
      !filteredOptions.every(item => value.includes(item.value))
    ))

  const [checked, setChecked] = React.useState(isChecked)
  const [indeterminate, setIndeterminate] = React.useState(isIndeterminate)

  React.useEffect(() => {
    setChecked(isChecked)
    setIndeterminate(isIndeterminate())
  }, [value, filterStr])

  React.useEffect(() => {
    if (!multi && filterStr && menuRef.current) {
      const matchedElement = menuRef.current.querySelector('[data-matched="true"]')
      if (matchedElement) {
        matchedElement.scrollIntoView({block: "nearest"})
      }
    }
  }, [filterStr])

  const MenuProps = {
    container: el,
    disablePortal: true,
    sx: {height: dropdown_height},
    MenuListProps: {
      ref: menuRef,
    },
    ...nb_menu_props
  }

  const getInput = () => {
    const inputProps = {
      id: "select-input",
      label: label || "",
      color
    }
    switch (variant) {
      case "outlined":
        return <OutlinedInput {...inputProps} />
      case "filled":
        return <FilledInput {...inputProps} />
      default:
        return <Input {...inputProps} />
    }
  }

  const renderValue = (selected) => {
    if (multi && placeholder && selected.length === 0) {
      return placeholder
    } else if (value_label) {
      return value_label
    }
    if (multi && chip) {
      return (
        <Box sx={{display: "flex", flexWrap: "wrap", gap: 0.5}}>
          {selected.map((selected_value) => (
            <Chip
              color={color}
              variant={solid ? "filled" : "outlined"}
              key={selected_value}
              label={selected_value}
              onMouseDown={(event) => event.stopPropagation()}
              onDelete={delete_button ? () => {
                setValue(value.filter(v => v !== selected_value))
              } : undefined}
            />
          ))}
        </Box>
      )
    }
    return multi ? selected.join(", ") : selected
  }

  const renderMenuItems = () => {
    if (typeof options === "object" && !Array.isArray(options)) {
      return Object.entries(options).flatMap(([groupLabel, groupOptions]) => [
        <ListSubheader key={`${groupLabel}-header`}>{groupLabel}</ListSubheader>,
        ...groupOptions.map((option, idx) => {
          const optValue = Array.isArray(option) ? option[1] : option
          const optLabel = Array.isArray(option) ? option[0] : option
          return (
            <MenuItem
              key={`${groupLabel}-${idx}`}
              value={optValue}
              disabled={disabled_options?.includes(optValue)}
            >
              {optLabel}
            </MenuItem>
          )
        }),
      ])
    }

    return (
      <>
        {searchable && <MenuItem
          disableGutters
          disableRipple
          onClick={(e) => {
            e.stopPropagation()
          }}
          sx={{
            paddingTop: 0,
            paddingBottom: 0,
            position: "sticky",
            pointerEvents: "auto",
            top: 0,
            zIndex: 100,
            backgroundColor: "background.paper",
            "&:hover": {
              backgroundColor: "background.paper",
            },
            "&.Mui-focusVisible": {
              backgroundColor: "background.paper",
            },
            display: "flex",
            flexDirection: "column",
          }}
        >
          <TextField
            sx={{
              paddingTop: 0,
              paddingBottom: 0,
              zIndex: 1,
              "&.Mui-focused": {
                backgroundColor: "background.paper",
              }
            }}
            fullWidth
            variant="filled"
            placeholder="Search..."
            value={filterStr}
            onKeyDown={(e) => {
              e.stopPropagation()
              if (e.key === "Enter" && filterStr) {
                if (multi) {
                  const filteredValues = [...bookmarkedOptions, ...filteredOptions]
                    .filter(item => item.label.toLowerCase().includes(filterStr.toLowerCase()))
                    .map(item => item.value)
                  const newValues = [...new Set([...value, ...filteredValues])]
                  setValue(max_items ? newValues.slice(0, max_items) : newValues)
                } else {
                  setValue(filteredOptions.find(item =>
                    item.label.toLowerCase().includes(filterStr.toLowerCase())
                  ).value)
                }
              }
            }}
            onChange={(e) => {
              setFilterStr(e.target.value)
              e.stopPropagation()
            }}
            onClick={(e) => {
              e.stopPropagation()
              e.preventDefault()
            }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <FilterListIcon />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment
                    onMouseDown={(e) => {
                      e.preventDefault();
                      e.stopPropagation();
                    }}
                    onClick={(e) => {
                      setFilterStr("")
                      setOpen(false)
                      e.preventDefault()
                      e.stopPropagation()
                    }}
                    position="end"
                    sx={{zIndex: 100}}
                  >
                    <IconButton>
                      <ClearIcon/>
                    </IconButton>
                  </InputAdornment>
                ),
              },
            }}
          />
          {multi && searchable && (
            <Box sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexDirection: "row",
              width: "100%",
              borderBottomColor: "divider",
              borderBottomWidth: 1,
              borderBottomStyle: "solid"
            }}
            >
              <Checkbox
                size="small"
                checked={checked}
                indeterminate={indeterminate}
                color={color}
                onMouseDown={(e) => {
                  e.preventDefault()
                  e.stopPropagation()
                }}
                onClick={(e) => {
                  const filteredValues = filteredOptions.map(item => item.value)
                  if (filterStr) {
                    if (!checked || indeterminate) {
                      setValue([...new Set([...value, ...filteredValues.filter(matches)])])
                      setChecked(true)
                      setIndeterminate(false)
                    } else {
                      setValue(value.filter(v => !matches(v)))
                      setChecked(false)
                      setIndeterminate(false)
                    }
                  } else {
                    if (!checked || indeterminate) {
                      setValue(filteredValues)
                      setChecked(true)
                      setIndeterminate(false)
                    } else {
                      setValue([])
                      setChecked(false)
                      setIndeterminate(false)
                    }
                  }
                  e.preventDefault()
                  e.stopPropagation()
                }}
              />
              <Typography
                variant="caption"
                sx={{
                  display: "block",
                  px: 1,
                  py: 0,
                  color: "text.secondary"
                }}
              >
                {filterStr ? (
                  matched_count > 0 ?
                    `${checked ? "Deselect" : "Select"} ${matched_count} matched items` :
                    "No items matched"
                ) : (
                  `${checked ? "Deselect" : "Select"} ${checked ? value.length : (items.length - value.length)} items`
                )}
              </Typography>
              {filterStr && (
                <Button
                  size="small"
                  variant="text"
                  onClick={(e) => {
                    setFilterStr("")
                    e.stopPropagation()
                  }}
                >
                  Clear
                </Button>
              )}
            </Box>
          )}
        </MenuItem>}
        {[
          ...(bookmarkedOptions.length > 0 ? [
            ...bookmarkedOptions.map(item => ({...item, isBookmarked: true})),
            {isDivider: true}
          ] : []),
          ...filteredOptions.map(item => ({...item, isBookmarked: false}))
        ].map((item, index) => {
          if (item.isDivider) {
            return <MenuItem key={`divider-${index}`} disabled divider />
          }

          const matched = filterStr && matches(item.label)
          const {value: opt, label, isBookmarked} = item
          const handleClick = (e) => {
            if (!multi) {
              setValue(opt)
              setOpen(false)
              return
            }
            const isChecked = !value.includes(opt)
            if (isChecked) {
              if (max_items && value.length >= max_items) {
                setValue([...value.slice(1), opt])
              } else {
                setValue([...value, opt])
              }
            } else {
              setValue(value.filter(v => v !== opt))
            }
            e.stopPropagation()
          }

          return (
            <MenuItem
              data-matched={matched}
              disabled={disabled_options?.includes(opt)}
              disableGutters
              key={opt}
              onClick={handleClick}
              sx={{
                backgroundColor: matched ? "action.selected" : "inherit",
                "&:hover": {
                  backgroundColor: matched ? "action.selected" : "action.hover",
                }
              }}
              value={opt}
            >
              {multi && searchable && <Checkbox color={color} checked={value.includes(opt)} onClick={handleClick} />}
              <ListItemText primary={label} sx={{margin: 2}} />
            </MenuItem>
          )
        })}
      </>
    )
  }

  return (
    <FormControl disabled={disabled} fullWidth variant={variant}>
      {label && <InputLabel color={color} id={`select-label-${model.id}`}>{label}</InputLabel>}
      <Select
        color={color}
        disabled={disabled}
        input={getInput()}
        labelId={`select-label-${model.id}`}
        multiple={multi}
        onClose={() => setOpen(false)}
        onChange={(event) => {
          const newValue = event.target.value
          if (multi && max_items && newValue.length > max_items) {
            return
          }
          setValue(newValue)
        }}
        onOpen={() => setOpen(true)}
        open={open}
        renderValue={renderValue}
        size={size}
        sx={{padding: 0, margin: 0, "& .MuiMenu-list": {padding: 0}, ...sx}}
        value={value}
        variant={variant}
        MenuProps={MenuProps}
      >
        {renderMenuItems()}
      </Select>
    </FormControl>
  )
}
