import List from "@mui/material/List"
import Card from "@mui/material/Card"
import CardHeader from "@mui/material/CardHeader"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemText from "@mui/material/ListItemText"
import ListItemIcon from "@mui/material/ListItemIcon"
import Checkbox from "@mui/material/Checkbox"
import Button from "@mui/material/Button"
import Divider from "@mui/material/Divider"
import TextField from "@mui/material/TextField"
import InputAdornment from "@mui/material/InputAdornment"
import FilterListIcon from "@mui/icons-material/FilterList"
import ClearIcon from "@mui/icons-material/Clear"
import IconButton from "@mui/material/IconButton"
import KeyboardDoubleArrowLeftIcon from "@mui/icons-material/KeyboardDoubleArrowLeft"
import KeyboardDoubleArrowRightIcon from "@mui/icons-material/KeyboardDoubleArrowRight"
import InputLabel from "@mui/material/InputLabel"
import Box from "@mui/material/Box"
import {render_description} from "./description"
import {MUI_SIZE, denseSx, render_icon_text} from "./utils"

const CROSS_SELECTOR_ROOT_SX = {
  display: "flex",
  height: "100%",
  flexDirection: "column",
  gap: "0.5em"
}

function not(a, b) {
  const exclude = new Set(b)
  return a.filter((value) => !exclude.has(value))
}

function intersection(a, b) {
  const include = new Set(b)
  return a.filter((value) => include.has(value))
}

function union(a, b) {
  return [...a, ...not(b, a)]
}

// Memoized so that re-renders only touch rows whose label or checked state changed
const CrossSelectorItem = React.memo(function CrossSelectorItem({item, checked, color, visual_size, onToggle}) {
  const labelId = `transfer-list-all-item-${item.value}-label`
  return (
    <ListItemButton
      role="listitem"
      onClick={() => onToggle(item.value)}
      sx={{p: "0 4px 0 0", minWidth: 0}}
    >
      <ListItemIcon>
        <Checkbox
          color={color}
          checked={checked}
          tabIndex={-1}
          disableRipple
          size={MUI_SIZE(visual_size)}
          slotProps={{input: {"aria-labelledby": labelId}}}
        />
      </ListItemIcon>
      <ListItemText id={labelId} primary={render_icon_text(item.label)} primaryTypographyProps={{noWrap: true}} />
    </ListItemButton>
  )
})

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [label] = model.useState("label")
  const [options] = model.useState("options")
  const [definition_order] = model.useState("definition_order")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")
  const [searchable] = model.useState("searchable")
  const [size] = model.useState("size")
  const [visual_size] = model.useState("visual_size")
  const rootSx = React.useMemo(() => [CROSS_SELECTOR_ROOT_SX, denseSx(visual_size, sx)], [sx, visual_size])

  // CrossSelector specific props
  const [left_title] = ["Choices"]
  const [right_title] = ["Chosen"]
  const [left_filter, setLeftFilter] = React.useState("")
  const [right_filter, setRightFilter] = React.useState("")
  const [matches, setMatches] = React.useState({left: null, right: null})

  React.useEffect(() => {
    const handler = (msg) => {
      if (msg?.type === "filter_response") {
        const query = msg.side === "left" ? left_filter : right_filter
        if (msg.query === query) {
          setMatches(current => ({...current, [msg.side]: {query: msg.query, labels: msg.matches}}))
        }
      }
    }
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [model, left_filter, right_filter])

  React.useEffect(() => {
    if (left_filter) { model.send_msg({type: "filter", side: "left", query: left_filter}) }
    if (right_filter) { model.send_msg({type: "filter", side: "right", query: right_filter}) }
  }, [model, left_filter, right_filter, options])

  const [checked, setChecked] = React.useState([])

  const allOptions = React.useMemo(() => {
    if (!Array.isArray(options)) {
      return []
    }
    return options.map((option) => (
      Array.isArray(option) ? {value: option[1], label: option[0]} : {value: option, label: option}
    ))
  }, [options])

  const selectedValues = Array.isArray(value) ? value : []
  const [availableValues, selectedOptions] = React.useMemo(() => {
    const selectedSet = new Set(selectedValues)
    const available = allOptions.filter(opt => !selectedSet.has(opt.value))
    if (definition_order) {
      return [available, allOptions.filter(opt => selectedSet.has(opt.value))]
    }
    const byValue = new Map()
    for (const opt of allOptions) {
      if (!byValue.has(opt.value)) { byValue.set(opt.value, opt) }
    }
    return [available, selectedValues.map(selected => byValue.get(selected)).filter(Boolean)]
  }, [allOptions, value, definition_order])

  // Filter options based on search
  const filterOptions = (options, filterStr, side) => {
    if (!filterStr) { return options }
    if (matches[side]?.query !== filterStr) { return [] }
    const labels = new Set(matches[side].labels)
    return options.filter(opt => labels.has(opt.label))
  }

  const filteredAvailable = React.useMemo(
    () => filterOptions(availableValues, left_filter, "left"), [availableValues, left_filter, matches.left]
  )
  const filteredSelected = React.useMemo(
    () => filterOptions(selectedOptions, right_filter, "right"), [selectedOptions, right_filter, matches.right]
  )

  const checkedSet = React.useMemo(() => new Set(checked), [checked])
  const leftChecked = intersection(checked, filteredAvailable.map(opt => opt.value))
  const rightChecked = intersection(checked, filteredSelected.map(opt => opt.value))

  const handleToggle = React.useCallback((value) => {
    setChecked((current) => (
      current.includes(value) ? current.filter(v => v !== value) : [...current, value]
    ))
  }, [])

  const numberOfChecked = (items) => items.reduce((count, opt) => count + (checkedSet.has(opt.value) ? 1 : 0), 0)

  const handleToggleAll = (items) => () => {
    const itemValues = items.map(opt => opt.value)
    if (numberOfChecked(items) === items.length) {
      setChecked(not(checked, itemValues))
    } else {
      setChecked(union(checked, itemValues))
    }
  }

  const handleCheckedRight = () => {
    const newSelected = [...selectedValues, ...leftChecked]
    setValue(newSelected)
    setChecked(not(checked, leftChecked))
  }

  const handleCheckedLeft = () => {
    const newSelected = selectedValues.filter(v => !rightChecked.includes(v))
    setValue(newSelected)
    setChecked(not(checked, rightChecked))
  }

  const customList = (title, items, filterStr, setFilterStr) => (
    <Card sx={{flex: "1 1 0", minWidth: 0, height: "100%", overflowY: "auto"}}>
      <CardHeader
        sx={{p: "1em 0.8em 1em 0"}}
        avatar={
          <Checkbox
            color={color}
            disableRipple
            onClick={handleToggleAll(items)}
            checked={numberOfChecked(items) === items.length && items.length !== 0}
            indeterminate={
              numberOfChecked(items) !== items.length && numberOfChecked(items) !== 0
            }
            disabled={items.length === 0}
            slotProps={{
              input: {
                "aria-label": "all items selected",
              }
            }}
          />
        }
        title={render_icon_text(title)}
        subheader={`${numberOfChecked(items)}/${items.length} selected`}
      />
      {searchable && (
        <TextField
          color={color}
          size={MUI_SIZE(visual_size)}
          variant="outlined"
          placeholder="Search..."
          fullWidth
          sx={{p: "0 0.8em 0.5em"}}
          value={filterStr}
          onChange={(e) => setFilterStr(e.target.value)}
          slotProps={{
            input: {
              sx: {pl: "4px", pr: "4px"},
              startAdornment: (
                <InputAdornment position="start">
                  <FilterListIcon />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end" sx={{ml: 0}}>
                  <IconButton
                    disableRipple
                    size={MUI_SIZE(visual_size)}
                    onClick={() => setFilterStr("")}
                    sx={{visibility: filterStr ? "visible" : "hidden"}}
                  >
                    <ClearIcon />
                  </IconButton>
                </InputAdornment>
              ),
            }
          }}
        />
      )}
      <Divider />
      <List
        sx={{
          bgcolor: "background.paper",
          overflow: "auto",
          minWidth: 0,
          maxHeight: `calc((1.25rem + 18px) * ${size})`,
          pt: 0
        }}
        dense
        component="div"
        role="list"
      >
        {items.map((item) => (
          <CrossSelectorItem
            key={item.value}
            item={item}
            checked={checkedSet.has(item.value)}
            color={color}
            visual_size={visual_size}
            onToggle={handleToggle}
          />
        ))}
      </List>
    </Card>
  )

  return (
    <Box sx={rootSx}>
      {label && (
        <InputLabel>
          {render_icon_text(label)}
          {model.description ? render_description({model, el, view}) : null}
        </InputLabel>
      )}
      <Box sx={{display: "flex", flexGrow: 1, minWidth: 0, maxHeight: "calc(100% - 2em)", flexDirection: "row", justifyContent: "center", overflow: "hidden"}}>
        {customList(left_title, filteredAvailable, left_filter, setLeftFilter)}
        <Box sx={{display: "flex", flex: "0 0 auto", minWidth: 0, flexDirection: "column", alignItems: "center", justifyContent: "center", p: "0 1em"}}>
          <Button
            sx={{my: 0.5}}
            variant="outlined"
            size={MUI_SIZE(visual_size)}
            onClick={handleCheckedRight}
            disabled={leftChecked.length === 0 || disabled}
            aria-label="move selected right"
            color={color}
          >
            <KeyboardDoubleArrowRightIcon />
          </Button>
          <Button
            sx={{my: 0.5}}
            variant="outlined"
            size={MUI_SIZE(visual_size)}
            onClick={handleCheckedLeft}
            disabled={rightChecked.length === 0 || disabled}
            aria-label="move selected left"
            color={color}
          >
            <KeyboardDoubleArrowLeftIcon />
          </Button>
        </Box>
        {customList(right_title, filteredSelected, right_filter, setRightFilter)}
      </Box>
    </Box>
  )
}
