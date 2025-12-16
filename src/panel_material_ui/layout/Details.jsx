import {styled, useTheme} from "@mui/material/styles"
import Box from "@mui/material/Box"
import Collapse from "@mui/material/Collapse"
import IconButton from "@mui/material/IconButton"
import ChevronRightIcon from "@mui/icons-material/ChevronRight"
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"
import Typography from "@mui/material/Typography"
import {apply_flex} from "./utils"

const ExpandMore = styled(IconButton, {
  shouldForwardProp: (prop) => prop !== "expand",
})(({theme, expand}) => ({
  padding: "2px",
  margin: "0 2px",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
  ...(expand && {
    transform: "rotate(180deg)",
  }),
}))

const ExpandFull = styled(IconButton, {
  shouldForwardProp: (prop) => prop !== "expand",
})(({theme, expand}) => ({
  padding: "2px",
  margin: "0 2px",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
  ...(expand && {
    transform: "rotate(180deg)",
  }),
}))

export function render({model, view, el}) {
  const [collapsed, setCollapsed] = model.useState("collapsed")
  const [fully_expanded, setFullyExpanded] = model.useState("fully_expanded")
  const [header_color] = model.useState("header_color")
  const [header_css_classes] = model.useState("header_css_classes")
  const [header_background] = model.useState("header_background")
  const [hide_header] = model.useState("hide_header")
  const [square] = model.useState("square")
  const [sx] = model.useState("sx")
  const [title] = model.useState("title")
  const [title_css_classes] = model.useState("title_css_classes")
  const [scrollable_height] = model.useState("scrollable_height")
  const header = model.get_child("header")
  const objects = model.get_child("objects")
  const theme = useTheme()

  const shouldHideHeader = hide_header || (!model.header && (!title || title.trim() === ""))
  const shouldHideContent = objects.length === 0
  const isExpanded = !collapsed
  const isFullyExpanded = isExpanded && fully_expanded
  const isStretched = model.objects.some((object) => object.sizing_mode === "stretch_both" || object.sizing_mode === "stretch_height")

  const initialized = React.useRef(false)
  const updateHeight = () => {
    if (model.height != null) {
      const height = isFullyExpanded ? `${model.height}px` : "auto"
      view.el.style.height = el.style.height = height
    }
  }
  if (!initialized.current) {
    updateHeight()
    initialized.current = true
  }
  React.useEffect(() => {
    updateHeight()
  }, [isExpanded, isFullyExpanded])

  React.useEffect(() => {
    model.on("lifecycle:update_layout", () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    })
  }, [])

  if (model.header) {
    apply_flex(view.get_child_view(model.header), "row")
  }

  const handleToggleCollapse = () => {
    setCollapsed(!collapsed)
    if (!collapsed) {
      // If collapsing, also reset fully_expanded
      setFullyExpanded(false)
    }
  }

  const handleToggleFullExpand = (e) => {
    e.stopPropagation()
    setFullyExpanded(!fully_expanded)
  }

  const isDark = theme.palette.mode === "dark"
  const defaultHeaderBg = isDark
    ? theme.palette.grey[900]
    : theme.palette.grey[50]
  const topBarBackground = header_background || defaultHeaderBg

  return (
    <Box
      className="details"
      sx={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        height: "100%",
        minHeight: model.min_height ? `${model.min_height}px` : 0,
        border: `1px solid ${theme.palette.divider}`,
        borderRadius: square ? 0 : "4px",
        overflow: "hidden",
        ...sx
      }}
    >
      {!shouldHideHeader && (
        <Box
          className={header_css_classes?.length ? `details-header ${header_css_classes.join(" ")}` : "details-header"}
          onClick={handleToggleCollapse}
          sx={{
            display: "flex",
            alignItems: "center",
            padding: "4px 8px",
            cursor: "pointer",
            backgroundColor: topBarBackground,
            color: header_color || theme.palette.text.primary,
            minHeight: "28px",
            fontSize: "1rem",
            userSelect: "none",
          }}
        >
          <ChevronRightIcon
            sx={{
              fontSize: "16px",
              marginRight: "4px",
              transform: isExpanded ? "rotate(90deg)" : "rotate(0deg)",
              transition: theme.transitions.create("transform", {
                duration: theme.transitions.duration.shortest,
              }),
            }}
          />
          {model.header ? header : (
            <Typography
              classes={title_css_classes}
              dangerouslySetInnerHTML={{__html: title}}
              sx={{
                display: "inline-flex",
                alignItems: "center",
                gap: "0.25em",
                fontSize: "1rem",
                fontWeight: 400,
                flex: 1,
                margin: 0,
                padding: 0,
              }}
            />
          )}
          {isFullyExpanded && (
            <ExpandFull
              expand
              onClick={(e) => {
                e.stopPropagation()
                handleToggleFullExpand(e)
              }}
              aria-label="collapse to scrollable"
              size="small"
              sx={{
                ml: "auto",
              }}
            >
              <ExpandMoreIcon sx={{fontSize: "16px"}} />
            </ExpandFull>
          )}
        </Box>
      )}
      <Collapse
        in={isExpanded}
        timeout="auto"
        unmountOnExit
        sx={{
          flexGrow: 1,
          width: "100%",
          "& .MuiCollapse-wrapper": {
            height: (isFullyExpanded || isStretched) ? "100% !important" : "auto",
          },
        }}
      >
        {!shouldHideContent && (
          <Box
            className="details-content"
            sx={{
              display: "flex",
              flexDirection: "column",
              height: isFullyExpanded ? "100%" : "auto",
              maxHeight: isFullyExpanded ? "none" : `${scrollable_height}px`,
              minHeight: (isStretched && !isFullyExpanded && scrollable_height) ? `${scrollable_height}px` : "none",
              overflowY: isFullyExpanded ? "visible" : "auto",
              overflowX: "hidden",
            }}
          >
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                flex: 1,
              }}
            >
              {objects.map((object, index) => {
                apply_flex(view.get_child_view(model.objects[index]), "column")
                return object
              })}
            </Box>
          </Box>
        )}
      </Collapse>
      {isExpanded && !isFullyExpanded && (
        <Box
          className="details-expand-button"
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            padding: "4px",
            borderTop: `1px solid ${theme.palette.divider}`,
            backgroundColor: defaultHeaderBg,
            position: "sticky",
            bottom: 0,
          }}
        >
          <ExpandFull
            expand={false}
            onClick={handleToggleFullExpand}
            aria-label="expand fully"
            size="small"
          >
            <ExpandMoreIcon sx={{fontSize: "16px"}} />
          </ExpandFull>
        </Box>
      )}
    </Box>
  );
}
