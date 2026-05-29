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

export function CustomMenu({open, view, anchorEl, onClose, children, sx, keepMounted}) {
  const nb = detect_nb(view)
  if (nb == null) {
    return (
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={onClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        sx={sx}
        keepMounted={keepMounted}
      >
        {children}
      </Menu>
    )
  }

  return (
    <Popper
      open={open}
      anchorEl={anchorEl}
      placement="bottom-end"
      style={{zIndex: 1500, width: (anchorEl ? anchorEl.current : anchorEl)?.offsetWidth}}
    >
      {({TransitionProps, placement}) => (
        <Grow
          {...TransitionProps}
          style={{
            transformOrigin:
            placement === "bottom" ? "center top" : "center bottom",
          }}
        >
          <ClickAwayListener onClickAway={onClose}>
            <Paper elevation={3} sx={{overflowY: "auto", ...sx}}>
              <MenuList>
                {children}
              </MenuList>
            </Paper>
          </ClickAwayListener>
        </Grow>
      )}
    </Popper>
  )
}
