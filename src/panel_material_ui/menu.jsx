import React from "react"
import ClickAwayListener from "@mui/material/ClickAwayListener"
import Grow from "@mui/material/Grow"
import Menu from "@mui/material/Menu"
import Paper from "@mui/material/Paper"
import Popper from "@mui/material/Popper"

export function CustomMenu({open, anchorEl, onClose, children, sx}) {
  const nb = document.querySelector(".jp-NotebookPanel");

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
      style={{zIndex: 1500, width: anchorEl.current?.offsetWidth}}
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
              {children}
            </Paper>
          </ClickAwayListener>
        </Grow>
      )}
    </Popper>
  )
}
