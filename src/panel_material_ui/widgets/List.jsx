import Avatar from "@mui/material/Avatar"
import Collapse from "@mui/material/Collapse"
import Divider from "@mui/material/Divider"
import ExpandLess from "@mui/icons-material/ExpandLess"
import ExpandMore from "@mui/icons-material/ExpandMore"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import {parseIconName} from "./utils"
import List from "@mui/material/List"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemAvatar from "@mui/material/ListItemAvatar"
import ListItemText from "@mui/material/ListItemText"
import ListSubheader from "@mui/material/ListSubheader"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"
import MoreVert from "@mui/icons-material/MoreVert"
import Checkbox from "@mui/material/Checkbox"
import Tooltip from "@mui/material/Tooltip"
import {render_icon} from "./utils"

export function render({model}) {
  const [active, setActive] = model.useState("active")
  const [color] = model.useState("color")
  const [collapsed] = model.useState("collapsed")
  const [dense] = model.useState("dense")
  const [disabled] = model.useState("disabled")
  const [expanded, setExpanded] = model.useState("expanded")
  const [highlight] = model.useState("highlight")
  const [label] = model.useState("label")
  const [items] = model.useState("items")
  const [level_indent] = model.useState("level_indent")
  const [show_children] = model.useState("show_children")
  const [sx] = model.useState("sx")
  const [menu_open, setMenuOpen] = React.useState({})
  const [menu_anchor, setMenuAnchor] = React.useState(null)
  const current_menu_open = {...menu_open}

  const active_array = Array.isArray(active) ? active : [active]
  const [toggle_values, setToggleValues] = React.useState(new Map())
  const toggle_ref = React.useRef(toggle_values)

  const setAction = (key, value) => {
    const newMap = new Map(toggle_ref.current)
    newMap.set(key, value)
    setToggleValues(newMap)
    toggle_ref.current = newMap
  }

  React.useEffect(() => {
    setMenuOpen(current_menu_open)
    const handler = (msg) => {
      if (msg.type == "toggle_action") {
        const toggle_key = `${msg.index.join(",")}-${msg.action}`
        setAction(toggle_key, msg.value)
      }
    }
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [])

  const render_item = (item, index, path, indent=0) => {
    if (item == null) {
      return <Divider key={`divider-${index}`}/>
    }
    if (path == null) {
      path = [index]
    } else {
      path = [...path, index]
    }
    const isActive = path.length === active_array.length && path.every((value, index) => value === active_array[index])
    const isSelectable = item.selectable ?? true
    const key = path.join(",")
    const isObject = (typeof item === "object" && item !== null)
    const label = isObject ? item.label : item
    const secondary = item.secondary || null
    const actions = item.actions
    const icon = item.icon
    const icon_color = item.color || "default"
    const href = item.href
    const target = item.target
    const avatar = item.avatar
    const subitems = show_children ? item.items : []
    const item_open = expanded.map((e) => e.toString()).includes(path.toString()) || (item.open !== undefined ? item.open : false)

    current_menu_open[key] = current_menu_open[key] === undefined ? false : current_menu_open[key]

    let leadingComponent = null
    if (icon === null) {
      leadingComponent = null
    } else if (icon) {
      leadingComponent = (() => {
        const iconData = parseIconName(icon)
        return (
          <ListItemIcon>
            <Icon baseClassName={iconData.baseClassName} color={icon_color}>{iconData.iconName}</Icon>
          </ListItemIcon>
        )
      })()
    } else {
      leadingComponent = (
        <ListItemAvatar>
          <Avatar
            size="small"
            variant="square"
            color={icon_color}
            sx={{
              bgcolor: icon_color
            }}
          >
            {avatar || label[0].toUpperCase()}
          </Avatar>
        </ListItemAvatar>
      )
    }

    const inline_actions = actions ? actions.filter(b => b.inline) : []
    const menu_actions = actions ? actions.filter(b => !b.inline) : []

    const combined_indent = indent * level_indent
    const list_item = (
      <ListItemButton
        disableRipple={!isSelectable}
        color={color}
        className={collapsed ? "collapsed" : null}
        disabled={disabled}
        href={href}
        target={target}
        key={`list-item-${key}`}
        onClick={() => {
          if (isSelectable) {
            setActive(path)
          }
          model.send_msg({type: "click", item: path})
        }}
        selected={highlight && isActive}
        sx={{
          m: `0 0 0 ${combined_indent + (highlight ? 6 : 0)}px`,
          pr: 1,
          pl: 1,
          "&.MuiListItemButton-root": {
            "&.collapsed": {
              pl: 1,
              ".MuiListItemIcon-root": {pr: 0}
            },
            ".MuiListItemIcon-root": {minWidth: "unset", pr: 1},
            "&.Mui-selected": {
              bgcolor: isActive
                ? `rgba(var(--mui-palette-${color}-mainChannel) / var(--mui-palette-action-selectedOpacity))`
                : "inherit",
              ml: `${combined_indent}px`,
              borderLeft: `6px solid var(--mui-palette-${color}-main)`,
              ".MuiListItemText-root": {
                ".MuiTypography-root.MuiListItemText-primary": {
                  fontWeight: "bold"
                }
              }
            },
            "&.Mui-focusVisible": {
              borderLeft: isActive
                ? `6px solid var(--mui-palette-${color}-main)`
                : "3px solid var(--mui-palette-secondary-main)",
              borderTop: "3px solid var(--mui-palette-secondary-main)",
              borderRight: "3px solid var(--mui-palette-secondary-main)",
              borderBottom: "3px solid var(--mui-palette-secondary-main)",
              bgcolor: isActive
                ? `rgba(var(--mui-palette-${color}-mainChannel) / var(--mui-palette-action-selectedOpacity))`
                : "inherit"
            },
            "&:hover": {
              ".MuiListItemText-root": {
                ".MuiTypography-root.MuiListItemText-primary": {
                  textDecoration: "underline"
                }
              }
            }
          },
        }}
      >
        {leadingComponent}
        {!collapsed && <ListItemText primary={label} secondary={secondary} />}
        {!collapsed && inline_actions.map((action, index) => {
          const icon = action.icon
          const icon_color = action.color
          const active_icon = action.active_icon || icon
          const active_color = action.active_color || icon_color
          const action_key = action.action || action.label
          const toggle_key = `${key}-${action_key}`
          const action_value = toggle_ref.current.get(toggle_key) ?? action.value ?? false
          return action.toggle ? (
            <Checkbox
              checked={action_value}
              checkedIcon={active_icon && render_icon(active_icon, active_color || color, null, null)}
              color={action.color}
              disabled={disabled}
              icon={render_icon(icon, icon_color, null, null, "-outlined")}
              size={"small"}
              onMouseDown={(e) => {
                e.stopPropagation()
                e.preventDefault()
              }}
              onClick={(e) => {
                const new_value = !action_value
                setAction(toggle_key, new_value)
                model.send_msg({type: "action", action: action_key, item: path, value: new_value})
                e.stopPropagation()
                e.preventDefault()
              }}
            />
          ) : (
            <IconButton
              color={action.color}
              key={`action-button-${index}`}
              size="small"
              title={action.label}
              onMouseDown={(e) => {
                e.stopPropagation()
                e.preventDefault()
              }}
              onClick={(e) => {
                model.send_msg({type: "action", action: action.action || action.label, item: path})
                e.stopPropagation()
                e.preventDefault()
              }}
              sx={{ml: index > 0 ? "0" : "0.5em"}}
            >
              {action.icon && render_icon(action.icon)}
            </IconButton>)
        })}
        {!collapsed && menu_actions.length > 0 && (
          <React.Fragment>
            <IconButton
              size="small"
              onMouseDown={(e) => {
                e.stopPropagation()
              }}
              onClick={(e) => {
                current_menu_open[key] = true
                setMenuOpen(current_menu_open)
                setMenuAnchor(e.currentTarget)
                e.stopPropagation()
              }}
              sx={{ml: "0.5em", color: "text.secondary"}}
            >
              <MoreVert />
            </IconButton>
            <Menu
              anchorEl={menu_anchor}
              open={current_menu_open[key]}
              onClose={() => setMenuOpen({...current_menu_open, [key]: false})}
            >
              {menu_actions.map((action, index) => {
                if (action === null) {
                  return <Divider key={`action-divider-${index}`}/>
                }
                return (
                  <MenuItem
                    key={`action-${index}`}
                    onMouseDown={(e) => {
                      e.stopPropagation()
                    }}
                    onClick={(e) => {
                      model.send_msg({type: "action", action: action.action || action.label, item: path})
                      e.stopPropagation()
                    }}
                  >
                    {action.icon && render_icon(action.icon)}
                    {action.label}
                  </MenuItem>
                )
              })}
            </Menu>
          </React.Fragment>
        )}
        {!collapsed && subitems && subitems.length ? (
          <IconButton
            size="small"
            onMouseDown={(e) => {
              e.stopPropagation()
            }}
            onClick={(e) => {
              e.stopPropagation()
              const new_key = Number(key)
              const index = expanded.map((e) => e.toString()).indexOf(key.toString())
              const new_expanded = [...expanded]
              if (index === -1) {
                new_expanded.push(new_key)
              } else {
                new_expanded.splice(index, 1)
              }
              setExpanded(new_expanded)
            }}
            sx={{ml: 0.25}}
          >
            {item_open ? <ExpandLess/> : <ExpandMore />}
          </IconButton>
        ) : null}
      </ListItemButton>
    )

    if (!collapsed && subitems && subitems.length) {
      return [
        list_item,
        <Collapse in={item_open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding dense={dense}>
            {subitems.map((subitem, index) => {
              return render_item(subitem, index, path, indent+1)
            })}
          </List>
        </Collapse>
      ]
    } else if (collapsed) {
      return (
        <Tooltip title={label} placement="right" disableInteractive>
          {list_item}
        </Tooltip>
      )
    }
    return list_item
  }

  return (
    <List
      dense={dense}
      component="nav"
      sx={{p: 0, ...sx}}
      subheader={label && (
        <ListSubheader component="div" id="nested-list-subheader">
          {label}
        </ListSubheader>
      )}
    >
      {items.map((item, index) => render_item(item, index))}
    </List>
  )
}
