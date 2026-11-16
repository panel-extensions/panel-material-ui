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
import FormHelperText from "@mui/material/FormHelperText"
import InputLabel from "@mui/material/InputLabel"
import Select from "@mui/material/Select"
import OutlinedInput from "@mui/material/OutlinedInput"
import FilledInput from "@mui/material/FilledInput"
import Input from "@mui/material/Input"
import Typography from "@mui/material/Typography"
import ListSubheader from "@mui/material/ListSubheader"
import {DESCRIPTION_LABEL_SPACER, render_description} from "./description"
import {CustomMenu, detect_nb} from "./menu"
import {render_icon_text, render_icon_text_as_string, MUI_SIZE, denseSx, denseInputLabelSx, overlay_container} from "./utils"

const SELECT_BASE_SX = {padding: 0, margin: 0, "& .MuiMenu-list": {padding: 0}}

// Rendering a MenuItem per option makes searchable menus with thousands of
// options slow to open and to type into, so they render in pages of this size.
const MENU_PAGE_SIZE = 200

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [helper_text] = model.useState("helper_text")
  const [label] = model.useState("label")
  const [options] = model.useState("options")
  const [sx] = model.useState("sx")
  // MultiChoice inherits MultiSelect's integer `size` (visible rows), so its MUI size lives in `visual_size`
  const [size] = model.useState(model.esm_constants.multi ? "visual_size" : "size")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")
  const selectSx = React.useMemo(() => (sx ? [SELECT_BASE_SX, sx] : SELECT_BASE_SX), [sx])

  const ref = React.useRef(null)
  React.useEffect(() => {
    const focus_cb = () => ref.current?.focus()
    model.on("msg:custom", focus_cb)
    return () => model.off("msg:custom", focus_cb)
  }, [])

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
  let option_limit = null
  let search_option_limit = null
  if (multi) {
    const [chip_state] = model.useState("chip")
    const [delete_button_state] = model.useState("delete_button")
    const [max_items_state] = model.useState("max_items")
    const [placeholder_state] = model.useState("placeholder")
    const [solid_state] = model.useState("solid")
    const [option_limit_state] = model.useState("option_limit")
    const [search_option_limit_state] = model.useState("search_option_limit")
    chip = chip_state === undefined ? true : chip_state
    delete_button = delete_button_state === undefined ? true : delete_button_state
    max_items = max_items_state === undefined ? null : max_items_state
    solid = solid_state === undefined ? true : solid_state
    placeholder = placeholder_state === undefined ? null : placeholder_state
    option_limit = option_limit_state ?? null
    search_option_limit = search_option_limit_state ?? null
  }

  // Select specific props
  const [disabled_options] = model.useState("disabled_options", [])

  const allOptions = React.useMemo(() => {
    const toItem = (value, label, group) => ({value, label, group, search: String(label).toLowerCase()})
    if (Array.isArray(options)) {
      return options.map((option) => (
        Array.isArray(option) ? toItem(option[1], option[0]) : toItem(option, option)
      ))
    }
    if (options && typeof options === "object") {
      // Grouped options arrive as Panel's (str(value), label) pairs, but the
      // model value is the label, so the label serves as both.
      return Object.entries(options).flatMap(([group, groupOptions]) => (
        groupOptions.map((option) => {
          const label = Array.isArray(option) ? option[1] : option
          return toItem(label, label, group)
        })
      ))
    }
    return []
  }, [options])

  const valueSet = React.useMemo(() => new Set(multi && Array.isArray(value) ? value : []), [value])
  const bookmarkSet = React.useMemo(() => new Set(bookmarks || []), [bookmarks])
  const disabledSet = React.useMemo(() => new Set(disabled_options || []), [disabled_options])

  const filterLower = filterStr.toLowerCase()
  const matches = (item) => item.search.includes(filterLower)

  const menuRef = React.useRef(null)

  const {items, bookmarkedOptions, filteredOptions, matchedOptions} = React.useMemo(() => {
    const items = allOptions.filter((item) => (
      (!filter_on_search || filterStr === "" || matches(item)) &&
      (!multi || searchable || !valueSet.has(item.value))
    ))
    const bookmarkedOptions = []
    const filteredOptions = []
    for (const item of items) {
      (bookmarkSet.has(item.value) ? bookmarkedOptions : filteredOptions).push(item)
    }
    const matchedOptions = multi ? [...bookmarkedOptions, ...filteredOptions].filter(matches) : []
    return {items, bookmarkedOptions, filteredOptions, matchedOptions}
  }, [allOptions, filterStr, filter_on_search, searchable, valueSet, bookmarkSet])

  const matched_count = matchedOptions.length

  // Select-all checkbox state for multi-select
  const [checked, indeterminate] = React.useMemo(() => {
    if (!multi || filteredOptions.length === 0) {
      return [false, false]
    }
    const pool = filterStr ? matchedOptions : filteredOptions
    let selected = 0
    for (const item of pool) {
      if (valueSet.has(item.value)) { selected++ }
    }
    return [selected === pool.length, selected > 0 && selected < pool.length]
  }, [filteredOptions, matchedOptions, valueSet, filterStr])

  // The rendered page count resets whenever the menu reopens or the search changes
  const pageKey = `${open}|${filterStr}`
  const [pageState, setPageState] = React.useState({key: pageKey, pages: 1})
  const pages = pageState.key === pageKey ? pageState.pages : 1

  let pageSize = searchable ? MENU_PAGE_SIZE : Infinity
  const user_limit = filterStr ? (search_option_limit ?? option_limit) : option_limit
  if (user_limit != null) {
    pageSize = user_limit
  }
  let renderLimit = pageSize * pages
  if (!filter_on_search && filterStr && renderLimit < items.length) {
    // In highlight mode the first match must be rendered so it can be scrolled to
    const ordered = [...bookmarkedOptions, ...filteredOptions]
    const firstMatch = ordered.findIndex(matches)
    if (firstMatch >= renderLimit) {
      renderLimit = firstMatch + 1
    }
  }
  const visibleBookmarked = bookmarkedOptions.slice(0, renderLimit)
  const visibleFiltered = filteredOptions.slice(0, Math.max(renderLimit - visibleBookmarked.length, 0))
  const hiddenCount = items.length - visibleBookmarked.length - visibleFiltered.length

  React.useEffect(() => {
    if (!multi && filterStr && menuRef.current) {
      const matchedElement = menuRef.current.querySelector('[data-matched="true"]')
      if (matchedElement) {
        matchedElement.scrollIntoView({block: "nearest"})
      }
    }
  }, [filterStr])

  const nb = detect_nb(view)

  const MenuProps = nb ? {} : {
    container: overlay_container(el),
    sx: {height: dropdown_height},
    slotProps: {
      list: {
        ref: menuRef,
      }
    }
  }

  // The floating label/notch legend is a string-only slot, so tokens are stripped
  const label_text = render_icon_text_as_string(label)
  const label_spacer = label_text ? `${label_text}${model.description ? DESCRIPTION_LABEL_SPACER : ""}` : null

  const hasValue = multi
    ? Array.isArray(value) && value.length > 0
    : value !== "" && value != null;

  const getInput = () => {
    const inputProps = {
      id: "select-input",
      label: label_spacer,
      inputRef: ref,
      color,
    }
    switch (variant) {
      case "outlined":
        return <OutlinedInput notched={hasValue || open} {...inputProps} />
      case "filled":
        return <FilledInput {...inputProps} />
      default:
        return <Input {...inputProps} />
    }
  }

  const renderSeparated = (values) => (
    <>
      {values.map((item, index) => (
        <React.Fragment key={`${item}-${index}`}>
          {index > 0 ? ", " : ""}
          {render_icon_text(item)}
        </React.Fragment>
      ))}
    </>
  )

  const renderValue = (selected) => {
    if (multi && placeholder && selected.length === 0) {
      return render_icon_text(placeholder)
    } else if (value_label) {
      return render_icon_text(value_label)
    }
    if (multi && chip) {
      return (
        <Box sx={{display: "flex", flexWrap: "wrap", gap: 0.5, alignContent: "flex-start"}}>
          {selected.map((selected_value) => (
            <Chip
              color={color}
              variant={solid ? "filled" : "outlined"}
              key={selected_value}
              label={render_icon_text(selected_value)}
              onMouseDown={(event) => event.stopPropagation()}
              onDelete={delete_button ? () => {
                setValue(value.filter(v => v !== selected_value))
              } : undefined}
            />
          ))}
        </Box>
      )
    }
    return multi ? renderSeparated(selected) : render_icon_text(selected)
  }

  const renderMenuItems = () => {
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
                  const filteredValues = matchedOptions.map(item => item.value)
                  const newValues = [...new Set([...value, ...filteredValues])]
                  setValue(max_items ? newValues.slice(0, max_items) : newValues)
                } else {
                  const match = [...bookmarkedOptions, ...filteredOptions].find(item => (
                    matches(item) && !disabledSet.has(item.value)
                  ))
                  if (match) {
                    setValue(match.value)
                  }
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
                    size="small"
                    sx={{zIndex: 100}}
                  >
                    <IconButton size="small">
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
                  if (filterStr) {
                    const matchedValues = matchedOptions.map(item => item.value)
                    if (!checked || indeterminate) {
                      setValue([...new Set([...value, ...matchedValues])])
                    } else {
                      const matchedSet = new Set(matchedValues)
                      setValue(value.filter(v => !matchedSet.has(v)))
                    }
                  } else {
                    if (!checked || indeterminate) {
                      setValue(filteredOptions.map(item => item.value))
                    } else {
                      setValue([])
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
        {(bookmarkedOptions.length === 0 && filteredOptions.length === 0) ? (
          <MenuItem disabled>
            <ListItemText primary="No choices to choose from" />
          </MenuItem>
        ) : (
          [
            ...(visibleBookmarked.length > 0
              ? [...visibleBookmarked.map(item => ({...item, isBookmarked: true})), {isDivider: true}]
              : []),
            ...visibleFiltered.flatMap((item, index) => {
              const entry = {...item, isBookmarked: false}
              const newGroup = item.group !== undefined && item.group !== visibleFiltered[index - 1]?.group
              return newGroup ? [{isHeader: true, group: item.group}, entry] : [entry]
            })
          ].map((item, index) => {
            if (item.isDivider) {
              return <MenuItem key={`divider-${index}`} disabled divider />;
            }
            if (item.isHeader) {
              return <ListSubheader key={`${item.group}-header`}>{render_icon_text(item.group)}</ListSubheader>
            }

            const matched = filterStr && matches(item);
            const {value: opt, label} = item;

            const handleClick = (e) => {
              if (!multi) {
                setValue(opt);
                setOpen(false);
                e.stopPropagation();
                return;
              }
              const isChecked = !valueSet.has(opt);
              if (isChecked) {
                if (max_items && value.length >= max_items) {
                  setValue([...value.slice(1), opt]);
                } else {
                  setValue([...value, opt]);
                }
              } else {
                setValue(value.filter(v => v !== opt));
              }
              e.stopPropagation();
            };

            return (
              <MenuItem
                data-matched={matched}
                disabled={disabledSet.has(opt)}
                disableGutters
                key={opt}
                onClick={handleClick}
                sx={{
                  backgroundColor: matched ? "action.selected" : "inherit",
                  "&:hover": {backgroundColor: matched ? "action.selected" : "action.hover"}
                }}
                value={opt}
              >
                {multi && searchable && (
                  <Checkbox color={color} checked={valueSet.has(opt)} onClick={handleClick} />
                )}
                <ListItemText primary={render_icon_text(label)} sx={{margin: 2}} />
              </MenuItem>
            );
          }).concat(hiddenCount > 0 ? [
            <MenuItem
              className="select-more-options"
              key="__more_options__"
              onClick={(e) => {
                setPageState({key: pageKey, pages: pages + 1})
                e.stopPropagation()
              }}
            >
              <ListItemText
                secondary={`${hiddenCount} more option${hiddenCount === 1 ? "" : "s"}; ${searchable ? "refine the search or " : ""}click to show more`}
                sx={{margin: 2}}
              />
            </MenuItem>
          ] : [])
        )}
      </>
    )
  }

  const anchorEl = React.useRef(null)

  const multiChipSx = React.useMemo(() => {
    if (!multi || !chip) { return selectSx }
    return [
      ...Array.isArray(selectSx) ? selectSx : [selectSx],
      {
        height: "100%",
        "& .MuiSelect-select": {overflow: "hidden auto !important", height: "100% !important", boxSizing: "border-box", alignItems: "flex-start"},
      },
    ]
  }, [selectSx, multi, chip])

  return (
    <FormControl
      disabled={disabled}
      error={error_state}
      fullWidth
      size={MUI_SIZE(size)}
      variant={variant}
      sx={multi && chip ? {height: "100%"} : undefined}
    >
      {label &&
       <InputLabel
         color={color}
         id={`select-label-${model.id}`}
         shrink={hasValue || open}
         sx={denseInputLabelSx(size, multi && chip && variant === "outlined" ? {backgroundColor: "background.paper", px: 0.5, zIndex: 1} : undefined)}
       >
         {render_icon_text(label)}
         {model.description ? render_description({model, el, view}) : null}
       </InputLabel>
      }
      <Select
        color={color}
        disabled={disabled}
        input={getInput()}
        label={label_text}
        labelId={`select-label-${model.id}`}
        multiple={multi}
        onChange={(event) => {
          const newValue = event.target.value
          if (multi && max_items && newValue.length > max_items) {
            return
          }
          setValue(newValue)
        }}
        onClick={() => setOpen(true)}
        onClose={(e) => { e.stopPropagation(); setOpen(false) }}
        open={!nb && open}
        // With a controlled `open` MUI reads the anchor's clientWidth on every
        // render, closed or not, forcing a page reflow per Select as a page
        // mounts. Measure only while open and let autoWidth skip MUI's read.
        autoWidth
        MenuProps={{slotProps: {paper: {style: {minWidth: open ? anchorEl.current?.clientWidth : undefined}}}}}
        ref={anchorEl}
        renderValue={renderValue}
        size={MUI_SIZE(size)}
        sx={size === "large" ? denseSx(size, multiChipSx) : multiChipSx}
        value={value}
        variant={variant}

      >
        {!nb && renderMenuItems()}
      </Select>
      {nb && (
        <CustomMenu
          anchorEl={() => anchorEl.current}
          open={open}
          onClose={() => setOpen(false)}
          ref={menuRef}
          sx={{maxHeight: dropdown_height}}
          view={view}
        >
          {renderMenuItems()}
        </CustomMenu>
      )}
      {helper_text && <FormHelperText>{render_icon_text(helper_text)}</FormHelperText>}
    </FormControl>
  )
}
