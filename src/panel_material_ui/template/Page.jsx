import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import DarkMode from "@mui/icons-material/DarkMode";
import LightMode from "@mui/icons-material/LightMode";
import TocIcon from "@mui/icons-material/Toc";
import Tooltip from "@mui/material/Tooltip";
import useMediaQuery from "@mui/material/useMediaQuery";
import {styled, useTheme} from "@mui/material/styles";
import {dark_mode, setup_global_styles} from "./utils"

const Main = styled("main", {shouldForwardProp: (prop) => prop !== "open" && prop !== "variant" && prop !== "sidebar_width"})(
  ({sidebar_width, theme, open, variant}) => {
    return ({
      backgroundColor: theme.palette.background.paper,
      flexGrow: 1,
      marginLeft: variant === "persistent" ? `-${sidebar_width}px` : "0px",
      padding: "0px",
      p: 3,
      transition: theme.transitions.create("margin", {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
      height: "auto",
      overflow: "hidden",
      width: {sm: `calc(100% - ${sidebar_width}px)`},
      variants: [
        {
          props: ({open, variant}) => open && variant === "persistent",
          style: {
            transition: theme.transitions.create("margin", {
              easing: theme.transitions.easing.easeOut,
              duration: theme.transitions.duration.enteringScreen,
            }),
            marginLeft: 0,
          },
        },
      ],
    })
  }
)

export function render({model}) {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const [sidebar_width] = model.useState("sidebar_width")
  const [title] = model.useState("title")
  const [open, setOpen] = model.useState("sidebar_open")
  const [variant] = model.useState("sidebar_variant")
  const [dark_theme, setDarkTheme] = model.useState("dark_theme")
  const [theme_toggle] = model.useState("theme_toggle")
  const [sx] = model.useState("sx")
  const [contextbar_open, contextOpen] = model.useState("contextbar_open")
  const [contextbar_width] = model.useState("contextbar_width")
  const sidebar = model.get_child("sidebar")
  const contextbar = model.get_child("contextbar")
  const header = model.get_child("header")

  const toggleTheme = () => {
    setDarkTheme(!dark_theme)
  }

  setup_global_styles(theme)

  React.useEffect(() => dark_mode.set_value(dark_theme), [])

  const drawer_variant = variant === "auto" ? (isMobile ? "temporary": "persistent") : variant
  const drawer = sidebar.length > 0 ? (
    <Drawer
      PaperProps={{className: "sidebar"}}
      anchor="left"
      disablePortal
      open={open}
      onClose={drawer_variant === "temporary" ? (() => setOpen(false)) : null}
      sx={{
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {width: sidebar_width, boxSizing: "border-box"},
      }}
      variant={drawer_variant}
    >
      <Toolbar/>
      <Divider />
      <Box sx={{overflow: "auto"}}>
        {sidebar}
      </Box>
    </Drawer>
  ) : null

  const context_drawer = contextbar.length > 0 ? (
    <Drawer
      PaperProps={{className: "contextbar"}}
      anchor="right"
      disablePortal
      open={contextbar_open}
      onClose={() => contextOpen(false)}
      sx={{
        flexShrink: 0,
        width: contextbar_width,
        zIndex: (theme) => theme.zIndex.drawer + 2,
        [`& .MuiDrawer-paper`]: {width: contextbar_width, padding: "0.5em", boxSizing: "border-box"},
      }}
      variant="temporary"
    >
      {contextbar}
    </Drawer>
  ) : null

  return (
    <Box className={`mui-${dark_theme ? "dark" : "light"}`} sx={{display: "flex", width: "100vw", height: "100vh", overflow: "hidden", ...sx}}>
      <AppBar position="fixed" color="primary" className="header" sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
        <Toolbar>
          {(model.sidebar.length > 0 && drawer_variant !== "permanent") &&
            <Tooltip enterDelay={500} title={open ? "Close drawer" : "Open drawer"}>
              <IconButton
                color="inherit"
                aria-label={open ? "Close drawer" : "Open drawer"}
                onClick={() => setOpen(!open)}
                edge="start"
                sx={{mr: 2}}
              >
                {open ? <MenuOpenIcon/> : <MenuIcon />}
              </IconButton>
            </Tooltip>
          }
          <Typography variant="h5" sx={{color: "white"}}>
            {title}
          </Typography>
          <Box sx={{alignItems: "center", flexGrow: 1, display: "flex", flexDirection: "row"}}>
            {header}
          </Box>
          {theme_toggle &&
            <Tooltip enterDelay={500} title="Toggle theme">
              <IconButton onClick={toggleTheme} aria-label="Toggle theme" color="inherit" align="right" sx={{mr: "1em"}}>
                {dark_theme ? <DarkMode /> : <LightMode />}
              </IconButton>
            </Tooltip>
          }
          {(model.contextbar.length > 0 && !contextbar_open) &&
            <Tooltip enterDelay={500} title="Toggle contextbar">
              <IconButton
                color="inherit"
                aria-label="toggle contextbar"
                onClick={() => contextOpen(!contextbar_open)}
                edge="start"
                sx={{mr: 2}}
              >
                <TocIcon />
              </IconButton>
            </Tooltip>
          }
        </Toolbar>
      </AppBar>
      {drawer &&
      <Box
        component="nav"
        sx={
          drawer_variant === "temporary" ? (
            {width: 0, flexShrink: {xs: 0}}
          ) : (
            {width: {sm: sidebar_width}, flexShrink: {sm: 0}}
          )
        }
      >
        {drawer}
      </Box>}
      <Main className="main" open={open} sidebar_width={sidebar_width} variant={drawer_variant}>
        <Box sx={{display: "flex", flexDirection: "column", height: "100%"}}>
          <Toolbar/>
          <Box sx={{flexGrow: 1, display: "flex", minHeight: 0, flexDirection: "column"}}>
            {model.get_child("main")}
          </Box>
        </Box>
      </Main>
      <Box component="nav" sx={{flexShrink: 0}}>
        {context_drawer}
      </Box>
    </Box>
  );
}
