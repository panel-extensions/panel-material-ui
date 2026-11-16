import DarkMode from "@mui/icons-material/DarkMode"
import FormControlLabel from "@mui/material/FormControlLabel"
import LightMode from "@mui/icons-material/LightMode"
import IconButton from "@mui/material/IconButton"
import Switch from "@mui/material/Switch"
import Tooltip from "@mui/material/Tooltip"
import {useTheme} from "@mui/material/styles"
import {dark_mode, setup_global_styles} from "./utils"

export function render({model, view}) {
  const theme = useTheme()
  const [dark_theme, setDarkTheme] = model.useState("dark_theme")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  setup_global_styles(view, theme)

  // On mount the theme hooks decide whether this toggle publishes its value
  // (when it was set explicitly) or adopts the page theme.
  const mounted = React.useRef(false)
  React.useEffect(() => {
    if (!mounted.current) {
      mounted.current = true
      return
    }
    dark_mode.set_value(value)
    setDarkTheme(value)
  }, [value])

  const toggle = () => {
    dark_mode.switched = true
    setValue(!value)
  }

  React.useEffect(() => {
    setValue(dark_theme)
  }, [dark_theme])

  return (
    <Tooltip enterDelay={500} title="Toggle theme">
      {variant === "switch" ? (
        <FormControlLabel
          control={
            <Switch checked={value} onChange={toggle} />
          }
          label={value ? "Dark Theme" : "Light Theme"}
        />
      ) : (
        <IconButton
          aria-label="Toggle theme"
          color="inherit" align="right"
          onClick={toggle}
        >
          {value ? <DarkMode /> : <LightMode />}
        </IconButton>
      )}
    </Tooltip>
  )
}
