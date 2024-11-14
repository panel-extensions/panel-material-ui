import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";

export function render({model}) {
  const [active, setActive] = model.useState("active");
  const [color] = model.useState("color");
  const [location] = model.useState("tabs_location");
  const [names] = model.useState("_names");
  const objects = model.get_child("objects");

  const handleChange = (event, newValue) => {
    setActive(newValue);
  };

  const orientation = (location === "above" || location === "below") ? "horizontal" : "vertical"

  const tabs = (
    <Tabs
      indicatorColor={color}
      textColor={color}
      value={active}
      onChange={handleChange}
      orientation={orientation}
      variant="scrollable"
      scrollButtons="auto"
    >
      {names.map((label, index) => (
        <Tab key={index} label={label} />
      ))}
    </Tabs>
  )
  return (
    <Box style={{display: "flex", flexDirection: (location === "left" || location === "right") ? "row" : "column"}}  >
      { (location === "left" || location === "above") && tabs }
      <Box>
        {objects[active]}
      </Box>
      { (location === "right" || location === "below") && tabs }
    </Box>
  );
}
