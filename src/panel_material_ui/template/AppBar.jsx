import AppBar from "@mui/material/AppBar"
import Box from "@mui/material/Box"
import Toolbar from "@mui/material/Toolbar"
import Typography from "@mui/material/Typography"
import IconButton from "@mui/material/IconButton"
import {render_icon, render_icon_text} from "./utils"

export function render({model, host}) {
  const [color] = model.useState("color")
  const [enable_color_on_dark] = model.useState("enable_color_on_dark")
  const [icon] = model.useState("icon")
  const [position] = model.useState("position")
  const [title] = model.useState("title")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const drawer_toggle = model.render_children("drawer_toggle")
  const objects = model.render_children("objects", {direction: "row"})

  return (
    <AppBar
      color={color}
      enableColorOnDark={enable_color_on_dark}
      position={position}
      sx={sx}
    >
      <Toolbar disableGutters variant={variant}>
        {drawer_toggle}
        {icon && (
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{mr: 2}}
          >
            {render_icon(icon, null, "large")}
          </IconButton>
        )}
        {title && (
          <Typography variant="h3" component="div" noWrap sx={{flexGrow: 0}}>
            {render_icon_text(title)}
          </Typography>
        )}
        <Box sx={{flexGrow: 1, display: "flex", alignItems: "center", ml: title ? 2 : 0}}>
          {objects}
        </Box>
      </Toolbar>
    </AppBar>
  )
}
