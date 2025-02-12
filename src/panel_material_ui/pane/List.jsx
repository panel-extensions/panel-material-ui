import Divider from "@mui/material/Divider";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import Icon from "@mui/material/Icon";
import ListItemText from "@mui/material/ListItemText";

export function render({model}) {
  const [items] = model.useState("items");

  const handleItemClick = (item, index) => {
    model.send_event("click", {index, item});
  };

  const listItems = items.map((item, index) => {
    const isObject = (typeof item === "object" && item !== null);
    const label = isObject ? item.label : item;
    if (label === "---") {
      return <Divider/>
    }
    const secondary = isObject ? item.secondary : null;
    const icon = isObject ? item.icon : undefined;
    const avatar = isObject ? item.avatar : undefined;

    let leadingComponent = null;
    if (avatar) {
      leadingComponent = (
        <ListItemAvatar>
          <Avatar>{avatar}</Avatar>
        </ListItemAvatar>
      );
    } else if (icon) {
      leadingComponent = (
        <ListItemIcon>
          <Icon>{icon}</Icon>
        </ListItemIcon>
      );
    }

    return (
      <ListItem
        component="div"
        key={index}
      >
        <ListItemButton onClick={() => handleItemClick(item, index)}>
          {leadingComponent}
          <ListItemText primary={label} secondary={secondary} />
        </ListItemButton>
      </ListItem>
    );
  });
  return (
    <List>
      {listItems}
    </List>
  );
}
