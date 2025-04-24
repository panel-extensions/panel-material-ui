import Divider from "@mui/material/Divider"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"

export function render({model, view}) {
  const [dense] = model.useState("dense")
  const [items] = model.useState("items")
  const [open, setOpen] = model.useState("open")
  const [sx] = model.useState("sx")

  const keys = Array.isArray(items) ? items.map((_, index) => index) : Object.keys(items)
  const anchorEl = view.parent?.element_views.includes(view) ? view.parent.el : null

  return (
    <Menu
      anchorEl={anchorEl}
      container={view.container}
      dense={dense}
      onClose={() => setOpen(false)}
      open={open}
      sx={sx}
    >
      {keys.map((name) => {
        const item = items[name]
        if (item === null || item.label === "---") {
          return <Divider />
        }
        const label = item.label || name
        const props = {key: name, onClick: () => { model.send_msg(name) }}
        return (
          <MenuItem {...props}>
            {item.icon ? <Icon>{item.icon}</Icon> : null}
            {label}
          </MenuItem>
        )
      })}
    </Menu>
  )
}
