import Autocomplete from "@mui/material/Autocomplete"
import Popper from "@mui/material/Popper"
import TextField from "@mui/material/TextField"
import {render_description} from "./description"

export function render({model, el, view}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
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
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [model])

  function CustomPopper(props) {
    return <Popper {...props} container={el} />
  }

  const filter_op = (input) => {
    return (opt) => {
      if (!model.case_sensitive) {
        opt = opt.toLowerCase()
        input = input.toLowerCase()
      }
      return model.search_strategy == "includes" ? opt.includes(input) : opt.startsWith(input)
    }
  }

  const filt_func = (options, state) => {
    const input = state.inputValue
    if (input.length < model.min_characters) {
      return []
    }
    return options.filter(filter_op(input))
  }

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
  const filterOptions = lazy_search ? undefined : filt_func

  return (
    <Autocomplete
      color={color}
      disabled={disabled}
      filterOptions={filterOptions}
      freeSolo={!restrict}
      fullWidth
      inputValue={value_input || ""}
      onChange={(event, newValue) => setValue(newValue)}
      options={displayOptions}
      renderInput={(params) => (
        <TextField
          {...params}
          color={color}
          label={model.description ? <>{label}{render_description({model, el, view})}</> : label}
          inputRef={ref}
          placeholder={placeholder}
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
                const filtered = lazy_search ? filteredOptions : options.filter(filter_op(new_value))
                if (filtered.length > 0) {
                  new_value = filtered[0]
                  setValueInput(filtered[0])
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
      size={size}
      sx={sx}
      value={value}
      variant={variant}
      PopperComponent={CustomPopper}
    />
  )
}
