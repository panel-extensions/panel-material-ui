import {deepmerge} from "@mui/utils";
import {grey} from "@mui/material/colors";

export class SessionStore {
  constructor() {
    this.shared_var = null
    this._callbacks = []
  }

  set_value(value) {
    this.shared_var = value
    for (const cb of this._callbacks) {
      cb(value)
    }
  }

  get_value() {
    return this.shared_var
  }

  subscribe(callback) {
    this._callbacks.push(callback)
    return () => this._callbacks.splice(this._callbacks.indexOf(callback), 1)
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
        main: grey[dark_theme ? 700 : 400],
        light: grey[dark_theme ? 500 : 200],
        dark: grey[dark_theme ? 900 : 600],
        contrastText: dark_theme ? "#ffffff" : "#000000",
      },
      dark: {
        main: grey[dark_theme ? 800 : 600],
        light: grey[dark_theme ? 700 : 400],
        dark: grey[dark_theme ? 900 : 800],
        contrastText: dark_theme ? "#ffffff" : "#000000",
      },
      light: {
        main: grey[200],
        light: "#ffffff",
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
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: "none",
          },
        },
      },
      MuiButtonBase: {
        styleOverrides: {
          root: {
            textTransform: "none",
          },
        },
      },
    }
  }
  if (theme_config != null) {
    return deepmerge(theme_config, config)
  }
  return config
}
