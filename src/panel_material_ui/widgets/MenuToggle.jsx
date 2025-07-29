import Button from "@mui/material/Button"
import Divider from "@mui/material/Divider"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp"

export function render({model, el}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [items] = model.useState("items")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [persistent] = model.useState("persistent")
  const [size] = model.useState("size")
  const [active, setActive] = model.useState("active")
  const [toggle_icon] = model.useState("toggle_icon")
  const [toggled] = model.useState("toggled")
  const [sx] = model.useState("sx")
  const anchorEl = React.useRef(null)

  const handleToggle = () => {
    const newState = !active
    setActive(newState)
    model.send_msg({type: "toggle", active: newState})
  }

  const handleClose = () => {
    setActive(false)
    model.send_msg({type: "toggle", active: false})
  }

  const handleItemClick = (event, index, item) => {
    // Prevent menu from closing when clicking on item in persistent mode
    if (persistent) {
      event.stopPropagation()
    }

    // Send toggle_item message to toggle the item's state
    model.send_msg({type: "toggle_item", item: index})

    // Close menu if not persistent
    if (!persistent) {
      handleClose()
    }
  }

  const currentIcon = active && toggle_icon ? toggle_icon : icon
  const dropdownIcon = active ? <ArrowDropUpIcon /> : <ArrowDropDownIcon />

  const isItemToggled = (index) => {
    return toggled && toggled.includes(index)
  }

  return (
    <>
      <Button
        color={color}
        disabled={disabled}
        endIcon={dropdownIcon}
        loading={loading}
        onClick={handleToggle}
        ref={anchorEl}
        size={size}
        startIcon={currentIcon && (
          currentIcon.trim().startsWith("<") ?
            <span style={{
              maskImage: `url("data:image/svg+xml;base64,${btoa(currentIcon)}")`,
              backgroundColor: "currentColor",
              maskRepeat: "no-repeat",
              maskSize: "contain",
              width: icon_size,
              height: icon_size,
              display: "inline-block"
            }} /> :
            <Icon style={{fontSize: icon_size}}>{currentIcon}</Icon>
        )}
        sx={sx}
        variant="contained"
      >
        {label}
      </Button>
      <Menu
        anchorEl={anchorEl.current}
        open={active}
        onClose={handleClose}
        // For persistent mode, we still want backdrop clicks to close the menu
        MenuListProps={{
          // Prevent click propagation on the menu list itself
          onClick: persistent ? (e) => e.stopPropagation() : undefined
        }}
      >
        {items.map((item, index) => {
          if (item === null || item.label === "---") {
            return <Divider key={`divider-${index}`} />
          }

          const itemToggled = isItemToggled(index)
          const itemIcon = itemToggled && item.active_icon ? item.active_icon : item.icon
          const itemColor = itemToggled && item.active_color ? item.active_color : item.color

          return (
            <MenuItem
              key={`menu-item-${index}`}
              onClick={(e) => handleItemClick(e, index, item)}
              selected={itemToggled}
              sx={itemColor ? {color: itemColor} : {}}
            >
              {itemIcon && (
                <ListItemIcon sx={itemColor ? {color: itemColor} : {}}>
                  {itemIcon.trim().startsWith("<") ?
                    <span style={{
                      maskImage: `url("data:image/svg+xml;base64,${btoa(itemIcon)}")`,
                      backgroundColor: "currentColor",
                      maskRepeat: "no-repeat",
                      maskSize: "contain",
                      width: icon_size,
                      height: icon_size,
                      display: "inline-block"
                    }} /> :
                    <Icon style={{fontSize: icon_size}}>{itemIcon}</Icon>
                  }
                </ListItemIcon>
              )}
              <ListItemText>{item.label}</ListItemText>
            </MenuItem>
          )
        })}
      </Menu>
    </>
  )
}
