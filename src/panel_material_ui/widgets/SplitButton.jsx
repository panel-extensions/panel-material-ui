import Button from "@mui/material/Button"
import ButtonGroup from "@mui/material/ButtonGroup"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import ClickAwayListener from "@mui/material/ClickAwayListener"
import MenuItem from "@mui/material/MenuItem"
import {CustomMenu} from "./menu"

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [active] = model.useState("active")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [items] = model.useState("items")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [mode] = model.useState("mode")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  const [open, setOpen] = React.useState(false)
  const [selectedIndex, setSelectedIndex] = React.useState(active)
  const anchorEl = React.useRef(null)

  const handleMenuItemClick = (event, selectedIndex) => {
    setSelectedIndex(selectedIndex)
    setOpen(false)
    model.send_msg({type: "click", item: selectedIndex})
  }

  const handleClose = (event) => {
    if (anchorEl.current && anchorEl.current.contains(event.target)) {
      return
    }
    setOpen(false)
  }

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = undefined
  }

  let current_icon = icon
  let current_label = label
  if (mode === "select") {
    current_label = items[active].label
    current_icon = items[active].icon ?? icon
  }

  return (
    <div ref={ref}>
      <ButtonGroup
        color={color}
        disabled={disabled}
        fullWidth
        ref={anchorEl}
        size={size}
        variant={variant}
        {...other}
      >
        <Button
          color={color}
          startIcon={current_icon && (
            current_icon.trim().startsWith("<") ?
              <span style={{
                maskImage: `url("data:image/svg+xml;base64,${btoa(current_icon)}")`,
                backgroundColor: "currentColor",
                maskRepeat: "no-repeat",
                maskSize: "contain",
                width: icon_size,
                height: icon_size,
                display: "inline-block"}}
              /> :
              <Icon style={{fontSize: icon_size}}>{current_icon}</Icon>
          )}
          loading={loading}
          onClick={() => model.send_msg({type: "click"})}
          sx={{
            ...sx,
            borderBottomRightRadius: 0,
            borderTopRightRadius: 0
          }}
          variant={variant}
        >
          {current_label}
        </Button>
        <Button
          aria-controls={open ? "split-button-menu" : undefined}
          aria-expanded={open ? "true" : undefined}
          aria-haspopup="menu"
          color={color}
          disabled={disabled || loading}
          onClick={() => setOpen((prevOpen) => !prevOpen)}
          size="small"
          sx={{
            borderBottomLeftRadius: 0,
            borderTopLeftRadius: 0,
            maxWidth: 50
          }}
          variant={variant}
        >
          <ArrowDropDownIcon />
        </Button>
      </ButtonGroup>
      <CustomMenu
        anchorEl={() => anchorEl.current}
        open={open}
        onClose={() => setOpen(false)}
      >
        {items.map((option, index) => (
          <MenuItem
            key={`menu-item-${index}`}
            component={option.href ? "a" : "li"}
            href={option.href}
            selected={mode === "select" && index === selectedIndex}
            onClick={(event) => handleMenuItemClick(event, index)}
            target={option.target}
          >
            {option.icon && (
              option.icon.trim().startsWith("<") ?
                <span style={{
                  maskImage: `url("data:image/svg+xml;base64,${btoa(option.icon)}")`,
                  backgroundColor: "currentColor",
                  maskRepeat: "no-repeat",
                  maskSize: "contain",
                  width: option.icon_size || "1em",
                  height: option.icon_size || "1em",
                  display: "inline-block"}}
                /> :
                <Icon style={{fontSize: option.icon_size || "1em", paddingRight: "1.5em"}}>{option.icon}</Icon>
            )}
            {option.label}
          </MenuItem>
        ))}
      </CustomMenu>
    </div>
  )
}
