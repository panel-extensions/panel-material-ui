import Box from '@mui/material/Box'
import Chip from '@mui/material/Chip'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import InputAdornment from '@mui/material/InputAdornment'
import FilterListIcon from '@mui/icons-material/FilterList'
import ClearIcon from '@mui/icons-material/Clear'
import Checkbox from '@mui/material/Checkbox'
import TextField from '@mui/material/TextField'
import MenuItem from '@mui/material/MenuItem'
import ListItemText from '@mui/material/ListItemText'
import FormControl from '@mui/material/FormControl'
import InputLabel from '@mui/material/InputLabel'
import Select from '@mui/material/Select'
import OutlinedInput from '@mui/material/OutlinedInput'
import FilledInput from '@mui/material/FilledInput'
import Input from '@mui/material/Input'
import Typography from '@mui/material/Typography'

export function render({ model, view }) {
  const [bookmarks] = model.useState("bookmarks")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [dropdown_height] = model.useState("dropdown_height")
  const [filterStr, setFilterStr] = model.useState("filter_str")
  const [filter_on_search] = model.useState("filter_on_search")
  const [label] = model.useState("label")
  const [open, setOpen] = model.useState("dropdown_open")
  const [options] = model.useState("options")
  const [placeholder] = model.useState("placeholder")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  const multi = model.esm_constants.multi
  const solid = true
  const delete_button = true
  let chip = false
  if (multi) {
    [chip] = model.useState("chip")
  }

  const menuRef = React.useRef(null)

  React.useEffect(() => {
    if (!multi && filterStr && menuRef.current) {
      const matchedElement = menuRef.current.querySelector('[data-matched="true"]')
      if (matchedElement) {
        matchedElement.scrollIntoView({ block: 'nearest' })
      }
    }
  }, [filterStr])

  const matches = (label) => {
    return label.toLowerCase().includes(filterStr.toLowerCase())
  }

  const items = options
  .map((opt) => {
    const option = options.find((o) => (Array.isArray(o) ? o[0] === opt : o === opt))
    const value = Array.isArray(option) ? option[1] : option
    const label = Array.isArray(option) ? option[0] : option
    return { value, label }
  }).filter(({label}) => (!filter_on_search || filterStr === "" || matches(label)))

  const bookmarkedOptions = items.filter(({ value }) => bookmarks.includes(value))
  const filteredOptions = items.filter(({ value }) => !bookmarks.includes(value))
  let matchedOptions = [...bookmarkedOptions, ...filteredOptions].filter(({ label }) => matches(label))
  if (!multi) {
    matchedOptions = matchedOptions.slice(0, 1)
  }

  const matched_count = matchedOptions.length

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

  const MenuProps = {
    disablePortal: true,
    getContentAnchorEl: null,
    anchorOrigin: {
      vertical: 'bottom',
      horizontal: 'left',
    },
    sx: {height: dropdown_height},
    MenuListProps: {
      ref: menuRef,
    },
  }
  return (
    <FormControl fullWidth variant={variant} disabled={disabled}>
      {label && <InputLabel id={`${model.id}-label`}>{label}</InputLabel>}
      <Select
        multiple={multi}
        color={color}
        variant={variant}
        value={value}
        displayEmpty
        input={variant === "outlined" ?
          <OutlinedInput label={value.length > 0 || open ? label : ""}/> :
            variant === "filled" ?
          <FilledInput label={value.length > 0 || open ? label : ""}/> :
          <Input label={value.length > 0 || open ? label : ""}/>
        }
        MenuProps={MenuProps}
        placeholder={placeholder}
        labelId={`${model.id}-label`}
        open={open}
        onOpen={() => setOpen(true)}
        onClose={() => setOpen(false)}
        sx={{padding: 0, margin: 0, "& .MuiMenu-list": {padding: 0}, ...sx}}
        renderValue={(selected) => {
          if (multi) {
            if (chip) {
              return (
                <Box sx={{display: "flex", flexWrap: "wrap", gap: 0.5}}>
                  {selected.map((selected_value) => (
                    <Chip
                      color={color}
                      variant={solid ? "filled" : "outlined"}
                      key={selected_value}
                      label={selected_value}
                      onMouseDown={(event) => event.stopPropagation()}
                      onDelete={delete_button ? (event) => {
                        setValue(value.filter(v => v !== selected_value));
                      } : undefined}
                    />
                  ))}
                </Box>
              )
            }
            return selected.join(', ')
          }
          return selected
        }}
      >
        <MenuItem
          disableGutters
          sx={{
            paddingTop: 0,
            paddingBottom: 0,
            position: 'sticky',
            pointerEvents: 'auto',
            top: 0,
            zIndex: 100,
            backgroundColor: 'background.paper',
            "&:hover": {
              backgroundColor: 'background.paper',
            },
            "&.Mui-focusVisible": {
              backgroundColor: 'background.paper',
            },
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <TextField
            sx={{ paddingTop: 0, paddingBottom: 0, zIndex: 1, "&.Mui-focused": {
              backgroundColor: 'background.paper',
            }}}
            fullWidth
            variant="filled"
            placeholder="Search..."
            value={filterStr}
            onKeyDown={(e) => {
              e.stopPropagation();
              if (e.key === 'Enter' && filterStr) {
                if (multi) {
                  const filteredValues = [...bookmarkedOptions, ...filteredOptions]
                  .filter(item => item.label.toLowerCase().includes(filterStr.toLowerCase()))
                  .map(item => item.value);
                  setValue([...new Set([...value, ...filteredValues])])
                } else {
                  setValue(filteredOptions.find(item => item.label.toLowerCase().includes(filterStr.toLowerCase())).value)
                }
              }
            }}
            onChange={(e) => {
              setFilterStr(e.target.value)
              e.stopPropagation()
            }}
            onClick={(e) => {
              e.stopPropagation()
            }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <FilterListIcon />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end" onClick={() => {
                    setFilterStr("");
                    setOpen(false)
                  }}>
                    <IconButton>
                      <ClearIcon/>
                    </IconButton>
                  </InputAdornment>
                ),
              },
            }}
          />
          {multi && (
          <Box sx={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexDirection: 'row',
              width: '100%',
              borderBottomColor: 'divider',
              borderBottomWidth: 1,
              borderBottomStyle: 'solid'
            }}
          >
            <Checkbox
              size="small"
              checked={checked}
              indeterminate={indeterminate}
              onMouseDown={(e) => {
                e.preventDefault();
                e.stopPropagation();
              }}
              onClick={(e) => {
                const filteredValues = filteredOptions.map(item => item.value)
                if (filterStr) {
                  if (!checked || indeterminate) {
                    setValue([...new Set([...value, ...filteredValues.filter(matches)])])
                    setChecked(true)
                    setIndeterminate(false)
                  } else {
                    setValue(value.filter(v => !matches(v)));
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
                e.preventDefault();
                e.stopPropagation();
              }}
            />
            <Typography
              variant="caption"
              sx={{
                  display: 'block',
                  px: 1,
                  py: 0,
                  color: 'text.secondary'
              }}
              >
              {filterStr ? (
                matched_count > 0 ? `${checked ? "Deselect" : "Select"} ${matched_count} matched items` : 'No items matched'
              ) : (
                `${checked ? "Deselect" : "Select"} ${checked ? value.length : (items.length - value.length)} items`
              )}
            </Typography>
            {filterStr && <Button
              size="small"
              variant="text"
              onClick={(e) => {
                setFilterStr("");
                e.stopPropagation();
              }}
            >
              Clear
            </Button>}
          </Box>
        )}
        </MenuItem>
        {[
          ...(bookmarkedOptions.length > 0 ? [
            ...bookmarkedOptions.map(item => ({ ...item, isBookmarked: true })),
            { isDivider: true }
          ] : []),
          ...filteredOptions.map(item => ({ ...item, isBookmarked: false }))
        ].map((item, index) => {
          if (item.isDivider) {
            return <MenuItem key={`divider-${index}`} disabled divider />
          }

          const matched = filterStr && matches(item.label)
          const { value: opt, label, isBookmarked } = item
          const handleClick = (e) => {
            if (!multi) {
              setValue(opt)
              return
            }
            const isChecked = !value.includes(opt)
            if (isChecked) {
              setValue([...value, opt])
            } else {
              setValue(value.filter(v => v !== opt))
            }
            e.stopPropagation()
          }

          return (
            <MenuItem
              key={opt}
              value={opt}
              disableGutters
              onClick={handleClick}
              data-matched={matched}
              sx={{
                backgroundColor: matched ? 'action.selected' : 'inherit',
                '&:hover': {
                  backgroundColor: matched ? 'action.selected' : 'action.hover',
                }
              }}
            >
              {multi && <Checkbox checked={value.includes(opt)} onClick={handleClick} />}
              <ListItemText primary={label} sx={{margin: 2}} />
            </MenuItem>
          )
        })}
      </Select>
    </FormControl>
  )
}
