import Button from "@mui/material/Button"
import Checkbox from "@mui/material/Checkbox"
import Divider from "@mui/material/Divider"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"
import ListSubheader from "@mui/material/ListSubheader"
import MenuItem from "@mui/material/MenuItem"
import Paper from "@mui/material/Paper"
import Radio from "@mui/material/Radio"
import Toolbar from "@mui/material/Toolbar"
import Typography from "@mui/material/Typography"
import ChevronRightIcon from "@mui/icons-material/ChevronRight"
import {CustomMenu} from "./menu"
import {render_icon, render_icon_text} from "./utils"

function SubMenu({item, index, model, view, onCloseAll, path}) {
  const [anchorEl, setAnchorEl] = React.useState(null)
  const open = Boolean(anchorEl)

  const handleOpen = (e) => {
    setAnchorEl(e.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <>
      <MenuItem
        onClick={handleOpen}
        disabled={item.disabled}
      >
        {item.icon && (
          <ListItemIcon sx={{minWidth: 28}}>
            {render_icon(item.icon, null, "small")}
          </ListItemIcon>
        )}
        <ListItemText>{render_icon_text(item.label)}</ListItemText>
        {item.hint && (
          <Typography variant="body2" sx={{ml: 2, color: "text.secondary"}}>
            {item.hint}
          </Typography>
        )}
        <ChevronRightIcon fontSize="small" sx={{ml: 1, color: "text.secondary"}} />
      </MenuItem>
      <CustomMenu
        anchorEl={() => anchorEl}
        open={open}
        onClose={handleClose}
        view={view}
        sx={{minWidth: 180, mt: -1}}
        anchorOrigin={{vertical: "top", horizontal: "right"}}
        transformOrigin={{vertical: 8, horizontal: "left"}}
        placement="right-start"
      >
        {item.items.map((subItem, subIndex) => (
          <MenuItemContent
            key={`sub-${path.join("-")}-${index}-${subIndex}`}
            item={subItem}
            index={subIndex}
            model={model}
            view={view}
            onCloseAll={() => { handleClose(); onCloseAll() }}
            path={[...path, index]}
          />
        ))}
      </CustomMenu>
    </>
  )
}

function MenuItemContent({item, index, model, view, onCloseAll, path}) {
  if (item === null || item.label === "---") {
    return <Divider key={`divider-${path.join("-")}-${index}`} />
  }

  if (item.group && item.items) {
    return (
      <div key={`group-${path.join("-")}-${index}`}>
        <ListSubheader sx={{lineHeight: "32px", userSelect: "none"}}>
          {item.icon && (
            <ListItemIcon sx={{minWidth: 28, verticalAlign: "middle", display: "inline-flex"}}>
              {render_icon(item.icon, null, "small")}
            </ListItemIcon>
          )}
          {render_icon_text(item.label)}
        </ListSubheader>
        {item.items.map((subItem, subIndex) => (
          <MenuItemContent
            key={`group-item-${path.join("-")}-${index}-${subIndex}`}
            item={subItem}
            index={subIndex}
            model={model}
            view={view}
            onCloseAll={onCloseAll}
            path={[...path, index]}
          />
        ))}
        <Divider />
      </div>
    )
  }

  if (item.items && !item.group) {
    return (
      <SubMenu
        key={`submenu-${path.join("-")}-${index}`}
        item={item}
        index={index}
        model={model}
        view={view}
        onCloseAll={onCloseAll}
        path={path}
      />
    )
  }

  if (item.checkbox !== undefined) {
    return (
      <MenuItem
        key={`checkbox-${path.join("-")}-${index}`}
        onClick={() => {
          model.send_msg({type: "checkbox", path: [...path, index], value: !item.checkbox})
        }}
        disabled={item.disabled}
        dense
      >
        <Checkbox
          checked={item.checkbox}
          size="small"
          sx={{p: 0, mr: 1}}
          tabIndex={-1}
          disableRipple
        />
        <ListItemText>{render_icon_text(item.label)}</ListItemText>
        {item.hint && (
          <Typography variant="body2" sx={{ml: 2, color: "text.secondary"}}>
            {item.hint}
          </Typography>
        )}
      </MenuItem>
    )
  }

  if (item.radio !== undefined) {
    return (
      <MenuItem
        key={`radio-${path.join("-")}-${index}`}
        onClick={() => {
          model.send_msg({type: "radio", path: [...path, index], value: item.radio})
        }}
        disabled={item.disabled}
        dense
      >
        <Radio
          checked={item._radio_selected || false}
          size="small"
          sx={{p: 0, mr: 1}}
          tabIndex={-1}
          disableRipple
        />
        <ListItemText>{render_icon_text(item.label)}</ListItemText>
        {item.hint && (
          <Typography variant="body2" sx={{ml: 2, color: "text.secondary"}}>
            {item.hint}
          </Typography>
        )}
      </MenuItem>
    )
  }

  return (
    <MenuItem
      key={`item-${path.join("-")}-${index}`}
      onClick={() => {
        model.send_msg({type: "click", path: [...path, index]})
        onCloseAll()
      }}
      disabled={item.disabled}
      dense
    >
      {item.icon && (
        <ListItemIcon sx={{minWidth: 28}}>
          {render_icon(item.icon, null, "small")}
        </ListItemIcon>
      )}
      <ListItemText>{render_icon_text(item.label)}</ListItemText>
      {item.hint && (
        <Typography variant="body2" sx={{ml: 2, color: "text.secondary"}}>
          {item.hint}
        </Typography>
      )}
    </MenuItem>
  )
}

function TopLevelMenu({menu, menuIndex, model, view, color, size}) {
  const [anchorEl, setAnchorEl] = React.useState(null)
  const open = Boolean(anchorEl)
  const anchorRef = React.useRef(null)

  const handleOpen = (e) => {
    anchorRef.current = e.currentTarget
    setAnchorEl(e.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  return (
    <>
      <Button
        color={color === "default" ? "inherit" : color}
        size={size}
        onClick={handleOpen}
        startIcon={menu.icon ? render_icon(menu.icon, null, "small") : undefined}
        sx={{
          textTransform: "none",
          minWidth: "auto",
          px: 1.5,
          fontWeight: open ? 600 : 400,
        }}
        disabled={menu.disabled}
      >
        {render_icon_text(menu.label)}
      </Button>
      <CustomMenu
        anchorEl={() => anchorRef.current}
        open={open}
        onClose={handleClose}
        view={view}
        sx={{minWidth: 200}}
        anchorOrigin={{vertical: "bottom", horizontal: "left"}}
        transformOrigin={{vertical: "top", horizontal: "left"}}
        placement="bottom-start"
      >
        {(menu.items || []).map((item, index) => (
          <MenuItemContent
            key={`menu-${menuIndex}-${index}`}
            item={item}
            index={index}
            model={model}
            view={view}
            onCloseAll={handleClose}
            path={[menuIndex]}
          />
        ))}
      </CustomMenu>
    </>
  )
}

export function render({model, view}) {
  const [items] = model.useState("items")
  const [color] = model.useState("color")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  const elevation = variant === "outlined" ? 0 : 1

  return (
    <Paper
      variant={variant}
      elevation={elevation}
      sx={{
        display: "flex",
        flexWrap: "wrap",
        alignItems: "center",
        px: 0.5,
        ...sx
      }}
    >
      <Toolbar variant="dense" disableGutters sx={{minHeight: "auto", gap: 0}}>
        {items.map((menu, index) => (
          <TopLevelMenu
            key={`top-menu-${index}`}
            menu={menu}
            menuIndex={index}
            model={model}
            view={view}
            color={color}
            size={size}
          />
        ))}
      </Toolbar>
    </Paper>
  )
}
