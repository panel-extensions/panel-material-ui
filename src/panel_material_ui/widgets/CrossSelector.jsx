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

function not(a, b) {
  return a.filter((value) => !b.includes(value))
}

function intersection(a, b) {
  return a.filter((value) => b.includes(value))
}

function union(a, b) {
  return [...a, ...not(b, a)]
}

export function render({model, el}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [label] = model.useState("label")
  const [options] = model.useState("options")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")
  const [searchable] = model.useState("searchable")

  // CrossSelector specific props
  const [left_title] = ["Choices"]
  const [right_title] = ["Chosen"]
  const [left_filter, setLeftFilter] = React.useState("")
  const [right_filter, setRightFilter] = React.useState("")

  const [checked, setChecked] = React.useState([])

  // Process options to get available and selected items
  const processOptions = () => {
    if (Array.isArray(options)) {
      return options.map((opt) => {
        const option = options.find((o) => (Array.isArray(o) ? o[0] === opt : o === opt))
        const optionValue = Array.isArray(option) ? option[1] : option
        const optionLabel = Array.isArray(option) ? option[0] : option
        return {value: optionValue, label: optionLabel}
      })
    }
    return []
  }

  const allOptions = processOptions()
  const selectedValues = Array.isArray(value) ? value : []
  const availableValues = allOptions.filter(opt => !selectedValues.includes(opt.value))
  const selectedOptions = allOptions.filter(opt => selectedValues.includes(opt.value))

  // Filter options based on search
  const filterOptions = (options, filterStr) => {
    if (!filterStr) { return options }
    return options.filter(opt =>
      opt.label.toLowerCase().includes(filterStr.toLowerCase())
    )
  }

  const filteredAvailable = filterOptions(availableValues, left_filter)
  const filteredSelected = filterOptions(selectedOptions, right_filter)

  const leftChecked = intersection(checked, filteredAvailable.map(opt => opt.value))
  const rightChecked = intersection(checked, filteredSelected.map(opt => opt.value))

  const handleToggle = (value) => () => {
    const currentIndex = checked.indexOf(value)
    const newChecked = [...checked]

    if (currentIndex === -1) {
      newChecked.push(value)
    } else {
      newChecked.splice(currentIndex, 1)
    }

    setChecked(newChecked)
  }

  const numberOfChecked = (items) => intersection(checked, items.map(opt => opt.value)).length

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
    <Card sx={{height: "100%"}}>
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
            inputProps={{
              "aria-label": "all items selected",
            }}
          />
        }
        title={title}
        subheader={`${numberOfChecked(items)}/${items.length} selected`}
      />
      {searchable && (
        <TextField
          color={color}
          size="small"
          variant="outlined"
          placeholder="Search..."
          fullWidth
          sx={{p: "0 0.8em 0.5em"}}
          value={filterStr}
          onChange={(e) => setFilterStr(e.target.value)}
          InputProps={{
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
                  size="small"
                  onClick={() => setFilterStr("")}
                  sx={{isibility: filterStr ? "visible" : "hidden"}}
                >
                  <ClearIcon />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      )}
      <Divider />
      <List
        sx={{
          bgcolor: "background.paper",
          overflow: "auto",
        }}
        dense
        component="div"
        role="list"
      >
        {items.map((item) => {
          const labelId = `transfer-list-all-item-${item.value}-label`

          return (
            <ListItemButton
              key={item.value}
              role="listitem"
              onClick={handleToggle(item.value)}
              sx={{p: "0 4px 0 0"}}
            >
              <ListItemIcon>
                <Checkbox
                  color={color}
                  checked={checked.includes(item.value)}
                  tabIndex={-1}
                  disableRipple
                  inputProps={{
                    "aria-labelledby": labelId,
                  }}
                />
              </ListItemIcon>
              <ListItemText id={labelId} primary={item.label} />
            </ListItemButton>
          )
        })}
      </List>
    </Card>
  )

  return (
    <Box sx={{display: "flex", flexDirection: "column", gap: "0.5em", ...sx}}>
      {label && <InputLabel>{label}</InputLabel>}
      <Box sx={{display: "flex", flexDirection: "row", justifyContent: "center"}}>
        {customList(left_title, filteredAvailable, left_filter, setLeftFilter)}
        <Box sx={{display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", p: "0 1em"}}>
          <Button
            sx={{my: 0.5}}
            variant="outlined"
            size="small"
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
            size="small"
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
