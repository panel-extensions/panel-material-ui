import {DayPicker} from "react-day-picker"
import "react-day-picker/style.css"
import TextField from "@mui/material/TextField"
import Paper from "@mui/material/Paper"
import Popper from "@mui/material/Popper"
import ClickAwayListener from "@mui/material/ClickAwayListener"
import InputAdornment from "@mui/material/InputAdornment"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import Button from "@mui/material/Button"
import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"
import {useTheme} from "@mui/material/styles"
import useMediaQuery from "@mui/material/useMediaQuery"
import dayjs from "dayjs"

function formatDate(date, format) {
  if (!date) { return "" }
  return dayjs(date).format(format)
}

function parseDateOnly(value) {
  if (!value) { return undefined }
  if (value instanceof Date) { return value }
  if (typeof value === "number") {
    const d = new Date(value)
    return new Date(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate())
  }
  if (typeof value === "string") {
    const d = dayjs(value)
    return d.isValid() ? d.toDate() : undefined
  }
  return undefined
}

function parseDatetime(value) {
  if (!value) { return undefined }
  if (value instanceof Date) { return value }
  if (typeof value === "number") {
    return new Date(value)
  }
  if (typeof value === "string") {
    const d = dayjs(value)
    return d.isValid() ? d.toDate() : undefined
  }
  return undefined
}

function pad(n) {
  return n.toString().padStart(2, "0")
}

export function render({model, el, view}) {
  const theme = useTheme()
  const [modelValue] = model.useState("value")
  const [start] = model.useState("start")
  const [end] = model.useState("end")
  const [disabled] = model.useState("disabled")
  const [format] = model.useState("format")
  const [label] = model.useState("label")
  const [color] = model.useState("color")
  const [variant] = model.useState("variant")
  const [disabled_dates] = model.useState("disabled_dates")
  const [enabled_dates] = model.useState("enabled_dates")
  const [sx] = model.useState("sx")

  const time = model.esm_constants.time

  let enableSeconds = false
  let militaryTime = true
  if (time) {
    const [_enableSeconds] = model.useState("enable_seconds")
    const [_militaryTime] = model.useState("military_time")
    enableSeconds = _enableSeconds
    militaryTime = _militaryTime
  }

  const isMobileQuery = useMediaQuery(theme.breakpoints.down("sm"))
  const mobile = isMobileQuery

  const parseDate = time ? parseDatetime : parseDateOnly

  const [open, setOpen] = React.useState(false)
  const anchorRef = React.useRef(null)

  const selected = React.useMemo(() => {
    if (!modelValue || !Array.isArray(modelValue) || modelValue.length !== 2) {
      return undefined
    }
    const from = parseDate(modelValue[0])
    const to = parseDate(modelValue[1])
    if (!from || !to) { return undefined }
    return {from, to}
  }, [modelValue])

  const [fromTime, setFromTime] = React.useState(() => {
    if (selected?.from) {
      return {h: selected.from.getHours(), m: selected.from.getMinutes(), s: selected.from.getSeconds()}
    }
    return {h: 0, m: 0, s: 0}
  })

  const [toTime, setToTime] = React.useState(() => {
    if (selected?.to) {
      return {h: selected.to.getHours(), m: selected.to.getMinutes(), s: selected.to.getSeconds()}
    }
    return {h: 23, m: 59, s: 59}
  })

  React.useEffect(() => {
    if (selected?.from) {
      setFromTime({h: selected.from.getHours(), m: selected.from.getMinutes(), s: selected.from.getSeconds()})
    }
    if (selected?.to) {
      setToTime({h: selected.to.getHours(), m: selected.to.getMinutes(), s: selected.to.getSeconds()})
    }
  }, [modelValue])

  const [month, setMonth] = React.useState(() => {
    if (selected?.from) { return selected.from }
    if (start) { return parseDate(start) }
    return new Date()
  })

  const displayValue = React.useMemo(() => {
    if (!selected) { return "" }
    return `${formatDate(selected.from, format)} – ${formatDate(selected.to, format)}`
  }, [selected, format])

  const minDate = React.useMemo(() => parseDate(start), [start])
  const maxDate = React.useMemo(() => parseDate(end), [end])

  function commitRange(range, fTime, tTime) {
    if (!range || !range.from || !range.to) { return }
    if (time) {
      const from = new Date(range.from)
      from.setHours(fTime.h, fTime.m, fTime.s)
      const to = new Date(range.to)
      to.setHours(tTime.h, tTime.m, tTime.s)
      const fromStr = dayjs(from).format("YYYY-MM-DD HH:mm:ss")
      const toStr = dayjs(to).format("YYYY-MM-DD HH:mm:ss")
      model.value = [fromStr, toStr]
    } else {
      const fromStr = dayjs(range.from).format("YYYY-MM-DD")
      const toStr = dayjs(range.to).format("YYYY-MM-DD")
      model.value = [fromStr, toStr]
    }
  }

  function shouldDisableDate(date) {
    if (enabled_dates && enabled_dates.length > 0) {
      return !inList(date, enabled_dates)
    }
    if (disabled_dates && disabled_dates.length > 0) {
      return inList(date, disabled_dates)
    }
    return false
  }

  function inList(date, list) {
    if (!list || list.length === 0) { return false }
    const dateStr = dayjs(date).format("YYYY-MM-DD")
    for (const item of list) {
      if (Array.isArray(item)) {
        const from = dayjs(parseDate(item[0]))
        const to = dayjs(parseDate(item[1]))
        const d = dayjs(date)
        if (d >= from && d <= to) { return true }
      } else {
        if (dayjs(parseDate(item)).format("YYYY-MM-DD") === dateStr) { return true }
      }
    }
    return false
  }

  const [pendingRange, setPendingRange] = React.useState(null)
  const rangeStepRef = React.useRef("start")

  const openPicker = () => {
    if (disabled) { return }
    setPendingRange(null)
    rangeStepRef.current = "start"
    setOpen(true)
  }

  const handleDayClick = (day) => {
    if (rangeStepRef.current === "start") {
      setPendingRange({from: day, to: undefined})
      rangeStepRef.current = "end"
    } else {
      const from = pendingRange?.from || day
      const range = day < from ? {from: day, to: from} : {from, to: day}
      setPendingRange(range)
      rangeStepRef.current = "start"
      if (!mobile && !time) {
        commitRange(range, fromTime, toTime)
        setPendingRange(null)
        setOpen(false)
      }
    }
  }

  const handleCancel = () => {
    setPendingRange(null)
    rangeStepRef.current = "start"
    setOpen(false)
  }

  const handleOk = () => {
    const range = pendingRange || selected
    if (range?.from && range?.to) {
      commitRange(range, fromTime, toTime)
    }
    setPendingRange(null)
    rangeStepRef.current = "start"
    setOpen(false)
  }

  const effectiveSelected = React.useMemo(() => {
    if (pendingRange) { return pendingRange }
    return selected
  }, [pendingRange, selected])

  const muiColor = theme.palette[color] || theme.palette.primary

  const dayPickerStyles = {
    "--rdp-accent-color": muiColor.main,
    "--rdp-accent-background-color": `${muiColor.main}1a`,
    "--rdp-range_middle-color": theme.palette.text.primary,
    "--rdp-range_middle-background-color": `${muiColor.main}1a`,
    "--rdp-font-family": theme.typography.fontFamily,
    "--rdp-day-font": `${theme.typography.body2.fontSize} ${theme.typography.fontFamily}`,
    "--rdp-day-height": "36px",
    "--rdp-day-width": "36px",
    "--rdp-selected-font": `bold ${theme.typography.body2.fontSize} ${theme.typography.fontFamily}`,
  }

  function TimeInput({label, value, onChange}) {
    const handleTimeChange = (e) => {
      const raw = e.target.value
      if (!raw) { return }
      const [hStr, mStr] = raw.split(":")
      const h = parseInt(hStr, 10)
      const m = parseInt(mStr, 10)
      if (!isNaN(h) && !isNaN(m)) {
        onChange({...value, h, m})
      }
    }

    return (
      <TextField
        label={label}
        type="time"
        size="small"
        value={`${pad(value.h)}:${pad(value.m)}`}
        onChange={handleTimeChange}
        slotProps={{
          input: {step: enableSeconds ? 1 : 60},
          inputLabel: {shrink: true},
        }}
        sx={{minWidth: 120}}
      />
    )
  }

  const showActionButtons = mobile || time

  return (
    <div style={{width: "100%", ...(sx || {})}}>
      <TextField
        ref={anchorRef}
        label={label}
        value={displayValue}
        onClick={openPicker}
        variant={variant}
        color={color}
        disabled={disabled}
        fullWidth
        slotProps={{
          input: {
            readOnly: true,
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  edge="end"
                  disabled={disabled}
                  onClick={(e) => {
                    e.stopPropagation()
                    if (open) { handleCancel() } else { openPicker() }
                  }}
                  size="small"
                >
                  <Icon>date_range</Icon>
                </IconButton>
              </InputAdornment>
            ),
          },
        }}
      />
      <Popper
        open={open}
        anchorEl={anchorRef.current}
        placement="bottom-start"
        container={view.container}
        style={{zIndex: theme.zIndex.modal}}
      >
        <ClickAwayListener onClickAway={handleCancel}>
          <Paper elevation={8} sx={{p: 2, mt: 0.5}}>
            <DayPicker
              mode="range"
              selected={effectiveSelected}
              onDayClick={handleDayClick}
              month={month}
              onMonthChange={setMonth}
              disabled={(date) => {
                if (minDate && date < minDate) { return true }
                if (maxDate && date > maxDate) { return true }
                return shouldDisableDate(date)
              }}
              numberOfMonths={mobile ? 1 : 2}
              style={dayPickerStyles}
            />
            {time && (
              <Box sx={{
                display: "flex",
                gap: 2,
                alignItems: "center",
                justifyContent: "center",
                pt: 1,
                borderTop: 1,
                borderColor: "divider",
                mt: 1
              }}
              >
                <TimeInput label="Start time" value={fromTime} onChange={setFromTime} />
                <Typography variant="body2" color="text.secondary">–</Typography>
                <TimeInput label="End time" value={toTime} onChange={setToTime} />
              </Box>
            )}
            {showActionButtons && (
              <Box sx={{
                display: "flex",
                justifyContent: "flex-end",
                gap: 1,
                pt: 1,
                borderTop: time ? 0 : 1,
                borderColor: "divider",
                mt: 1
              }}
              >
                <Button size="small" onClick={handleCancel}>Cancel</Button>
                <Button
                  size="small"
                  variant="text"
                  color={color}
                  onClick={handleOk}
                  disabled={!effectiveSelected?.from || !effectiveSelected?.to}
                >
                  Ok
                </Button>
              </Box>
            )}
          </Paper>
        </ClickAwayListener>
      </Popper>
    </div>
  )
}
