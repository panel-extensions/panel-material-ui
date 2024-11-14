import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Icon from "@mui/material/Icon";

export function render({model}) {
  const [color] = model.useState("color")
  const [title] = model.useState("title")
  const [position] = model.useState("position")
  const objects = model.get_child("objects");

  return (
    <AppBar color={color} position={position}>
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{mr: 2}}
        >
          <Icon>menu</Icon>
        </IconButton>
        <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
          {title}
        </Typography>
        {objects}
      </Toolbar>
    </AppBar>
  );
}
