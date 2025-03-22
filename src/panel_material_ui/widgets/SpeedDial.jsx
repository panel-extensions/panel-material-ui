import Avatar from "@mui/material/Avatar"
import SpeedDialIcon from "@mui/material/SpeedDialIcon"
import SpeedDialAction from "@mui/material/SpeedDialAction"
import SpeedDial from "@mui/material/SpeedDial"
import Icon from "@mui/material/Icon"

export function render({model, view}) {
  const [color] = model.useState("color")
  const [direction] = model.useState("direction")
  const [icon] = model.useState("icon")
  const [items] = model.useState("items")
  const [open_icon] = model.useState("open_icon")
  const [sx] = model.useState("sx")
  const [label] = model.useState("label")

  const keys = Array.isArray(items) ? items.map((_, index) => index) : Object.keys(items)
  const margin = (() => {
    switch (direction) {
      case "left":
        return {marginRight: "16px"}
      case "right":
        return {marginLeft: "16px"}
      case "up":
        return {marginBottom: "16px"}
      case "down":
        return {marginTop: "16px"}
      default:
        return {}
    }
  })()

  return (
    <SpeedDial
      FabProps={{color}}
      ariaLabel={label}
      direction={direction}
      icon={icon ? <Icon>{icon}</Icon> : <SpeedDialIcon openIcon={open_icon ? open_icon : undefined} />}
      sx={{
        "& .MuiSpeedDial-actions": {
          position: "absolute",
          zIndex: "calc(var(--mui-zIndex-fab) + 1)",
          ...margin
        },
        ...sx
      }}
    >
      {keys.map((name) => {
        const item = items[name]
        const avatar = item.avatar || item.label ? item.label[0].toUpperCase() : name[0].toUpperCase()
        return (
          <SpeedDialAction
            key={name}
            icon={item.icon ? (
              <Icon color={item.color}>{item.icon}</Icon>
            ) : (
              <Avatar color={item.color}>{avatar}</Avatar>
            )}
            tooltipTitle={item.label || name}
            slotProps={{popper: {container: view.container}}}
            onClick={() => { model.send_msg(name) }}
          />
        )
      })}
    </SpeedDial>
  )
}
