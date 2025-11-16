import Button from "@mui/material/Button"
import Divider from "@mui/material/Divider"
import MenuItem from "@mui/material/MenuItem"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp"
import {CustomMenu} from "./menu"

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [disable_elevation] = model.useState("disable_elevation")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [items] = model.useState("items")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [persistent] = model.useState("persistent")
  const [size] = model.useState("size")
  const [toggle_icon] = model.useState("toggle_icon")
  const [toggled, setToggled] = model.useState("toggled")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const [open, setOpen] = React.useState(false)
  const anchorEl = React.useRef(null)

  const handleItemClick = (event, index, item) => {
    // Prevent menu from closing when clicking on item in persistent mode
    if (persistent) {
      event.stopPropagation()
    }

    if (toggled) {
      const new_toggled = [...toggled]
      const idx = new_toggled.indexOf(index)
      if (idx > -1) {
        new_toggled.splice(idx, 1)
      } else {
        new_toggled.push(index)
      }
      setToggled(new_toggled)
    }
    // Send toggle_item message to toggle the item's state
    model.send_msg({type: "toggle_item", item: index})

    // Close menu if not persistent
    if (!persistent) {
      setOpen(false)
    }
  }

  const currentIcon = open && toggle_icon ? toggle_icon : icon
  const dropdownIcon = open ? <ArrowDropUpIcon /> : <ArrowDropDownIcon />

  return (
    <div ref={ref}>
      <Button
        color={color}
        disabled={disabled}
        disableElevation={disable_elevation}
        endIcon={dropdownIcon}
        loading={loading}
        onClick={() => setOpen(!open)}
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
            }}
            /> :
            <Icon fontSize={icon_size}>{currentIcon}</Icon>
        )}
        sx={sx}
        variant={variant}
        {...other}
      >
        {label}
      </Button>
      <CustomMenu
        anchorEl={() => anchorEl.current}
        open={open}
        // For persistent mode, we still want backdrop clicks to close the menu
        onClick={() => persistent || e.stopPropagation()}
        onClose={() => setOpen(false)}
      >
        {items.map((item, index) => {
          if (item === null || item.label === "---") {
            return <Divider key={`divider-${index}`} />
          }

          const itemToggled = toggled.includes(index)
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
                      width: item.icon_size || "1em",
                      height: item.icon_size || "1em",
                      display: "inline-block"
                    }}
                    /> :
                    <Icon style={{fontSize: item.icon_size}}>{itemIcon}</Icon>
                  }
                </ListItemIcon>
              )}
              <ListItemText>{item.label}</ListItemText>
            </MenuItem>
          )
        })}
      </CustomMenu>
    </div>
  )
}
