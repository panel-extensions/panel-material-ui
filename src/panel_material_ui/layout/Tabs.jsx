import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Box from "@mui/material/Box"
import {useTheme} from "@mui/material/styles"
import {apply_flex} from "./utils"

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
  const objects = model.get_child("objects")

  const theme = useTheme()

  const handleChange = (event, newValue) => {
    setActive(newValue);
  };

  const orientation = (location === "above" || location === "below") ? "horizontal" : "vertical"

  const handleClose = (event, index) => {
    event.stopPropagation()
    if (index === active && index > objects.length - 2) {
      setActive(Math.max(0, objects.length - 2))
    }
    const newObjects = [...view.model.data.objects]
    newObjects.splice(index, 1)
    view.model.data.setv({objects: newObjects})
  }

  const tabs = (
    <Tabs
      centered={centered}
      indicatorColor={color}
      textColor={color}
      value={active}
      onChange={handleChange}
      orientation={orientation}
      scrollButtons="auto"
      TabIndicatorProps={{
        sx: {
          backgroundColor: theme.palette[color].main,
          ...(location === "right" && {left: 0, right: "auto", width: 3}),
          ...(location === "bottom" && {top: 0, bottom: "auto", height: 3}),
        },
      }}
      sx={{transition: "height 0.3s", ...sx}}
      variant="scrollable"
    >
      {names.map((label, index) => (
        <Tab
          key={index}
          disabled={disabled.includes(index)}
          label={
            closable ? (
              <Box sx={{display: "flex", alignItems: "center"}}>
                <span dangerouslySetInnerHTML={{__html: label}} />
                <Box
                  component="span"
                  sx={{
                    ml: 1,
                    cursor: "pointer",
                    "&:hover": {opacity: 0.7}
                  }}
                  onClick={(e) => handleClose(e, index)}
                >
                  ✕
                </Box>
              </Box>
            ) : label
          }
          wrapped={wrapped}
        />
      ))}
    </Tabs>
  )
  return (
    <Box className="MuiTabsPanel" sx={{display: "flex", flexDirection: (location === "left" || location === "right") ? "row" : "column", height: "100%", maxWidth: "100%"}}  >
      { (location === "left" || location === "above") && tabs }
      {apply_flex(view.get_child_view(model.objects[active]), "column") || objects[active]}
      { (location === "right" || location === "below") && tabs }
    </Box>
  );
}
