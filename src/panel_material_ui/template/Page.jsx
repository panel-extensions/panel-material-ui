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
import useMediaQuery from "@mui/material/useMediaQuery";
import {styled, useTheme} from "@mui/material/styles";

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
  const [sx] = model.useState("sx")
  const [contextbar_open, contextOpen] = model.useState("contextbar_open")
  const [contextbar_width] = model.useState("contextbar_width")
  const sidebar = model.get_child("sidebar")
  const contextbar = model.get_child("contextbar")
  const header = model.get_child("header")

  const toggleTheme = () => {
    setDarkTheme(!dark_theme)
  }

  let global_style_el = document.querySelector("#global-styles-panel-mui")
  const template_style_el = document.querySelector("#template-styles")
  if (!global_style_el) {
    {
      global_style_el = document.createElement("style")
      global_style_el.id = "global-styles-panel-mui"
      if (template_style_el) {
        document.head.insertBefore(global_style_el, template_style_el)
      } else {
        document.head.appendChild(global_style_el)
      }
    }
  }
  let page_style_el = document.querySelector("#page-style")
  if (!page_style_el) {
    page_style_el = document.createElement("style")
    page_style_el.id = "page-style"
    if (template_style_el) {
      document.head.insertBefore(page_style_el, template_style_el)
    } else {
      document.head.appendChild(page_style_el)
    }
  }

  React.useEffect(() => {
    global_style_el.textContent = render_theme_css(theme)
    const style_objs = theme.generateStyleSheets()
    const css = style_objs
      .map((obj) => {
        return Object.entries(obj).map(([selector, vars]) => {
          const varLines = Object.entries(vars)
            .map(([key, val]) => `  ${key}: ${val};`)
            .join("\n");
          return `:root, ${selector} {\n${varLines}\n}`;
        })
          .join("\n\n");
      })
      .join("\n\n");
    page_style_el.textContent = css
  }, [theme])

  const drawer = sidebar.length > 0 ? (
    <Drawer
      open={open}
      sx={{
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {width: sidebar_width, boxSizing: "border-box"},
      }}
      variant={variant === "drawer" || isMobile ? "temporary": "persistent"}
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
      anchor="right"
      open={contextbar_open}
      onClose={() => contextOpen(false)}
      sx={{
        width: contextbar_width,
        flexShrink: 0,
        zIndex: (theme) => theme.zIndex.drawer + 2,
        [`& .MuiDrawer-paper`]: {width: contextbar_width, padding: "0.5em", boxSizing: "border-box"},
      }}
      variant="temporary"
    >
      {contextbar}
    </Drawer>
  ) : null

  return (
    <Box sx={{display: "flex", width: "100vw", height: "100vh", overflow: "hidden", ...sx}}>
      <AppBar position="fixed" color="primary" sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
        <Toolbar>
          { model.sidebar.length > 0 &&
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={() => setOpen(!open)}
            edge="start"
            sx={[
              {
                mr: 2,
              },
            ]}
          >
            {open ? <MenuOpenIcon/> : <MenuIcon />}
          </IconButton>
          }
          <Typography variant="h5" sx={{color: "white"}}>
            {title}
          </Typography>
          <Box sx={{alignItems: "center", flexGrow: 1, display: "flex", flexDirection: "row"}}>
            {header}
          </Box>
          <IconButton onClick={toggleTheme} color="inherit" align="right">
            {dark_theme ? <DarkMode /> : <LightMode />}
          </IconButton>
          { (model.contextbar.length > 0 && !contextbar_open) &&
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={() => contextOpen(!contextbar_open)}
            edge="start"
            sx={[
              {
                mr: 2,
              },
            ]}
          >
            <TocIcon />
          </IconButton>}
        </Toolbar>
      </AppBar>
      {drawer &&
      <Box
        component="nav"
        sx={variant === "drawer" || isMobile ? {width: 0, flexShrink: {xs: 0}} : {width: {sm: sidebar_width}, flexShrink: {sm: 0}}}
      >
        {drawer}
      </Box>}
      <Main open={open} sidebar_width={sidebar_width} variant={isMobile ? "drawer" : variant}>
        <Box sx={{display: "flex", flexDirection: "column", height: "100%"}}>
          <Toolbar/>
          <Box sx={{flexGrow: 1, display: "flex", minHeight: 0}}>
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
