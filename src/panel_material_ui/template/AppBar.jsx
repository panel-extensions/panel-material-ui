import AppBar from "@mui/material/AppBar"
import Box from "@mui/material/Box"
import Toolbar from "@mui/material/Toolbar"
import Typography from "@mui/material/Typography"
import IconButton from "@mui/material/IconButton"
import {render_icon, render_icon_text} from "./utils"
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [color] = model.useState("color")
  const [enable_color_on_dark] = model.useState("enable_color_on_dark")
  const [icon] = model.useState("icon")
  const [position] = model.useState("position")
  const [title] = model.useState("title")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const drawer_toggle = model.get_child("drawer_toggle")
  const objects = model.get_child("objects")

  React.useEffect(() => {
    const handler = () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "row")
      })
    }
    model.on("lifecycle:update_layout", handler)
    return () => model.off?.("lifecycle:update_layout", handler)
  }, [])

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
          <Typography variant="h3" component="div" noWrap>
            {render_icon_text(title)}
          </Typography>
        )}
        <Box sx={{flexGrow: 1, display: "flex", alignItems: "center", ml: title ? 2 : 0}}>
          {objects.map((object, index) => {
            apply_flex(view.get_child_view(model.objects[index]), "row")
            return object
          })}
        </Box>
      </Toolbar>
    </AppBar>
  )
}
