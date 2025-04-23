import * as React from "react"
import {grey} from "@mui/material/colors"
import {createTheme} from "@mui/material/styles"
import {deepmerge} from "@mui/utils"

export class SessionStore {
  constructor() {
    this.shared_var = null
    this._callbacks = []
  }

  set_value(value) {
    const old = this.shared_var
    this.shared_var = value
    if (value !== old) {
      for (const cb of this._callbacks) {
        cb(value)
      }
    }
  }

  get_value() {
    return this.shared_var
  }

  subscribe(callback) {
    this._callbacks.push(callback)
    return () => this._callbacks.splice(this._callbacks.indexOf(callback), 1)
  }

  unsubscribe(callback) {
    this._callbacks.splice(this._callbacks.indexOf(callback), 1)
  }
}

export const dark_mode = new SessionStore()

export function render_theme_css(theme) {
  const dark = theme.palette.mode === "dark"
  return `
    :root, :host {
      --panel-primary-color: ${theme.palette.primary.main};
      --panel-on-primary-color: ${theme.palette.primary.contrastText};
      --panel-secondary-color: ${theme.palette.secondary.main};
      --panel-on-secondary-color: ${theme.palette.secondary.contrastText};
      --panel-background-color: ${theme.palette.background.default};
      --panel-on-background-color: ${theme.palette.text.primary};
      --panel-surface-color: ${theme.palette.background.paper};
      --panel-on-surface-color: ${theme.palette.text.primary};
      --code-bg-color: #263238;
      --code-text-color: #82aaff;
      --success-bg-color: ${theme.palette.success.main};
      --success-text-color: ${theme.palette.success.contrastText};
      --danger-bg-color: ${theme.palette.error.main};
      --danger-text-color: ${theme.palette.error.contrastText};
      --info-bg-color: ${theme.palette.info.main};
      --info-text-color: ${theme.palette.info.contrastText};
      --primary-bg-color: #0d6efd;
      --secondary-bg-color: #6c757d;
      --warning-bg-color: #ffc107;
      --light-bg-color: #f8f9fa;
      --dark-bg-color: #212529;
      --primary-text-color: #0a58ca;
      --secondary-text-color: #6c757d;
      --warning-text-color: #997404;
      --light-text-color: #6c757d;
      --dark-text-color: #495057;
      --primary-bg-subtle: ${dark ? "#031633" : "#cfe2ff"};
      --secondary-bg-subtle: ${dark ? "#212529" : "#f8f9fa"};
      --success-bg-subtle: ${dark ? "#051b11" : "#d1e7dd"};
      --info-bg-subtle: ${dark ? "#032830" : "#cff4fc"};
      --warning-bg-subtle: ${dark ? "#332701" : "#fff3cd"};
      --danger-bg-subtle: ${dark ? "#2c0b0e" : "#f8d7da"};
      --light-bg-subtle: ${dark ? "#343a40" : "#fcfcfd"};
      --dark-bg-subtle: ${dark ? "#1a1d20" : "#ced4da"};
      --primary-border-subtle: ${dark ? "#084298" : "#9ec5fe"};
      --secondary-border-subtle: ${dark ? "#495057" : "#e9ecef"};
      --success-border-subtle: ${dark ? "#0f5132" : "#a3cfbb"};
      --info-border-subtle: ${dark ? "#055160" : "#9eeaf9"};
      --warning-border-subtle: ${dark ? "#664d03" : "#ffe69c"};
      --danger-border-subtle: ${dark ? "#842029" : "#f1aeb5"};
      --light-border-subtle: ${dark ? "#495057" : "#e9ecef"};
      --dark-border-subtle: ${dark ? "#343a40" : "#adb5bd"};
      --bokeh-font-size: ${theme.typography.fontSize}px;
    }
  `
}

export function render_theme_config(props, theme_config, dark_theme) {
  const config = {
    cssVariables: {
      rootSelector: ":host",
      colorSchemeSelector: "class",
    },
    palette: {
      mode: dark_theme ? "dark" : "light",
      default: {
        main: dark_theme ? grey[500] : "#000000",
        light: grey[dark_theme ? 200 : 100],
        dark: grey[dark_theme ? 800 : 600],
        contrastText: dark_theme ? "#ffffff" : "#ffffff",
      },
      dark: {
        main: grey[dark_theme ? 800 : 600],
        light: grey[dark_theme ? 700 : 400],
        dark: grey[dark_theme ? 900 : 800],
        contrastText: "#ffffff",
      },
      light: {
        main: grey[200],
        light: grey[100],
        dark: grey[300],
        contrastText: "#000000",
      },
    },
    components: {
      MuiPopover: {
        defaultProps: {
          container: props.view.container,
        },
      },
      MuiPopper: {
        defaultProps: {
          container: props.view.container,
        },
      },
      MuiModal: {
        defaultProps: {
          container: props.view.container,
        },
      },
      MuiIconButton: {
        styleOverrides: {
          root: {
            variants: [
              {
                props: {color: "default"},
                style: {
                  color: "var(--mui-palette-default-dark)",
                },
              },
            ],
          },
        },
      },
      MuiSwitch: {
        styleOverrides: {
          switchBase: {
            "&.MuiSwitch-colorDefault.Mui-checked": {
              color: "var(--mui-palette-default-contrastText)",
            },
            "&.MuiSwitch-colorDefault.Mui-checked + .MuiSwitch-track": {
              backgroundColor: "var(--mui-palette-default-main)",
              opacity: 0.7,
            },
          },
        },
      },
      MuiSlider: {
        styleOverrides: {
          root: {
            "& .MuiSlider-thumbColorDefault": {
              backgroundColor: "var(--mui-palette-default-contrastText)",
            },
            variants: [
              {
                props: {color: "default"},
                style: {
                  color: "var(--mui-palette-default-dark)",
                },
              },
            ],
          },
        },
      },
      MuiToggleButton: {
        styleOverrides: {
          root: {
            "&.MuiToggleButton-default.Mui-selected": {
              backgroundColor: "var(--mui-palette-default-light)",
              color: "var(--mui-palette-default-dark)",
            },
          },
        },
      },
      MuiFab: {
        styleOverrides: {
          root: {
            "&.MuiFab-default": {
              color: "var(--mui-palette-default-main)",
              backgroundColor: "var(--mui-palette-default-contrastText)",
            },
          }
        },
      },
      MuiTab: {
        styleOverrides: {
          root: {
            "&.MuiTab-textColorDefault": {
              color: "var(--mui-palette-default-main)"
            }
          }
        }
      },
      MuiButton: {
        styleOverrides: {
          root: {
            variants: [
              {
                props: {variant: "contained", color: "default"},
                style: {
                  backgroundColor: `var(--mui-palette-default-${dark_theme ? "dark": "contrastText"})`,
                  color: `var(--mui-palette-default-${dark_theme ? "contrastText" : "main"})`,
                  "&:hover": {
                    backgroundColor: "var(--mui-palette-default-light)",
                    color: "var(--mui-palette-default-dark)",
                  },
                },
              },
              {
                props: {variant: "outlined", color: "default"},
                style: {
                  borderColor: "var(--mui-palette-default-main)",
                  color: "var(--mui-palette-default-main)",
                  "&:hover": {
                    backgroundColor: "var(--mui-palette-default-light)",
                    color: "var(--mui-palette-default-dark)"
                  },
                },
              },
              {
                props: {variant: "text", color: "default"},
                style: {
                  color: "var(--mui-palette-default-main)",
                  "&:hover": {
                    backgroundColor: "var(--mui-palette-default-light)",
                    color: "var(--mui-palette-default-dark)",
                  },
                },
              },
            ],
            textTransform: "none",
          },
        },
      },
      MuiMultiSectionDigitalClock: {
        styleOverrides: {
          root: {
            minWidth: "165px"
          }
        }
      }
    }
  }
  if (theme_config != null) {
    return deepmerge(theme_config, config)
  }
  return config
}

export const install_theme_hooks = (props) => {
  const [dark_theme, setDarkTheme] = props.model.useState("dark_theme")
  const [own_theme_config] = props.model.useState("theme_config")

  let current = props.view
  let found = false
  while (current != null) {
    if (current.model?.data?.theme_config != null) {
      found = true
      break
    } else {
      current = current.parent
    }
  }
  const view = found ? current : props.view
  const [theme_config, setThemeConfig] = React.useState(own_theme_config ?? view.model.data.theme_config)
  const theme = React.useMemo(() => {
    const config = render_theme_config(props, theme_config, dark_theme)
    return createTheme(config)
  }, [dark_theme, theme_config])

  const cb = () => setThemeConfig(own_theme_config ?? view.model.data.theme_config)

  // If parent updates theme_config update the theme
  React.useEffect(() => {
    view.model_proxy.on("theme_config", cb)
    return () => view.model_proxy.off("theme_config", cb)
  }, [])

  // If local theme_config is updated update theme
  React.useEffect(() => cb(), [own_theme_config])

  // Sync local dark_mode with global dark mode
  const isFirstRender = React.useRef(true)
  React.useEffect(() => {
    if (isFirstRender.current && dark_mode.get_value() != null) {
      isFirstRender.current = false
      setDarkTheme(dark_mode.get_value())
      return
    }
    dark_mode.set_value(dark_theme)
  }, [dark_theme])

  React.useEffect(() => {
    let style_el = document.querySelector("#global-styles-panel-mui")
    const cb = (val) => setDarkTheme(val)
    if (style_el) {
      return dark_mode.subscribe(cb)
    } else {
      style_el = document.createElement("style")
      style_el.id = "styles-panel-mui"
      props.view.shadow_el.insertBefore(style_el, props.view.container)
      style_el.textContent = render_theme_css(theme)
    }
    return () => dark_mode.unsubscribe(cb)
  }, [])

  React.useEffect(() => {
    const style_el = props.view.shadow_el.querySelector("#styles-panel-mui")
    if (style_el) {
      style_el.textContent = render_theme_css(theme)
    }
  }, [theme])
  return theme
}
