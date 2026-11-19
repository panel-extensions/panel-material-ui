import Autocomplete, {createFilterOptions} from "@mui/material/Autocomplete"
import InputAdornment from "@mui/material/InputAdornment"
import Paper from "@mui/material/Paper"
import Popper from "@mui/material/Popper"
import TextField from "@mui/material/TextField"
import Typography from "@mui/material/Typography"
import {render_description} from "./description"
import {parse_icon_text, render_icon_segment, render_icon_text, render_icon_text_as_string, overlay_container} from "./utils"

// Rendering an <li> per match makes broad queries against large option lists
// slow, so only this many matches are rendered and the rest are summarized.
const MAX_RENDERED_OPTIONS = 200

const defaultFilterOptions = createFilterOptions()

export function render({model, host}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [helper_text] = model.useState("helper_text")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")
  const [value_input, setValueInput] = model.useState("value_input")
  const [options] = model.useState("options")
  const [placeholder] = model.useState("placeholder")
  const [restrict] = model.useState("restrict")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const [lazy_search] = model.useState("lazy_search")

  const ref = React.useRef(null)
  const pendingQueries = React.useRef(new Map())
  const queryCounter = React.useRef(0)
  const [filteredOptions, setFilteredOptions] = React.useState(options || [])

  // Update filtered options when options change
  React.useEffect(() => {
    if (!lazy_search) {
      setFilteredOptions(options || [])
    }
  }, [options, lazy_search])

  React.useEffect(() => {
    const handler = (msg) => {
      if (msg && msg.action === "focus") {
        ref.current?.focus()
      } else if (msg && msg.type === "search_response" && msg.id !== undefined) {
        const resolver = pendingQueries.current.get(msg.id)
        if (resolver) {
          resolver(msg.options || [])
          pendingQueries.current.delete(msg.id)
        }
      }
    }
    return model.on("msg", handler)
  }, [model])

  function CustomPopper(props) {
    return <Popper {...props} container={host.overlay_root} />
  }

  const filter_op = (input) => {
    return (opt) => {
      opt = render_icon_text_as_string(opt)
      if (!model.case_sensitive) {
        opt = opt.toLowerCase()
        input = input.toLowerCase()
      }
      return model.search_strategy == "includes" ? opt.includes(input) : opt.startsWith(input)
    }
  }

  const hiddenCount = React.useRef(0)
  const limitOptions = (matched) => {
    hiddenCount.current = Math.max(matched.length - MAX_RENDERED_OPTIONS, 0)
    return hiddenCount.current ? matched.slice(0, MAX_RENDERED_OPTIONS) : matched
  }

  const filt_func = (options, state) => {
    const input = state.inputValue
    if (input.length < model.min_characters) {
      hiddenCount.current = 0
      return []
    }
    return limitOptions(options.filter(filter_op(input)))
  }

  // Mirrors MUI's AutocompletePaper styles, adding a note below the listbox when matches were cut off
  const OptionsPaper = React.useMemo(() => React.forwardRef(function OptionsPaper({children, ownerState, sx, ...props}, ref) {
    return (
      <Paper {...props} ref={ref} sx={[{typography: "body1", overflow: "auto"}, ...(Array.isArray(sx) ? sx : [sx])]}>
        {children}
        {hiddenCount.current > 0 && (
          <Typography className="autocomplete-more-options" variant="body2" sx={{color: "text.secondary", px: 2, py: 1.25}}>
            {`${hiddenCount.current} more match${hiddenCount.current === 1 ? "" : "es"}, keep typing to refine`}
          </Typography>
        )}
      </Paper>
    )
  }), [])

  // Handle input changes for lazy search
  const handleInputChange = React.useCallback(async (inputValue) => {
    if (lazy_search) {
      if (inputValue.length < model.min_characters) {
        setFilteredOptions([])
        return
      }

      // Use lazy search: send query to backend and await response
      const queryId = queryCounter.current++
      const queryPromise = new Promise((resolve) => {
        pendingQueries.current.set(queryId, resolve)
        // Timeout after 5 seconds
        setTimeout(() => {
          if (pendingQueries.current.has(queryId)) {
            pendingQueries.current.delete(queryId)
            resolve([])
          }
        }, 5000)
      })

      model.send_msg({
        type: "search",
        id: queryId,
        query: inputValue,
        case_sensitive: model.case_sensitive,
        search_strategy: model.search_strategy
      })

      const results = await queryPromise
      setFilteredOptions(results)
    }
  }, [lazy_search, model])

  // Debounce input changes for lazy search
  const debounceTimer = React.useRef(null)
  React.useEffect(() => {
    if (lazy_search && value_input !== undefined) {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
      debounceTimer.current = setTimeout(() => {
        handleInputChange(value_input || "")
      }, 300) // 300ms debounce
      return () => {
        if (debounceTimer.current) {
          clearTimeout(debounceTimer.current)
        }
      }
    }
  }, [value_input, lazy_search, handleInputChange])

  // Use filtered options for lazy search, otherwise use all options with local filtering
  const displayOptions = lazy_search ? filteredOptions : options
  const filterOptions = lazy_search ? (opts, state) => limitOptions(defaultFilterOptions(opts, state)) : filt_func
  const selectedIcon = options?.includes(value) && value_input === render_icon_text_as_string(value)
    ? parse_icon_text(value).find((segment) => segment.type === "icon") : null

  const renderOptionLabel = (option) => {
    if (typeof option === "string") {
      return render_icon_text(option)
    }
    if (typeof option === "number") {
      return option
    }
    if (option && typeof option === "object") {
      if (typeof option.label === "string") {
        return render_icon_text(option.label)
      }
      if (typeof option.value === "string") {
        return render_icon_text(option.value)
      }
    }
    return String(option ?? "")
  }

  return (
    <Autocomplete
      color={color}
      disabled={disabled}
      filterOptions={filterOptions}
      freeSolo={!restrict}
      fullWidth
      getOptionLabel={render_icon_text_as_string}
      inputValue={value_input || ""}
      onChange={(event, newValue) => setValue(newValue)}
      options={displayOptions}
      renderInput={(params) => (
        <TextField
          {...params}
          color={color}
          error={error_state}
          helperText={helper_text ? render_icon_text(helper_text) : undefined}
          label={model.description ? <>{render_icon_text(label)}{render_description({model, host})}</> : render_icon_text(label)}
          inputRef={ref}
          slotProps={{...params.slotProps, input: {
            ...params.slotProps.input,
            startAdornment: selectedIcon ? (
              <InputAdornment position="start">{render_icon_segment(selectedIcon)}</InputAdornment>
            ) : params.slotProps.input.startAdornment,
          }}}
          placeholder={render_icon_text_as_string(placeholder)}
          onChange={(event) => {
            setValueInput(event.target.value)
          }}
          onKeyDown={(event) => {
            if (restrict && ((value_input || "").length < model.min_characters)) {
              return
            } else if (event.key === "Enter") {
              let new_value = value_input
              if (restrict) {
                // Use filtered options for lazy search, otherwise filter locally
                const match = lazy_search ? filteredOptions[0] : options.find(filter_op(new_value))
                if (match !== undefined) {
                  new_value = match
                  setValueInput(match)
                } else {
                  return
                }
              }
              event.target.value = new_value
              model.send_event("enter", event)
              setValue(new_value)
            }
          }}
          size={size}
          variant={variant}
        />
      )}
      renderOption={(props, option) => (
        <li {...props}>{renderOptionLabel(option)}</li>
      )}
      size={size}
      sx={sx}
      value={value}
      variant={variant}
      slots={{
        paper: OptionsPaper,
        popper: CustomPopper
      }}
    />
  );
}
