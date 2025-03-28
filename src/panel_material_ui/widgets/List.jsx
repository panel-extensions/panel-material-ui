import Avatar from "@mui/material/Avatar"
import Divider from "@mui/material/Divider"
import Icon from "@mui/material/Icon"
import List from "@mui/material/List"
import ListItem from "@mui/material/ListItem"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemAvatar from "@mui/material/ListItemAvatar"
import ListItemText from "@mui/material/ListItemText"

export function render({model}) {
  const [items] = model.useState("items")
  const [sx] = model.useState("sx")
  const [dense] = model.useState("dense")
  const keys = Array.isArray(items) ? items.map((_, index) => index) : Object.keys(items)

  const listItems = keys.map((name, index) => {
    const item = items[name]
    const isObject = (typeof item === "object" && item !== null)
    const label = isObject ? item.label : item
    if (label === "---" || label === null) {
      return <Divider key={`divider-${index}`}/>
    }
    const secondary = isObject ? item.secondary : null
    const icon = isObject ? item.icon : undefined
    const avatar = isObject ? item.avatar : undefined
    const color = isObject ? item.color : undefined

    let leadingComponent = null
    if (icon) {
      leadingComponent = (
        <ListItemIcon>
          <Icon color={color}>{icon}</Icon>
        </ListItemIcon>
      )
    } else {
      leadingComponent = (
        <ListItemAvatar>
          <Avatar color={color}>{avatar || label[0].toUpperCase()}</Avatar>
        </ListItemAvatar>
      )
    }

    return (
      <ListItem
        component="div"
        key={name}
      >
        <ListItemButton onClick={() => model.send_msg(name)}>
          {leadingComponent}
          <ListItemText primary={label} secondary={secondary} />
        </ListItemButton>
      </ListItem>
    )
  })

  return (
    <List dense={dense} sx={sx}>
      {listItems}
    </List>
  )
}
