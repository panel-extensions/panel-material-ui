import Button from "@mui/material/Button"
import Divider from "@mui/material/Divider"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import {CustomMenu} from "./menu"

export function render({model, el}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [items] = model.useState("items")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")
  const anchorEl = React.useRef(null)
  const [open, setOpen] = React.useState(false)

  return (
    <>
      <Button
        color={color}
        disabled={disabled}
        endIcon={<ArrowDropDownIcon />}
        loading={loading}
        onClick={() => setOpen(!open)}
        ref={anchorEl}
        size={size}
        startIcon={icon && (
          icon.trim().startsWith("<") ?
            <span style={{
              maskImage: `url("data:image/svg+xml;base64,${btoa(icon)}")`,
              backgroundColor: "currentColor",
              maskRepeat: "no-repeat",
              maskSize: "contain",
              width: icon_size,
              height: icon_size,
              display: "inline-block"}}
            /> :
            <Icon style={{fontSize: icon_size}}>{icon}</Icon>
        )}
        sx={sx}
        variant={variant}
      >
        {label}
      </Button>
      <CustomMenu
        anchorEl={() => anchorEl.current}
        open={open}
        onClose={() => setOpen(false)}
      >
        {items.map((item, index) => {
          if (item === null || item.label === "---") {
            return <Divider/>
          }
          return (
            <MenuItem
              key={`menu-item-${index}`}
              href={item.href}
              onClick={() => {
                setOpen(false)
                model.send_msg({type: "click", item: index})
              }}
              target={item.target}
            >
              {item.icon && (
                item.icon.trim().startsWith("<") ?
                  <span style={{
                    maskImage: `url("data:image/svg+xml;base64,${btoa(item.icon)}")`,
                    backgroundColor: "currentColor",
                    maskRepeat: "no-repeat",
                    maskSize: "contain",
                    width: icon_size,
                    height: icon_size,
                    display: "inline-block"}}
                  /> :
                  <Icon style={{fontSize: icon_size, paddingRight: "1.5em"}}>{item.icon}</Icon>
              )}
              {item.label}
            </MenuItem>
          )
        })}
      </CustomMenu>
    </>
  )
}
