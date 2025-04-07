import Avatar from "@mui/material/Avatar"
import Collapse from "@mui/material/Collapse"
import Divider from "@mui/material/Divider"
import ExpandLess from "@mui/icons-material/ExpandLess"
import ExpandMore from "@mui/icons-material/ExpandMore"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import List from "@mui/material/List"
import ListItem from "@mui/material/ListItem"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemAvatar from "@mui/material/ListItemAvatar"
import ListItemText from "@mui/material/ListItemText"
import ListSubheader from "@mui/material/ListSubheader"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"
import MoreVert from "@mui/icons-material/MoreVert"

export function render({model}) {
  const [dense] = model.useState("dense")
  const [label] = model.useState("label")
  const [items] = model.useState("items")
  const [sx] = model.useState("sx")
  const [open, setOpen] = React.useState({})
  const [menu_open, setMenuOpen] = React.useState({})
  const [menu_anchor, setMenuAnchor] = React.useState(null)
  const keys = Array.isArray(items) ? items.map((_, index) => index) : Object.keys(items)
  const current_open = {...open}
  const current_menu_open = {...menu_open}

  React.useEffect(() => {
    setOpen(current_open)
    setMenuOpen(current_menu_open)
  }, [])

  const render_item =(name, item, index, path, indent=0) => {
    if (path == null) {
      path = [name]
    } else {
      path = [...path, name]
    }
    const key = path.join(",")
    const isObject = (typeof item === "object" && item !== null)
    const label = isObject ? item.label : item
    if (label === "---" || label === null) {
      return <Divider key={`divider-${index}`}/>
    }
    const secondary = isObject ? item.secondary : null
    const actions = isObject ? item.actions : undefined
    const icon = isObject ? item.icon : undefined
    const avatar = isObject ? item.avatar : undefined
    const color = isObject ? item.color : undefined
    const subitems = isObject ? item.subitems : undefined
    const item_open = isObject ? item.open: true
    current_open[key] = current_open[key] === undefined ? item_open : current_open[key]
    current_menu_open[key] = current_menu_open[key] === undefined ? false : current_menu_open[key]

    let leadingComponent = null
    if (icon === null) {
      leadingComponent = null
    } else if (icon) {
      leadingComponent = (
        <ListItemIcon>
          <Icon color={color}>{icon}</Icon>
        </ListItemIcon>
      )
    } else {
      leadingComponent = (
        <ListItemAvatar>
          <Avatar size="small" variant="square" color={color}>{avatar || label[0].toUpperCase()}</Avatar>
        </ListItemAvatar>
      )
    }

    const list_item = (
      <ListItemButton onClick={() => { model.send_msg({type: "click", item: path}) }} sx={{p: `0 4px 0 ${(indent+1) * 8}px`}}>
        {leadingComponent}
        <ListItemText primary={label} secondary={secondary} />
        {subitems && (
          <IconButton size="small" onClick={(e) => { setOpen({...current_open, [key]: !current_open[key]}); e.stopPropagation() }}>
            {current_open[key] ? <ExpandLess/> : <ExpandMore />}
          </IconButton>
        )}
        {actions && (
          <React.Fragment>
            <IconButton
              size="small"
              onClick={(e) => {
                current_menu_open[key] = true
                setMenuOpen(current_menu_open)
                setMenuAnchor(e.currentTarget)
                e.stopPropagation()
              }}
            >
              <MoreVert />
            </IconButton>
            <Menu
              anchorEl={menu_anchor}
              open={current_menu_open[key]}
              onClose={() => setMenuOpen({...current_menu_open, [key]: false})}
            >
              {actions.map((action, index) => (
                <MenuItem
                  key={index}
                  onClick={() => {
                    model.send_msg({type: "action", action: action.action, item: path})
                  }}
                >
                  {action.icon && <Icon>{action.icon}</Icon>}
                  {action.label}
                </MenuItem>
              ))}
            </Menu>
          </React.Fragment>
        )}
      </ListItemButton>
    )

    if (subitems) {
      return [
        list_item,
        <Collapse in={current_open[key]} timeout="auto" unmountOnExit>
          <List component="div" disablePadding dense={dense}>
            {subitems.map((subitem, index) => {
              return render_item(index, subitem, index, path, indent+1)
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
      {keys.map((name, index) => render_item(name, items[name], index))}
    </List>
  )
}
