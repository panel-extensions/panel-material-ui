import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Box from "@mui/material/Box"
import Avatar from "@mui/material/Avatar"
import {useTheme} from "@mui/material/styles"
import {render_icon, render_icon_text} from "./utils"

const TABMENU_LABEL_ROW_SX = {display: "flex", alignItems: "center", gap: 0.5}
const TABMENU_AVATAR_SX = {fontSize: "1em", width: 24, height: 24, marginRight: 4}

export function render({model}) {
  const [color] = model.useState("color")
  const [items] = model.useState("items")
  const [sx] = model.useState("sx")
  const [active, setActive] = model.useState("active")
  const [variant] = model.useState("variant")
  const [centered] = model.useState("centered")
  const [scrollButtons] = model.useState("scroll_buttons")
  const [iconPosition] = model.useState("icon_position")

  const theme = useTheme()
  const safeItems = Array.isArray(items) ? items : []
  const resolvedIconPosition = iconPosition || "start"

  const handleChange = (event, newValue) => {
    setActive(newValue)
    model.send_msg({type: "click", item: newValue})
  }

  const tabItems = React.useMemo(() => safeItems.map((item, index) => {
    const label = typeof item === "string" ? item : (item?.label || "")
    const icon = item?.icon
    const avatar = item?.avatar
    const href = item?.href
    const target = item?.target

    if (icon && !avatar) {
      return (
        <Tab
          key={index}
          icon={render_icon(icon)}
          iconPosition={resolvedIconPosition}
          href={href}
          target={target}
          label={render_icon_text(label)}
        />
      )
    }

    const labelContent = (
      <Box sx={TABMENU_LABEL_ROW_SX}>
        {icon ? render_icon(icon, null, null, "1.2em") : null}
        {avatar ? (
          <Avatar
            sx={TABMENU_AVATAR_SX}
            style={{backgroundColor: theme.palette[color]?.main || color}}
          >
            {avatar}
          </Avatar>
        ) : null}
        {render_icon_text(label)}
      </Box>
    )

    return (
      <Tab
        key={index}
        label={labelContent}
        iconPosition={resolvedIconPosition}
        href={href}
        target={target}
      />
    )
  }), [safeItems, resolvedIconPosition, theme.palette, color])

  // Handle active being None - Tabs requires a number or false
  const tabValue = Number.isInteger(active) && active >= 0 && active < safeItems.length ? active : false

  // MUI Tabs only supports "primary" and "secondary" for indicatorColor/textColor
  // For other colors, we use custom styling via sx using CSS variables or theme palette
  const isStandardColor = color === "primary" || color === "secondary" || !color
  const baseColor = isStandardColor ? (color || "primary") : "primary"

  // Build custom sx styles for non-standard colors using palette CSS variables
  // MUI exposes palette colors via theme.palette, which we can use directly
  const customSx = !isStandardColor && theme.palette[color] ? {
    "& .MuiTabs-indicator": {
      backgroundColor: `var(--mui-palette-${color}-main, ${theme.palette[color].main})`
    },
    "& .MuiTab-root.Mui-selected": {
      color: `var(--mui-palette-${color}-main, ${theme.palette[color].main})`
    },
    "& .MuiTab-root": {
      color: theme.palette.text.secondary
    }
  } : {}

  const mergedSx = React.useMemo(() => {
    if (sx) {
      return [customSx, sx]
    }
    return customSx
  }, [customSx, sx])

  return (
    <Tabs
      value={tabValue}
      onChange={handleChange}
      centered={centered}
      indicatorColor={baseColor}
      variant={variant || "standard"}
      scrollButtons={scrollButtons || "auto"}
      sx={mergedSx}
      textColor={baseColor}
    >
      {tabItems}
    </Tabs>
  )
}
