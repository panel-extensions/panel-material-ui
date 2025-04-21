import Avatar from "@mui/material/Avatar"
import SpeedDialIcon from "@mui/material/SpeedDialIcon"
import SpeedDialAction from "@mui/material/SpeedDialAction"
import SpeedDial from "@mui/material/SpeedDial"
import Icon from "@mui/material/Icon"

export function render({model, view}) {
  const [color] = model.useState("color")
  const [direction] = model.useState("direction")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [items] = model.useState("items")
  const [open_icon] = model.useState("open_icon")
  const [persistent_tooltips] = model.useState("persistent_tooltips")
  const [sx] = model.useState("sx")
  const [label] = model.useState("label")

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
      ariaLabel={label}
      direction={direction}
      FabProps={{color, disabled}}
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
      {items.map((item, index) => {
        const label = item.label
        const avatar = item.avatar || label[0].toUpperCase()
        return (
          <SpeedDialAction
            key={`speed-dial-action-${index}`}
            icon={item.icon ? (
              <Icon color={item.color}>{item.icon}</Icon>
            ) : (
              <Avatar color={item.color}>{avatar}</Avatar>
            )}
            tooltipTitle={item.label}
            tooltipOpen={persistent_tooltips}
            slotProps={{popper: {container: view.container}}}
            onClick={() => { model.send_msg({type: "click", item: index}) }}
          />
        )
      })}
    </SpeedDial>
  )
}
