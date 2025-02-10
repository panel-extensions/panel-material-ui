import ToggleButton from "@mui/material/ToggleButton"
import Icon from "@mui/material/Icon";
import Tooltip from "@mui/material/Tooltip";

export function render({model, el}) {
  const [color] = model.useState("button_type")
  const [description] = model.useState("description")
  const [description_delay] = model.useState("description_delay")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [variant] = model.useState("button_style")
  const [value, setValue] = model.useState("value")

  const button = (
    <ToggleButton
      color={color}
      disabled={disabled}
      variant={variant}
      selected={value}
      onChange={(e, newValue) => setValue(!value)}
    >
      {icon && <Icon style={{fontSize: icon_size}}>{icon}</Icon>}
      {label}
    </ToggleButton>
  )

  return (description ? (
    <Tooltip
      title={description}
      enterDelay={description_delay}
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
