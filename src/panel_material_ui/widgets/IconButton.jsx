import IconButton from "@mui/material/IconButton";
import Icon from "@mui/material/Icon";
import Tooltip from "@mui/material/Tooltip";

export function render({model, el}) {
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("button_type")
  const [description] = model.useState("description")
  const [disabled] = model.useState("disabled")
  const [edge] = model.useState("edge")
  const [icon] = model.useState("icon")
  const [size] = model.useState("size")
  const [toggle_duration] = model.useState("toggle_duration")
  const [current_icon, setIcon] = React.useState(icon)

  const handleClick = (e) => {
    model.send_event("click", e)
    if (active_icon) {
      setIcon(active_icon)
      setTimeout(() => setIcon(icon), toggle_duration)
    }
  }

  const button = (
    <IconButton
      color={color}
      disabled={disabled}
      edge={edge}
      size={size}
      onClick={handleClick}
    >
      <Icon style={{fontSize: size}}>{current_icon}</Icon>
    </IconButton>
  )

  return (description ? (
    <Tooltip
      title={description}
      arrow
      placement="right"
      PopperProps={{
        container: el
      }}
    >
      {button}
    </Tooltip>) : button
  )
}
