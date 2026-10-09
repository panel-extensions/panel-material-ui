import * as React from "react"
import "@fontsource/roboto/400.css"
import "@fontsource/roboto/700.css"
import "material-icons/iconfont/filled.css"
import "material-icons/iconfont/outlined.css"
import CircularProgress from "@mui/material/CircularProgress"
import CssBaseline from "@mui/material/CssBaseline"
import Tooltip from "@mui/material/Tooltip"
import {ThemeProvider, useTheme as useMuiTheme} from "@mui/material/styles"
import {apply_global_css, install_theme_hooks, render_icon_text} from "./utils"

// Wrappers applied around the render function of a component, in the order
// they are listed, e.g. component(render, withLoading, withTheme) renders
// the theme provider outermost.
export function component(render, ...wrappers) {
  return {render: wrappers.reduce((wrapped, wrapper) => wrapper(wrapped), render)}
}

export function withTheme(Component) {
  return function Themed(props) {
    const theme = install_theme_hooks(props)
    const attached = ("attached" in props.view.model.data.properties) ? props.model.get_child("attached") : []
    if (props.view.is_root && document.documentElement.getAttribute("data-theme-managed") === "false") {
      apply_global_css(props.model, props.view, theme)
    }
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Component {...props}/>
        {attached.length ? <div className="attached">{attached}</div> : null}
      </ThemeProvider>
    )
  }
}

export function withLoading(Component) {
  return function Loading(props) {
    const [loading] = props.model.useState("loading")
    const loading_inset = props.model.esm_constants.loading_inset || 0
    const theme = useMuiTheme()

    const overlayColor = theme.palette.mode === "dark"
      ? "rgba(18, 18, 18, 0.7)"
      : "rgba(255, 255, 255, 0.5)"

    return (
      <div style={{display: "contents", position: "relative"}}>
        <Component {...props}/>
        {loading && (
          <div style={{
            position: "absolute",
            inset: loading_inset,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: overlayColor,
            zIndex: theme.zIndex.modal - 1
          }}
          >
            <CircularProgress color="primary" sx={{p: "8px"}} />
          </div>
        )}
      </div>
    )
  }
}

export function withTooltip(Component) {
  const WithRef = React.forwardRef(Component)
  return function Described(props) {
    const [description] = props.model.useState("description")
    const [description_delay] = props.model.useState("description_delay")

    return (description ? (
      <Tooltip
        title={render_icon_text(description)}
        arrow
        enterDelay={description_delay}
        enterNextDelay={description_delay}
        placement="right"
        slotProps={{popper: {container: props.el}}}
      >
        <WithRef {...props}/>
      </Tooltip>) : <Component {...props}/>
    )
  }
}
