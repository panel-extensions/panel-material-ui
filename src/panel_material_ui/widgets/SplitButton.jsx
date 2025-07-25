import Button from "@mui/material/Button"
import ButtonGroup from "@mui/material/ButtonGroup"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import ClickAwayListener from "@mui/material/ClickAwayListener"
import Grow from "@mui/material/Grow"
import Paper from "@mui/material/Paper"
import Popper from "@mui/material/Popper"
import MenuItem from "@mui/material/MenuItem"
import MenuList from "@mui/material/MenuList"

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [active] = model.useState("active")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [items] = model.useState("items")
  const [label] = model.useState("label")
  const [mode] = model.useState("mode")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  const anchorEl = React.useRef(null)
  const [open, setOpen] = React.useState(false)
  const [selectedIndex, setSelectedIndex] = React.useState(active)

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

  let current_icon = icon
  let current_label = label
  if (mode === "select") {
    current_label = items[active].label
    current_icon = items[active].icon ?? icon
  }

  return (
    <>
      <ButtonGroup
        color={color}
        disabled={disabled}
        ref={anchorEl}
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
          variant={variant}
          onClick={() => model.send_msg({type: "click"})}
          sx={{
            ...sx,
            borderBottomRightRadius: 0,
            borderTopRightRadius: 0
          }}
        >
          {current_label}
        </Button>
        <Button
          variant={variant}
          color={color}
          size="small"
          aria-controls={open ? "split-button-menu" : undefined}
          aria-expanded={open ? "true" : undefined}
          aria-haspopup="menu"
          onClick={() => setOpen((prevOpen) => !prevOpen)}
          sx={{
            borderBottomLeftRadius: 0,
            borderTopLeftRadius: 0
          }}
        >
          <ArrowDropDownIcon />
        </Button>
      </ButtonGroup>
      <Popper
        sx={{zIndex: 1500}}
        open={open}
        anchorEl={anchorEl.current}
        role={undefined}
        placement="bottom-start"
        transition
        disablePortal
      >
        {({TransitionProps, placement}) => (
          <Grow
            {...TransitionProps}
            style={{
              transformOrigin:
                placement === "bottom" ? "center top" : "center bottom",
            }}
          >
            <Paper>
              <ClickAwayListener onClickAway={handleClose}>
                <MenuList id="split-button-menu" autoFocusItem>
                  {items.map((option, index) => (
                    <MenuItem
                      key={`menu-item-${index}`}
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
                            width: icon_size,
                            height: icon_size,
                            display: "inline-block"}}
                          /> :
                          <Icon style={{fontSize: icon_size, paddingRight: "1.5em"}}>{option.icon}</Icon>
                      )}
                      {option.label}
                    </MenuItem>
                  ))}
                </MenuList>
              </ClickAwayListener>
            </Paper>
          </Grow>
        )}
      </Popper>
    </>
  )
}
