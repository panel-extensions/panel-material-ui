import React from "react"
import ClickAwayListener from "@mui/material/ClickAwayListener"
import Grow from "@mui/material/Grow"
import Menu from "@mui/material/Menu"
import MenuList from "@mui/material/MenuList"
import Paper from "@mui/material/Paper"
import Popper from "@mui/material/Popper"

export function detect_nb(view) {
  let nb = document.querySelector(".jp-NotebookPanel");
  let node = view.el
  while (node != null) {
    if (node.host != null) {
      node = node.host
    } else {
      node = node.parentNode
    }
    const cls = node?.className || ""
    if (cls.includes("react-flow") || cls.includes("muuri-grid")) {
      nb = true
    }
  }
  return nb
}

/**
 * `passthrough` opts a menu out of owning its own dismissal. The menu surface
 * stays interactive but everything around it is pointer-transparent, so hover
 * and clicks reach whatever sits behind, including sibling and ancestor menus.
 * A menu structure using it (e.g. MenuBar) is responsible for closing itself,
 * which lets one click away dismiss every open layer instead of just the
 * innermost one. `autoFocus={false}` additionally keeps a menu opened by hover
 * from stealing focus from the menu it was opened from.
 */
export function CustomMenu({open, view, anchorEl, onClose, children, sx, keepMounted, anchorOrigin, transformOrigin, placement, autoFocus, passthrough, paperProps}) {
  const nb = detect_nb(view)
  const unfocused = autoFocus === false

  if (nb == null) {
    return (
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={onClose}
        anchorOrigin={anchorOrigin || {
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={transformOrigin || {
          vertical: "top",
          horizontal: "right",
        }}
        sx={sx}
        keepMounted={keepMounted}
        hideBackdrop={passthrough}
        {...(unfocused ? {
          autoFocus: false,
          disableAutoFocus: true,
          disableAutoFocusItem: true,
          disableEnforceFocus: true,
          disableRestoreFocus: true,
        } : {})}
        slotProps={{
          root: passthrough ? {sx: {pointerEvents: "none"}} : undefined,
          paper: {
            ...paperProps,
            sx: {...(passthrough ? {pointerEvents: "auto"} : {}), ...paperProps?.sx},
          },
        }}
      >
        {children}
      </Menu>
    )
  }

  const resolvedPlacement = placement || "bottom-end"
  const popperWidth = resolvedPlacement.startsWith("right") || resolvedPlacement.startsWith("left")
    ? undefined
    : (anchorEl ? anchorEl.current : anchorEl)?.offsetWidth

  const paper = (
    <Paper
      elevation={3}
      {...paperProps}
      sx={{overflowY: "auto", ...sx, ...(passthrough ? {pointerEvents: "auto"} : {}), ...paperProps?.sx}}
    >
      <MenuList autoFocusItem={open && !unfocused}>
        {children}
      </MenuList>
    </Paper>
  )

  return (
    <Popper
      open={open}
      anchorEl={anchorEl}
      placement={resolvedPlacement}
      style={{zIndex: 1500, width: popperWidth, pointerEvents: passthrough ? "none" : undefined}}
    >
      {({TransitionProps, placement}) => (
        <Grow
          {...TransitionProps}
          style={{
            transformOrigin:
            placement === "bottom" ? "center top" : "center bottom",
          }}
        >
          {passthrough ? paper : <ClickAwayListener onClickAway={onClose}>{paper}</ClickAwayListener>}
        </Grow>
      )}
    </Popper>
  )
}
