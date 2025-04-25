import DarkMode from "@mui/icons-material/DarkMode";
import LightMode from "@mui/icons-material/LightMode";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import {useTheme} from "@mui/material/styles";
import {dark_mode, setup_global_styles} from "./utils";

export function render({model}) {
  const theme = useTheme()
  const [dark_theme, setDarkTheme] = model.useState("dark_theme")
  const [value, setValue] = model.useState("value")

  document.documentElement.dataset.themeManaged = "true"
  setup_global_styles(theme)

  return (
    <Tooltip enterDelay={500} title="Toggle theme">
      <IconButton onClick={() => { dark_mode.set_value(!value); setDarkTheme(!value); setValue(!value); }} aria-label="Toggle theme" color="inherit" align="right">
        {value ? <DarkMode /> : <LightMode />}
      </IconButton>
    </Tooltip>
  )
}
