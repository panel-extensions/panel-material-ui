import Box from "@mui/material/Box"
import FormControl from "@mui/material/FormControl"
import FormLabel from "@mui/material/FormLabel"
import IconButton from "@mui/material/IconButton"
import Slider from "@mui/material/Slider"
import ToggleButton from "@mui/material/ToggleButton"
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup"
import Tooltip from "@mui/material/Tooltip"
import Typography from "@mui/material/Typography"
import AddIcon from "@mui/icons-material/Add"
import ArrowRightAltIcon from "@mui/icons-material/ArrowRightAlt"
import FastRewindIcon from "@mui/icons-material/FastRewind"
import FirstPageIcon from "@mui/icons-material/FirstPage"
import LastPageIcon from "@mui/icons-material/LastPage"
import PauseIcon from "@mui/icons-material/Pause"
import PlayArrowIcon from "@mui/icons-material/PlayArrow"
import RemoveIcon from "@mui/icons-material/Remove"
import RepeatIcon from "@mui/icons-material/Repeat"
import SkipNextIcon from "@mui/icons-material/SkipNext"
import SkipPreviousIcon from "@mui/icons-material/SkipPrevious"
import SyncAltIcon from "@mui/icons-material/SyncAlt"
import {render_description} from "./description"
import {render_icon_text, render_icon_text_as_string} from "./utils"

const BUTTON_ORDER = [
  "slower", "first", "previous", "reverse", "pause", "play", "next", "last", "faster"
]

const BUTTON_ICONS = {
  slower: RemoveIcon,
  first: FirstPageIcon,
  previous: SkipPreviousIcon,
  reverse: FastRewindIcon,
  pause: PauseIcon,
  play: PlayArrowIcon,
  next: SkipNextIcon,
  last: LastPageIcon,
  faster: AddIcon,
}

const BUTTON_TITLES = {
  slower: "Slower",
  first: "First frame",
  previous: "Previous frame",
  reverse: "Reverse",
  pause: "Pause",
  play: "Play",
  next: "Next frame",
  last: "Last frame",
  faster: "Faster",
}

const LOOP_ORDER = ["once", "loop", "reflect"]

const LOOP_ICONS = {
  once: ArrowRightAltIcon,
  loop: RepeatIcon,
  reflect: SyncAltIcon,
}

const LOOP_TITLES = {
  once: "Once",
  loop: "Loop",
  reflect: "Reflect",
}

// Multipliers matching the MUI IconButton size scale, in rem and px respectively.
const ICON_SIZES = {small: 1.25, medium: 1.5, large: 1.75}
const BUTTON_PADDING = {small: 5, medium: 8, large: 12}

// The classic player scales the interval by this factor on each speed change.
const SPEED_FACTOR = 0.7

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [direction, setDirection] = model.useState("direction")
  const [disabled] = model.useState("disabled")
  const [frame_interval, setFrameInterval] = model.useState("interval")
  const [label] = model.useState("label")
  const [loop_policy, setLoopPolicy] = model.useState("loop_policy")
  const [preview_duration] = model.useState("preview_duration")
  const [scale_buttons] = model.useState("scale_buttons")
  const [show_loop_controls] = model.useState("show_loop_controls")
  const [show_value] = model.useState("show_value")
  const [size] = model.useState("size")
  const [step] = model.useState("step")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [, setValueThrottled] = model.useState("value_throttled")
  const [value_align] = model.useState("value_align")
  const [variant] = model.useState("variant")
  const [visible_buttons] = model.useState("visible_buttons")
  const [visible_loop_options] = model.useState("visible_loop_options")

  const discrete = model.esm_constants.discrete

  let start
  let end
  let options = null
  if (discrete) {
    const [options_state] = model.useState("options")
    options = options_state === undefined ? [] : options_state
    start = 0
    end = Math.max(options.length - 1, 0)
  } else {
    const [start_state] = model.useState("start")
    const [end_state] = model.useState("end")
    start = start_state
    end = end_state
  }

  // The interval callback reads the current frame from a ref so that the
  // timer only has to be recreated when the direction or the speed change.
  const valueRef = React.useRef(value)
  React.useEffect(() => { valueRef.current = value }, [value])

  const set_frame = React.useCallback((frame, throttled = true) => {
    const clamped = Math.min(end, Math.max(start, frame))
    valueRef.current = clamped
    setValue(clamped)
    if (throttled) {
      setValueThrottled(clamped)
    }
  }, [start, end, setValue, setValueThrottled])

  React.useEffect(() => {
    if (disabled || direction === 0) {
      return
    }
    const forward = direction > 0
    const timer = window.setInterval(() => {
      const current = valueRef.current
      if (forward ? current < end : current > start) {
        set_frame(current + (forward ? step : -step))
      } else if (loop_policy === "loop") {
        set_frame(forward ? start : end)
      } else if (loop_policy === "reflect") {
        set_frame(forward ? end : start)
        setDirection(forward ? -1 : 1)
      } else {
        set_frame(forward ? end : start)
        setDirection(0)
      }
    }, frame_interval)
    return () => window.clearInterval(timer)
  }, [direction, disabled, frame_interval, loop_policy, start, end, step, set_frame, setDirection])

  const [fps_preview, setFpsPreview] = React.useState(null)
  const preview_timer = React.useRef(null)
  React.useEffect(() => () => window.clearTimeout(preview_timer.current), [])

  const change_speed = (button, factor) => {
    const new_interval = Math.max(Math.round(frame_interval * factor), 1)
    setFrameInterval(new_interval)
    setFpsPreview({button, fps: 1000 / new_interval})
    window.clearTimeout(preview_timer.current)
    if (preview_duration > 0) {
      preview_timer.current = window.setTimeout(() => setFpsPreview(null), preview_duration)
    }
  }

  const actions = {
    slower: () => change_speed("slower", 1 / SPEED_FACTOR),
    first: () => set_frame(start),
    previous: () => set_frame(value - step),
    reverse: () => setDirection(-1),
    pause: () => setDirection(0),
    play: () => setDirection(1),
    next: () => set_frame(value + step),
    last: () => set_frame(end),
    faster: () => change_speed("faster", SPEED_FACTOR),
  }

  const active = {reverse: direction === -1, pause: direction === 0, play: direction === 1}

  const buttonSx = React.useMemo(() => ({
    p: `${BUTTON_PADDING[size] * scale_buttons}px`,
    // Pinned so that the fps preview on the speed buttons does not reflow the row.
    minWidth: `${(ICON_SIZES[size] * 16 + BUTTON_PADDING[size] * 2) * scale_buttons}px`,
    "& .MuiSvgIcon-root": {fontSize: `${ICON_SIZES[size] * scale_buttons}rem`},
  }), [size, scale_buttons])

  const value_label = discrete ? (options[value] ?? "") : `${value}`
  const position_label = discrete ? value_label : `${value} / ${end}`

  const render_button = (name) => {
    const Icon = BUTTON_ICONS[name]
    const preview = fps_preview && fps_preview.button === name
    return (
      <Tooltip key={name} title={BUTTON_TITLES[name]}>
        <span style={{display: "inline-flex"}}>
          <IconButton
            aria-label={BUTTON_TITLES[name]}
            className={name}
            color={active[name] ? color : "default"}
            disabled={disabled}
            onClick={actions[name]}
            size={size}
            sx={buttonSx}
          >
            {preview ? (
              <Typography component="span" sx={{fontSize: `${0.6 * scale_buttons}rem`, lineHeight: 1, whiteSpace: "nowrap"}}>
                {fps_preview.fps.toFixed(1)}<br/>fps
              </Typography>
            ) : <Icon/>}
          </IconButton>
        </span>
      </Tooltip>
    )
  }

  const slider = (
    <Slider
      aria-label={render_icon_text_as_string(label) || "Player"}
      color={color}
      disabled={disabled}
      getAriaValueText={() => render_icon_text_as_string(value_label)}
      max={end}
      min={start}
      onChange={(_, new_value) => { valueRef.current = new_value; setValue(new_value) }}
      onChangeCommitted={(_, new_value) => setValueThrottled(new_value)}
      size={size}
      step={1}
      sx={{flexGrow: 1, minWidth: 0}}
      value={value}
      valueLabelDisplay="off"
    />
  )

  if (variant === "minimal") {
    const playing = direction !== 0
    return (
      <FormControl disabled={disabled} fullWidth sx={sx}>
        <Box sx={{display: "flex", flexDirection: "row", alignItems: "center", gap: 1, width: "100%"}}>
          {label && (
            <Typography component="span" variant="body2" sx={{whiteSpace: "nowrap"}}>
              {render_icon_text(label)}
            </Typography>
          )}
          <Tooltip title={playing ? "Pause" : "Play"}>
            <span style={{display: "inline-flex"}}>
              <IconButton
                aria-label={playing ? "Pause" : "Play"}
                className={playing ? "pause" : "play"}
                color={playing ? color : "default"}
                disabled={disabled}
                onClick={() => setDirection(playing ? 0 : 1)}
                size={size}
                sx={buttonSx}
              >
                {playing ? <PauseIcon/> : <PlayArrowIcon/>}
              </IconButton>
            </span>
          </Tooltip>
          {slider}
          {show_value && (
            <Typography component="span" variant="body2" sx={{whiteSpace: "nowrap"}}>
              {render_icon_text(position_label)}
            </Typography>
          )}
          {model.description && render_description({model, el, view})}
        </Box>
      </FormControl>
    )
  }

  const buttons = BUTTON_ORDER.filter((name) => visible_buttons.includes(name))
  const loop_options = LOOP_ORDER.filter((name) => visible_loop_options.includes(name))
  const show_header = Boolean(label) || show_value || Boolean(model.description)

  return (
    <FormControl disabled={disabled} fullWidth sx={sx}>
      {show_header && (
        <FormLabel sx={{textAlign: value_align, overflowWrap: "break-word", whiteSpace: "normal"}}>
          {label && <>{render_icon_text(label)}{show_value && ": "}</>}
          {show_value && <strong>{render_icon_text(value_label)}</strong>}
          {model.description && render_description({model, el, view})}
        </FormLabel>
      )}
      <Box sx={{display: "flex", flexDirection: "row", alignItems: "center", width: "100%"}}>
        {slider}
      </Box>
      <Box sx={{display: "flex", flexDirection: "row", alignItems: "center", justifyContent: "center", flexWrap: "wrap"}}>
        {buttons.map(render_button)}
      </Box>
      {show_loop_controls && loop_options.length > 0 && (
        <Box sx={{display: "flex", flexDirection: "row", justifyContent: "center"}}>
          <ToggleButtonGroup
            aria-label="Loop policy"
            color={color}
            disabled={disabled}
            exclusive
            onChange={(_, new_policy) => new_policy != null && setLoopPolicy(new_policy)}
            size="small"
            value={loop_policy}
          >
            {loop_options.map((name) => {
              const Icon = LOOP_ICONS[name]
              return (
                <Tooltip key={name} title={LOOP_TITLES[name]}>
                  <ToggleButton
                    aria-label={LOOP_TITLES[name]}
                    className={name}
                    disabled={disabled}
                    value={name}
                    sx={{p: `${BUTTON_PADDING[size] * scale_buttons}px`}}
                  >
                    <Icon sx={{fontSize: `${ICON_SIZES[size] * scale_buttons}rem`}}/>
                  </ToggleButton>
                </Tooltip>
              )
            })}
          </ToggleButtonGroup>
        </Box>
      )}
    </FormControl>
  )
}
