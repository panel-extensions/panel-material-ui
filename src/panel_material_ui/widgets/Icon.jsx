import Icon from '@mui/material/Icon';

export function render({model}) {
    const [icon] = model.useState("value")
    const [color] = model.useState("color")
    const [fontSize] = model.useState("font_size")
    const [sx] = model.useState("sx")
    console.log(fontSize)
    return (
      <Icon
        color={color}
        fontSize={fontSize}
        sx={sx}
      >{icon}
      </Icon>
    )
}
