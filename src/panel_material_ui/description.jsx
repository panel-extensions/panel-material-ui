import React from "react"
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined"
import Tooltip from "@mui/material/Tooltip"
import {ThemeProvider, useTheme} from "@mui/material/styles"
import {CacheProvider} from "@emotion/react"

export function render_description({model, el, view}) {
  const theme = useTheme()
  const [description] =  model.useState("description")

  const iconRef = React.useRef(null)
  const [open, setOpen] = React.useState(false);

  let container = el
  let cache = null
  if (view && view.root.model.class_name == "Page" && view.root.mui_cache != null) {
    container = view.root.shadow_el
    cache = view.root.mui_cache
    return (
      <>
        <InfoOutlinedIcon
          ref={iconRef}
          onMouseEnter={() => setOpen(true)}
          onMouseLeave={() => setOpen(false)}
          onFocus={() => setOpen(true)}
          onBlur={() => setOpen(false)}
          sx={{ml: "0.5em", fontSize: "0.9em"}}
        />
        <CacheProvider value={cache}>
          <ThemeProvider theme={theme}>
            <Tooltip
              title={description}
              arrow
              open={open}
              placement="right"
              slotProps={{
                popper: {
                  container,
                  anchorEl: () => iconRef.current
                }
              }}
              sx={{zIndex: 5000}}
            >
              <span />
            </Tooltip>
          </ThemeProvider>
        </CacheProvider>
      </>
    )
  }
  return (
    <Tooltip
      title={description}
      arrow
      placement="right"
      slotProps={{
        popper: {
          container
        }
      }}
      sx={{zIndex: 5000}}
    >
      <InfoOutlinedIcon sx={{ml: "0.5em", fontSize: "0.9em"}}/>
    </Tooltip>
  )
}
