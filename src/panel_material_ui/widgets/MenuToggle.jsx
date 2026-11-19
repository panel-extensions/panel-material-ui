import Button from "@mui/material/Button"
import Divider from "@mui/material/Divider"
import MenuItem from "@mui/material/MenuItem"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp"
import {CustomMenu} from "./menu"
import {render_icon, render_icon_text} from "./utils"

export function render(props, ref) {
  const {model, host, view, el, data, ...other} = props
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
  const [toggled] = model.useState("toggled")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const [open, setOpen] = React.useState(false)
  const anchorEl = React.useRef(null)

  if (ref == null || (Object.entries(ref).length === 0 && ref.constructor === Object)) {
    ref = undefined
  }
  React.useEffect(() => {
    const focus_cb = (msg) => anchorEl.current?.focus()
    return model.on("msg", focus_cb)
  }, [])

  const handleItemClick = (event, index, item) => {
    // Prevent menu from closing when clicking on item in persistent mode
    if (persistent) {
      event.stopPropagation()
    }

    // Python owns `toggled`; flipping it here as well would race the message
    // and double-toggle once the model write reaches Python first.
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
        startIcon={currentIcon && render_icon(currentIcon, null, size, icon_size)}
        sx={sx}
        variant={variant}
        {...other}
      >
        {render_icon_text(label)}
      </Button>
      <CustomMenu
        anchorEl={() => anchorEl.current}
        open={open}
        // For persistent mode, we still want backdrop clicks to close the menu
        onClick={(event) => {
          if (!persistent) {
            event.stopPropagation()
          }
        }}
        onClose={() => setOpen(false)}
        host={host}
      >
        {items.map((item, index) => {
          if (item === null || item.label === "---") {
            return <Divider key={`divider-${index}`} />
          }

          const itemToggled = toggled.includes(index)
          const itemIcon = itemToggled && item.active_icon ? item.active_icon : item.icon
          const itemColor = itemToggled && item.active_color ? item.active_color : item.color

          const menuItem = (
            <MenuItem
              key={`menu-item-${index}`}
              onClick={(e) => handleItemClick(e, index, item)}
              selected={itemToggled}
              sx={itemColor ? {color: itemColor} : {}}
            >
              {itemIcon && (
                <ListItemIcon sx={itemColor ? {color: itemColor} : {}}>
                  {render_icon(itemIcon, null, null, item.icon_size)}
                </ListItemIcon>
              )}
              <ListItemText>{render_icon_text(item.label)}</ListItemText>
            </MenuItem>
          )
          if (item.tooltip) {
            return (
              <Tooltip
                key={`menu-item-tooltip-${index}`}
                title={render_icon_text(item.tooltip)}
                placement="right"
                disableInteractive
              >
                {menuItem}
              </Tooltip>
            )
          }
          return menuItem
        })}
      </CustomMenu>
    </div>
  )
}
