import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import MenuOpenIcon from "@mui/icons-material/MenuOpen";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import DarkMode from "@mui/icons-material/DarkMode";
import LightMode from "@mui/icons-material/LightMode";
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
      height: "100%",
      overflow: "auto",
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
);

const DrawerHeader = styled("div")(({theme}) => ({
  display: "flex",
  alignItems: "center",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: "flex-end",
}));

export function render({model}) {
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const [sidebar_width] = model.useState("sidebar_width")
  const [title] = model.useState("title")
  const [open, setOpen] = model.useState("sidebar_open")
  const [variant] = model.useState("sidebar_variant")
  const [dark_theme, setDarkTheme] = model.useState("dark_theme")

  const toggleOpen = () => {
    setOpen(!open);
  }
  const toggleTheme = () => {
    setDarkTheme(!dark_theme)
  }

  const drawer = (
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
        {model.get_child("sidebar")}
      </Box>
    </Drawer>
  );

  return (
    <Box sx={{display: "flex", width: "100vw", height: "100vh", overflow: "hidden"}}>
      <AppBar position="fixed" color="primary" sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
        <Toolbar>
          { model.sidebar.length &&
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={toggleOpen}
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
            {model.get_child("header")}
          </Box>
          <IconButton onClick={toggleTheme} color="inherit" align="right">
            {dark_theme ? <DarkMode /> : <LightMode />}
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={variant === "drawer" || isMobile ? {width: 0, flexShrink: {xs: 0}} : {width: {sm: sidebar_width}, flexShrink: {sm: 0}}}
      >
        {drawer}
      </Box>
      <Main open={open} sidebar_width={sidebar_width} variant={isMobile ? "drawer" : variant}>
        <Toolbar/>
        {model.get_child("main")}
      </Main>
    </Box>
  );
}
