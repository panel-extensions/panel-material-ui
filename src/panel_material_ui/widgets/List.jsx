import Avatar from "@mui/material/Avatar"
import Collapse from "@mui/material/Collapse"
import Divider from "@mui/material/Divider"
import ExpandLess from "@mui/icons-material/ExpandLess"
import ExpandMore from "@mui/icons-material/ExpandMore"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
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

export function render({model}) {
  const [active, setActive] = model.useState("active")
  const [color] = model.useState("color")
  const [dense] = model.useState("dense")
  const [disabled] = model.useState("disabled")
  const [highlight] = model.useState("highlight")
  const [label] = model.useState("label")
  const [items] = model.useState("items")
  const [level_indent] = model.useState("level_indent")
  const [sx] = model.useState("sx")
  const [open, setOpen] = React.useState({})
  const [menu_open, setMenuOpen] = React.useState({})
  const [menu_anchor, setMenuAnchor] = React.useState(null)
  const current_open = {...open}
  const current_menu_open = {...menu_open}

  const active_array = Array.isArray(active) ? active : [active]

  React.useEffect(() => {
    setOpen(current_open)
    setMenuOpen(current_menu_open)
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
    const subitems = item.items
    const item_open = item.open || true
    current_open[key] = current_open[key] === undefined ? item_open : current_open[key]
    current_menu_open[key] = current_menu_open[key] === undefined ? false : current_menu_open[key]

    let leadingComponent = null
    if (icon === null) {
      leadingComponent = null
    } else if (icon) {
      leadingComponent = (
        <ListItemIcon>
          <Icon color={icon_color}>{icon}</Icon>
        </ListItemIcon>
      )
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

    const [toggle_values, setToggleValues] = React.useState(new Map())

    const list_item = (
      <ListItemButton
        disableRipple={!isSelectable}
        color={color}
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
          p: `0 4px 0 ${(indent+1) * level_indent}px`,
          "&.MuiListItemButton-root.Mui-selected": {
            bgcolor: isActive ? (
              `rgba(var(--mui-palette-${color}-mainChannel) / var(--mui-palette-action-selectedOpacity))`
            ) : "inherit"
          }
        }}
      >
        {leadingComponent}
        <ListItemText primary={label} secondary={secondary} />
        {inline_actions.map((action, index) => {
          const icon = action.icon
          const icon_color = action.color
          const active_icon = action.active_icon || icon
          const active_color = action.active_color || icon_color
          const action_key = action.action || action.label
          const toggle_key = `${key}-${action_key}`
          const action_value = toggle_values.get(toggle_key) ?? action.value ?? false
          toggle_values.set(toggle_key, action_value)
          return action.toggle ? (
            <Checkbox
              checked={action_value}
              color={action.color}
              disabled={disabled}
              selected={action_value}
              size={"small"}
              onMouseDown={(e) => {
                e.stopPropagation()
                e.preventDefault()
              }}
              onClick={(e) => {
                const new_value = !action_value
                const newMap = new Map(toggle_values)
                newMap.set(toggle_key, new_value)
                setToggleValues(newMap)
                model.send_msg({type: "action", action: action_key, item: path, value: new_value})
                e.stopPropagation()
                e.preventDefault()
              }}
              icon={
                icon.trim().startsWith("<") ?
                  <span style={{
                    maskImage: `url("data:image/svg+xml;base64,${btoa(icon)}")`,
                    backgroundColor: "currentColor",
                    maskRepeat: "no-repeat",
                    maskSize: "contain",
                    display: "inline-block"}}
                  /> :
                  <Icon
                    baseClassName={"material-icons-outlined"}
                    color={icon_color}
                  >
                    {icon}
                  </Icon>
              }
              checkedIcon={
                (active_icon && active_icon.trim().startsWith("<")) ?
                  <span style={{
                    maskImage: `url("data:image/svg+xml;base64,${btoa(active_icon)}")`,
                    backgroundColor: "currentColor",
                    maskRepeat: "no-repeat",
                    maskSize: "contain",
                    display: "inline-block"}}
                  /> :
                  <Icon color={active_color}>{active_icon}</Icon>
              }
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
              {action.icon && <Icon>{action.icon}</Icon>}
            </IconButton>)
        })}
        {menu_actions.length > 0 && (
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
              sx={{ml: "0.5em"}}
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
                    {action.icon && <Icon sx={{mr: "1em"}}>{action.icon}</Icon>}
                    {action.label}
                  </MenuItem>
                )
              })}
            </Menu>
          </React.Fragment>
        )}
        {subitems && (
          <IconButton
            size="small"
            onMouseDown={(e) => {
              e.stopPropagation()
            }}
            onClick={(e) => {
              e.stopPropagation()
              setOpen({...current_open, [key]: !current_open[key]})
            }}
          >
            {current_open[key] ? <ExpandLess/> : <ExpandMore />}
          </IconButton>
        )}
      </ListItemButton>
    )

    if (subitems) {
      return [
        list_item,
        <Collapse in={current_open[key]} timeout="auto" unmountOnExit>
          <List component="div" disablePadding dense={dense}>
            {subitems.map((subitem, index) => {
              return render_item(subitem, index, path, indent+1)
            })}
          </List>
        </Collapse>
      ]
    }
    return list_item
  }

  return (
    <List
      dense={dense}
      component="nav"
      sx={sx}
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
