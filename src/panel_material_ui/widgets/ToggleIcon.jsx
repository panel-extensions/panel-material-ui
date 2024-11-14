import Checkbox from "@mui/material/Checkbox"
import Icon from "@mui/material/Icon";
import Tooltip from "@mui/material/Tooltip";

export function render({model, el}) {
  const [active_icon] = model.useState("active_icon")
  const [color] = model.useState("color")
  const [description] = model.useState("description")
  const [disabled] = model.useState("disabled")
  const [icon] = model.useState("icon")
  const [size] = model.useState("size")
  const [label] = model.useState("label")
  const [value, setValue] = model.useState("value")

  const checkbox = (
    <Checkbox
      checked={value}
      color={color}
      disabled={disabled}
      selected={value}
      size={size}
      onClick={(e, newValue) => setValue(!value)}
      icon={<Icon>{icon}</Icon>}
      checkedIcon={<Icon>{active_icon}</Icon>}
    />
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
    </Tooltip>) : checkbox
  )
}
