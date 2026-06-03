import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Box from "@mui/material/Box"
import {useTheme} from "@mui/material/styles"
import {apply_flex} from "./utils"

const TABS_BASE_SX = {transition: "height 0.3s"}
const TAB_CLOSE_LABEL_SX = {display: "flex", alignItems: "center"}
const TAB_CLOSE_ICON_SX = {ml: 1, cursor: "pointer", "&:hover": {opacity: 0.7}}
const TABS_PANEL_BASE_SX = {height: "100%", maxWidth: "100%", position: "relative"}
const TABS_CONTENT_BASE_SX = {
  flex: 1,
  minWidth: 0,
  display: "flex",
  flexDirection: "column",
  overflow: "auto",
  position: "relative",
  width: "100%",
  opacity: 1,
}

export function render({model, view}) {
  const [active, setActive] = model.useState("active")
  const [centered] = model.useState("centered")
  const [closable] = model.useState("closable")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [location] = model.useState("tabs_location")
  const [names] = model.useState("_names")
  const [sx] = model.useState("sx")
  const [wrapped] = model.useState("wrapped")
  const headers = model.get_child("_headers")
  const objects = model.get_child("objects")

  const theme = useTheme()

  const handleChange = (event, newValue) => {
    setActive(newValue)
  }

  const orientation = (location === "above" || location === "below") ? "horizontal" : "vertical"
  const paletteEntry = theme.palette[color] || theme.palette.primary
  const disabledList = Array.isArray(disabled) ? disabled : []
  const activeIndex = Number.isInteger(active) && active >= 0 && active < objects.length ? active : 0
  const panelSx = React.useMemo(() => {
    return ({
      ...TABS_PANEL_BASE_SX,
      ...{display: objects.length === 0 ? "none" : "flex"},
      ...{flexDirection: (location === "left" || location === "right") ? "row" : "column"},
    })
  }, [objects.length, location])
  const contentSx = React.useMemo(() => [
    TABS_CONTENT_BASE_SX,
    {minHeight: 0},
    {transition: theme.transitions.create(["opacity", "min-height"], {
      duration: theme.transitions.duration.short,
      easing: theme.transitions.easing.easeInOut
    })}
  ], [theme.transitions])

  const handleClose = React.useCallback((event, index) => {
    event.stopPropagation()
    const objId = view.model.data.objects[index].id
    let newActive = active
    if (index < active) {
      newActive = active - 1
    } else if (index === active && active >= objects.length - 1) {
      newActive = Math.max(0, objects.length - 2)
    }
    if (newActive !== active) {
      setActive(newActive)
    }
    model.send_msg({type: "close", id: objId})
  }, [active, objects.length, setActive, model, view.model.data])

  const tabLabels = React.useMemo(() => (
    names.map((label, index) => (
      <Tab
        key={index}
        disabled={disabledList.includes(index)}
        label={
          closable ? (
            <Box sx={TAB_CLOSE_LABEL_SX}>
              {label ? <span dangerouslySetInnerHTML={{__html: label}} />: headers[index]}
              <Box
                component="span"
                sx={TAB_CLOSE_ICON_SX}
                onClick={(e) => handleClose(e, index)}
              >
                ✕
              </Box>
            </Box>
          ) : (label ? <span dangerouslySetInnerHTML={{__html: label}} /> : headers[index])
        }
        wrapped={wrapped}
      />
    ))
  ), [names, disabledList, closable, headers, handleClose, wrapped])

  const tabs = (
    <Tabs
      centered={centered}
      indicatorColor={color}
      textColor={color}
      value={active}
      onChange={handleChange}
      orientation={orientation}
      scrollButtons="auto"
      slotProps={{
        indicator: {
          sx: {
            backgroundColor: paletteEntry.main,
            ...(location === "right" && {left: 0, right: "auto", width: 3}),
            ...(location === "bottom" && {top: 0, bottom: "auto", height: 3}),
          },
        }
      }}
      sx={TABS_BASE_SX}
      variant="scrollable"
    >
      {tabLabels}
    </Tabs>
  )
  const content = objects.length === 0 ? null : (
    apply_flex(view.get_child_view(model.objects[activeIndex]), "column") || objects[activeIndex]
  )

  return (
    <Box
      className="MuiTabsPanel"
      sx={{...panelSx, ...sx}}
    >
      { (location === "left" || location === "above") && tabs }
      <Box
        sx={contentSx}
      >
        {content}
      </Box>
      { (location === "right" || location === "below") && tabs }
    </Box>
  );
}
