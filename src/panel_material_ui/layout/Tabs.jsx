import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Box from "@mui/material/Box"
import {useTheme} from "@mui/material/styles"

export function render({model, view}) {
  const [active, setActive] = model.useState("active")
  const [centered] = model.useState("centered")
  const [closable] = model.useState("closable")
  const [color] = model.useState("color")
  const [location] = model.useState("tabs_location")
  const [names] = model.useState("_names")
  const [sx] = model.useState("sx")
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
      variant="scrollable"
      scrollButtons="auto"
      TabIndicatorProps={{style: {backgroundColor: theme.palette[color].main}}}
      sx={{transition: "height 0.3s", ...sx}}
    >
      {names.map((label, index) => (
        <Tab
          key={index}
          label={
            closable ? (
              <Box sx={{display: "flex", alignItems: "center"}}>
                {label}
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
        />
      ))}
    </Tabs>
  )
  return (
    <Box sx={{display: "flex", flexDirection: (location === "left" || location === "right") ? "row" : "column", height: "100%", maxWidth: "100%"}}  >
      { (location === "left" || location === "above") && tabs }
      <Box sx={{flexGrow: 1, minWidth: 0}}>
        {objects[active]}
      </Box>
      { (location === "right" || location === "below") && tabs }
    </Box>
  );
}
