import Avatar from "@mui/material/Avatar"
import Breadcrumbs from "@mui/material/Breadcrumbs"
import Link from "@mui/material/Link"
import Typography from "@mui/material/Typography"
import Icon from "@mui/material/Icon"
import NavigateNextIcon from "@mui/icons-material/NavigateNext"
import {useTheme, styled} from "@mui/material/styles"

const StyledAvatar = styled(Avatar)(({theme, color}) => ({
  backgroundColor: theme.palette[color]?.main,
  fontSize: "1em",
  width: 24,
  height: 24,
  marginRight: theme.spacing(0.5)
}))

export function render({model}) {
  const [color] = model.useState("color")
  const [items] = model.useState("items")
  const [max_items] = model.useState("max_items")
  const [separator] = model.useState("separator")
  const [sx] = model.useState("sx")
  const [active, setActive] = model.useState("active")

  const theme = useTheme()

  const breadcrumbItems = items.map((item, index) => {
    const color_string = index == active ? color : "inherit"
    const props = {
      color: color_string,
      key: index,
      onClick: () => {
        setActive(index)
        model.send_msg({type: "click", item: index})
      },
      sx: {display: "flex", alignItems: "center"}
    }
    if (typeof item === "object" && item !== null) {
      if (item.href && index < items.length - 1) {
        return (
          <Link href={item.href} {...props}>
            {item.icon ?
              <Icon color={color_string} sx={{mr: 0.5}}>{item.icon}</Icon> : null
            }
            {item.avatar ?
              <StyledAvatar color={color_string} theme={theme}>{item.avatar}</StyledAvatar> : null
            }
            {item.label}
          </Link>
        )
      } else {
        return (
          <Typography {...props}>
            {item.icon ? <Icon color={color_string} sx={{mr: 0.5}}>{item.icon}</Icon> : null}
            {item.avatar ?
              <StyledAvatar color={color_string} theme={theme}>{item.avatar}</StyledAvatar> : null
            }
            {item.label}
          </Typography>
        )
      }
    } else {
      if (index < items.length - 1) {
        return <Link {...props} href="#">{item}</Link>
      } else {
        return <Typography {...props}>{item}</Typography>
      }
    }
  })

  return (
    <Breadcrumbs
      maxItems={max_items || undefined}
      separator={separator || <NavigateNextIcon fontSize="small" />}
      sx={sx}
    >
      {breadcrumbItems}
    </Breadcrumbs>
  )
}
