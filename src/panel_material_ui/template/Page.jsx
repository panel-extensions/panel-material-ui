import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import LinearProgress from "@mui/material/LinearProgress";
import MenuIcon from "@mui/icons-material/Menu";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import DarkMode from "@mui/icons-material/DarkMode";
import LightMode from "@mui/icons-material/LightMode";
import TocIcon from "@mui/icons-material/Toc";
import Tooltip from "@mui/material/Tooltip";
import useMediaQuery from "@mui/material/useMediaQuery";
import {styled, useTheme} from "@mui/material/styles";
import {apply_flex, dark_mode, setup_global_styles} from "./utils"

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

export function render({model, view}) {
  const theme = useTheme()
  const [busy] = model.useState("busy")
  const [busy_indicator] = model.useState("busy_indicator")
  const [contextbar_open, contextOpen] = model.useState("contextbar_open")
  const [contextbar_width] = model.useState("contextbar_width")
  const [dark_theme, setDarkTheme] = model.useState("dark_theme")
  const [logo] = model.useState("logo")
  const [open, setOpen] = model.useState("sidebar_open")
  const [sidebar_width] = model.useState("sidebar_width")
  const [theme_toggle] = model.useState("theme_toggle")
  const [site_url] = model.useState("site_url")
  const [title] = model.useState("title")
  const [variant] = model.useState("sidebar_variant")
  const [sx] = model.useState("sx")
  const sidebar = model.get_child("sidebar")
  const contextbar = model.get_child("contextbar")
  const header = model.get_child("header")
  const main = model.get_child("main")

  const isXl = useMediaQuery(theme.breakpoints.up("xl"))
  const isLg = useMediaQuery(theme.breakpoints.up("lg"))
  const isMd = useMediaQuery(theme.breakpoints.up("md"))
  const isSm = useMediaQuery(theme.breakpoints.up("sm"))
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"))

  const logoContent = React.useMemo(() => {
    if (!logo) { return null }
    if (typeof logo === "string") { return logo }

    if (isXl && logo.xl) { return logo.xl }
    if (isLg && logo.lg) { return logo.lg }
    if (isMd && logo.md) { return logo.md }
    if (isSm && logo.sm) { return logo.sm }
    if (logo.xs) { return logo.xs }

    return logo.default || Object.values(logo)[0];
  }, [logo, theme.breakpoints, isXl, isLg, isMd, isSm])

  React.useEffect(() => {
    model.on("lifecycle:update_layout", () => {
      sidebar.map((object, index) => {
        apply_flex(view.get_child_view(model.sidebar[index]), "column")
      })
      contextbar.map((object, index) => {
        apply_flex(view.get_child_view(model.contextbar[index]), "column")
      })
      header.map((object, index) => {
        apply_flex(view.get_child_view(model.header[index]), "row")
      })
      main.map((object, index) => {
        apply_flex(view.get_child_view(model.main[index]), "column")
      })
    })
  }, [])

  // Set up debouncing of busy indicator
  const [idle, setIdle] = React.useState(true);
  const timerRef = React.useRef(undefined)
  React.useEffect(() => {
    if (busy) {
      timerRef.current = setTimeout(() => {
        setIdle(false)
      }, 1000)
    } else {
      setIdle(true)
      clearTimeout(timerRef.current)
    }
  }, [busy])
  React.useEffect(() => () => clearTimeout(timerRef.current), [])

  const toggleTheme = () => {
    setDarkTheme(!dark_theme)
  }

  setup_global_styles(theme)
  React.useEffect(() => dark_mode.set_value(dark_theme), [dark_theme])

  const drawer_variant = variant === "auto" ? (isMobile ? "temporary": "persistent") : variant
  const drawer = sidebar.length > 0 ? (
    <Drawer
      PaperProps={{className: "sidebar"}}
      anchor="left"
      disablePortal
      open={open}
      onClose={drawer_variant === "temporary" ? (() => setOpen(false)) : null}
      sx={{
        display: "flex",
        flexDirection: "column",
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {width: sidebar_width, boxSizing: "border-box"},
      }}
      variant={drawer_variant}
    >
      <Toolbar sx={busy_indicator === "linear" ? {m: "4px"} : {}}>
        <Typography variant="h5">&nbsp;</Typography>
      </Toolbar>
      <Box sx={{overflow: "auto", flexGrow: 1, display: "flex", flexDirection: "column"}}>
        {sidebar.map((object, index) => {
          apply_flex(view.get_child_view(model.sidebar[index]), "column")
          return object
        })}
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
        display: "flex",
        flexDirection: "column",
        flexShrink: 0,
        width: contextbar_width,
        zIndex: (theme) => theme.zIndex.drawer + 2,
        [`& .MuiDrawer-paper`]: {width: contextbar_width, padding: "0.5em", boxSizing: "border-box"},
      }}
      variant="temporary"
    >
      {contextbar.map((object, index) => {
        apply_flex(view.get_child_view(model.contextbar[index]), "column")
        return object
      })}
    </Drawer>
  ) : null

  const color_scheme = dark_theme ? "dark" : "light"
  const main_stretch = model.main.length === 1 && (model.main[0].sizing_mode && (model.main[0].sizing_mode.includes("height") ||  model.main[0].sizing_mode.includes("both")))
  const primary_color = model.theme_config?.palette?.primary?.main ?? model.theme_config?.[color_scheme]?.palette?.primary?.main
  const header_sx = primary_color == null ? {backgroundColor: "#0072b5", color: "#ffffff"} : {}

  return (
    <Box className={`mui-${color_scheme}`} sx={{display: "flex", width: "100vw", height: "100vh", overflow: "hidden", ...sx}}>
      <AppBar position="fixed" color="primary" className="header" sx={{zIndex: (theme) => theme.zIndex.drawer + 1, ...header_sx}}>
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
          {logo && <a href={site_url}><img src={logoContent} alt="Logo" className="logo" style={{height: "2.5em", paddingRight: "1em"}} /></a>}
          {title && (
            <a href={site_url} style={{textDecoration: "none"}}>
              <Typography variant="h5" className="title" sx={{color: "white"}}>
                {title}
              </Typography>
            </a>
          )}
          <Box sx={{alignItems: "center", flexGrow: 1, display: "flex", flexDirection: "row"}}>
            {header.map((object, index) => {
              apply_flex(view.get_child_view(model.header[index]), "row")
              return object
            })}
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
                sx={{mr: 1}}
              >
                <TocIcon />
              </IconButton>
            </Tooltip>
          }
          {busy_indicator === "circular" &&
            <CircularProgress
              disableShrink
              size="1.4em"
              sx={{color: "white"}}
              thickness={5}
              variant={idle ? "determinate" : "indeterminate"}
              value={idle ? 100 : 0}
            />}
        </Toolbar>
        {busy_indicator === "linear" &&
          <LinearProgress
            sx={{width: "100%"}}
            variant={idle ? "determinate" : "indeterminate"}
            color="primary"
            value={idle ? 100 : 0}
          />
        }
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
          <Toolbar sx={busy_indicator === "linear" ? {m: "4px"} : {}}>
            <Typography variant="h5">&nbsp;</Typography>
          </Toolbar>
          <Box sx={{flexGrow: 1, display: "flex", minHeight: 0, flexDirection: "column", overflowY: main_stretch ? "hidden" : "auto"}}>
            {main.map((object, index) => {
              apply_flex(view.get_child_view(model.main[index]), "column")
              return object
            })}
          </Box>
        </Box>
      </Main>
      <Box component="nav" sx={{flexShrink: 0}}>
        {context_drawer}
      </Box>
    </Box>
  );
}
