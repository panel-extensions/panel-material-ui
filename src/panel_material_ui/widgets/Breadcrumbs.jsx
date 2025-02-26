import Breadcrumbs from "@mui/material/Breadcrumbs"
import Link from "@mui/material/Link"
import Typography from "@mui/material/Typography"
import Icon from "@mui/material/Icon"
import NavigateNextIcon from "@mui/icons-material/NavigateNext"

export function render({model}) {
  const [color] = model.useState("color")
  const [items] = model.useState("items")
  const [separator] = model.useState("separator")
  const [sx] = model.useState("sx")
  const [value] = model.useState("value")

  const keys = Array.isArray(items) ? items.map((_, index) => index) : Object.keys(items)
  const breadcrumbItems = keys.map((name, index) => {
    const item = items[name]
    const color_string = name == value ? color : "inherit"
    const props = {color: color_string, key: index, onClick: () => { model.send_msg(name) }}
    if (typeof item === "object" && item !== null) {
      if (item.href && index < items.length - 1) {
        return (
          <Link href={item.href} {...props}>
            {item.icon ? <Icon color={color_string}>{item.icon}</Icon> : null}
            {item.label}
          </Link>
        );
      } else {
        return (
          <Typography {...props}>
            {item.icon ? <Icon color={color_string}>{item.icon}</Icon> : null}
            {item.label}
          </Typography>
        );
      }
    } else {
      if (index < items.length - 1) {
        return <Link {...props} href="#">{item}</Link>;
      } else {
        return <Typography {...props}>{item}</Typography>;
      }
    }
  })

  return (
    <Breadcrumbs
      separator={separator || <NavigateNextIcon fontSize="small" />}
      sx={sx}
    >
      {breadcrumbItems}
    </Breadcrumbs>
  );
}
