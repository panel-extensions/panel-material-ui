import {styled} from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardHeader from "@mui/material/CardHeader";
import Collapse from "@mui/material/Collapse";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const ExpandMore = styled((props) => {
  const {expand, ...other} = props;
  return <IconButton {...other} />;
})(({theme}) => ({
  marginLeft: "auto",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
  variants: [
    {
      props: ({expand}) => !expand,
      style: {
        transform: "rotate(0deg)",
      },
    },
    {
      props: ({expand}) => !!expand,
      style: {
        transform: "rotate(180deg)",
      },
    },
  ],
}));

export function render({model}) {
  const [title] = model.useState("title");
  const [elevation] = model.useState("elevation");
  const [outlined] = model.useState("outlined");
  const [raised] = model.useState("raised");
  const [collapsible] = model.useState("collapsible");
  const [collapsed, setCollapsed] = model.useState("collapsed");
  const header = model.get_child("header");
  const objects = model.get_child("objects");

  return (
    <Card
      raised={raised}
      elevation={elevation}
      variant={outlined ? "outlined" : "elevation"}
    >
      {title && (
        <CardHeader
          action={
            collapsible &&
            <ExpandMore
              expand={!collapsed}
              onClick={() => setCollapsed(!collapsed)}
              aria-expanded={!collapsed}
              aria-label="show more"
            >
              <ExpandMoreIcon />
            </ExpandMore>
          }
          title={title}
        >{header}</CardHeader>
      )}
      <Collapse in={!collapsed} timeout="auto" unmountOnExit>
        <CardContent>
          {objects}
        </CardContent>
      </Collapse>
    </Card>
  );
}
