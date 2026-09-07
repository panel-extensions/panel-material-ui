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

function useSubMenus() {
  const [state, setState] = React.useState({index: null, focus: false})
  return React.useMemo(() => ({
    openIndex: state.index,
    focus: state.focus,
    open: (index, focus) => setState({index, focus}),
    close: () => setState({index: null, focus: false}),
  }), [state])
}

// A closed menu keeps its React state (only its DOM is unmounted), so nested
// state has to be cleared or the submenu reappears when the menu reopens.
function useResetWhenClosed(open, subs) {
  React.useEffect(() => {
    if (!open && subs.openIndex !== null) { subs.close() }
  }, [open, subs])
}

function SubMenu({item, index, model, view, onCloseAll, path, subs}) {
  const anchorRef = React.useRef(null)
  const open = subs.openIndex === index
  const childSubs = useSubMenus()
  useResetWhenClosed(open, childSubs)

  const handleClose = () => {
    childSubs.close()
    subs.close()
  }

  return (
    <>
      <MenuItem
        ref={anchorRef}
        onClick={() => subs.open(index, true)}
        onMouseEnter={() => { if (!item.disabled) { subs.open(index, false) } }}
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
            {render_icon_text(item.hint)}
          </Typography>
        )}
        <ChevronRightIcon fontSize="small" sx={{ml: 1, color: "text.secondary"}} />
      </MenuItem>
      <CustomMenu
        anchorEl={() => anchorRef.current}
        open={open}
        onClose={handleClose}
        autoFocus={subs.focus}
        passthrough
        view={view}
        paperProps={{"data-menubar-surface": ""}}
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
            subs={childSubs}
          />
        ))}
      </CustomMenu>
    </>
  )
}

function MenuItemContent({item, index, model, view, onCloseAll, path, subs}) {
  // Hovering any non-submenu item dismisses a sibling submenu that was opened by hover.
  const onMouseEnter = () => subs.close()

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
            subs={subs}
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
        subs={subs}
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
        onMouseEnter={onMouseEnter}
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
            {render_icon_text(item.hint)}
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
        onMouseEnter={onMouseEnter}
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
            {render_icon_text(item.hint)}
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
      onMouseEnter={onMouseEnter}
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
          {render_icon_text(item.hint)}
        </Typography>
      )}
    </MenuItem>
  )
}

function TopLevelMenu({menu, menuIndex, model, view, color, size, bar}) {
  const anchorRef = React.useRef(null)
  const open = bar.openIndex === menuIndex
  const subs = useSubMenus()
  useResetWhenClosed(open, subs)

  const handleClose = () => {
    subs.close()
    bar.close()
  }

  return (
    <>
      <Button
        ref={anchorRef}
        color={color === "default" ? "inherit" : color}
        size={size}
        onClick={() => (open ? handleClose() : bar.open(menuIndex))}
        // Once one menu is open, moving along the bar switches menus without a click.
        onMouseEnter={() => {
          if (!menu.disabled && bar.openIndex !== null && !open) {
            subs.close()
            bar.open(menuIndex)
          }
        }}
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
        passthrough
        view={view}
        paperProps={{"data-menubar-surface": ""}}
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
            subs={subs}
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
  const bar = useSubMenus()
  const barRef = React.useRef(null)

  // Every menu in the bar is pointer-transparent, so dismissal is handled once
  // here: a single click or Escape anywhere outside the open menus closes the
  // whole cascade rather than peeling off one layer at a time.
  const anyOpen = bar.openIndex !== null
  React.useEffect(() => {
    if (!anyOpen) { return }
    const onPointerDown = (e) => {
      const path = e.composedPath ? e.composedPath() : [e.target]
      const inside = path.some((el) => (
        el?.dataset?.menubarSurface !== undefined || el === barRef.current
      ))
      if (!inside) { bar.close() }
    }
    const onKeyDown = (e) => { if (e.key === "Escape") { bar.close() } }
    document.addEventListener("pointerdown", onPointerDown, true)
    document.addEventListener("keydown", onKeyDown, true)
    return () => {
      document.removeEventListener("pointerdown", onPointerDown, true)
      document.removeEventListener("keydown", onKeyDown, true)
    }
  }, [anyOpen, bar])

  return (
    <Paper
      ref={barRef}
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
            bar={bar}
          />
        ))}
      </Toolbar>
    </Paper>
  )
}
