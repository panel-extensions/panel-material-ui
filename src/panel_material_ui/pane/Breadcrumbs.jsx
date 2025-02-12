import Breadcrumbs from "@mui/material/Breadcrumbs";
import Link from "@mui/material/Link";
import Typography from "@mui/material/Typography";
import NavigateNextIcon from "@mui/icons-material/NavigateNext";

export function render({model}) {
  const [items] = model.useState("items");
  const [separator] = model.useState("separator");

  const breadcrumbItems = items.map((item, index) => {
    if (typeof item === "object" && item !== null) {
      if (item.href && index < items.length - 1) {
        return <Link key={index} color="inherit" href={item.href}>{item.label}</Link>;
      } else {
        return <Typography key={index} color="text.primary">{item.label}</Typography>;
      }
    } else {
      if (index < items.length - 1) {
        return <Link key={index} color="inherit" href="#">{item}</Link>;
      } else {
        return <Typography key={index} color="text.primary">{item}</Typography>;
      }
    }
  });

  return (
    <Breadcrumbs separator={separator || <NavigateNextIcon fontSize="small" />}>
      {breadcrumbItems}
    </Breadcrumbs>
  );
}
