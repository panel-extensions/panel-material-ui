import Avatar from "@mui/material/Avatar"
import Tabs from "@mui/material/Tabs"
import Tab from "@mui/material/Tab"
import Icon from "@mui/material/Icon"
import Box from "@mui/material/Box"
import {useTheme, styled} from "@mui/material/styles"
import {parseIconName} from "./utils"

const StyledAvatar = styled(Avatar)(({theme, color, spacing}) => ({
  backgroundColor: color,
  fontSize: "1em",
  width: 24,
  height: 24,
  marginRight: spacing || theme?.spacing(0.5) || 4
}))

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

  const handleChange = (event, newValue) => {
    setActive(newValue)
    model.send_msg({type: "click", item: newValue})
  }

  const tabItems = items.map((item, index) => {
    const label = typeof item === "string" ? item : (item?.label || "")
    const icon = item?.icon
    const avatar = item?.avatar
    const href = item?.href
    const target = item?.target

    // If there's only an icon and no label/avatar, use the icon prop
    if (icon && !avatar) {
      return (
        <Tab
          key={index}
          icon={(() => {
            const iconData = parseIconName(icon)
            return <Icon baseClassName={iconData.baseClassName}>{iconData.iconName}</Icon>
          })()}
          iconPosition={iconPosition || "start"}
          href={href}
          target={target}
          label={label}
        />
      )
    }

    // Otherwise, build label content with icon/avatar/label
    const labelContent = (
      <Box sx={{display: "flex", alignItems: "center", gap: 0.5}}>
        {icon ? (() => {
          const iconData = parseIconName(icon)
          return <Icon baseClassName={iconData.baseClassName} sx={{fontSize: "1.2rem"}}>{iconData.iconName}</Icon>
        })() : null}
        {avatar ? (
          <StyledAvatar
            theme={theme}
            color={theme.palette[color]?.main || color}
            spacing={theme.spacing(0.5)}
          >
            {avatar}
          </StyledAvatar>
        ) : null}
        {label}
      </Box>
    )

    return (
      <Tab
        key={index}
        label={labelContent}
        iconPosition={iconPosition || "start"}
        href={href}
        target={target}
      />
    )
  })

  // Handle active being None - Tabs requires a number or false
  const tabValue = active !== null && active !== undefined ? active : false

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

  const mergedSx = {...customSx, ...sx}

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
