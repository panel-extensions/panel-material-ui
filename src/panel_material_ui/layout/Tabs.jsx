import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";

export function render({model, view}) {
  const [active, setActive] = model.useState("active");
  const [centered] = model.useState("centered");
  const [color] = model.useState("color");
  const [location] = model.useState("tabs_location");
  const [names] = model.useState("_names");
  const [sx] = model.useState("sx");
  const objects = model.get_child("objects");

  const handleChange = (event, newValue) => {
    setActive(newValue);
  };

  const orientation = (location === "above" || location === "below") ? "horizontal" : "vertical"

  React.useEffect(() => view.update_layout(), [active])

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
      sx={sx}
    >
      {names.map((label, index) => (
        <Tab key={index} label={label} />
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
