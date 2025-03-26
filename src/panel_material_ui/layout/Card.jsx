import {styled} from "@mui/material/styles"
import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import CardHeader from "@mui/material/CardHeader"
import Collapse from "@mui/material/Collapse"
import IconButton from "@mui/material/IconButton"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"
import Typography from "@mui/material/Typography"

function set_flex(props) {
  const model = props.parent.model.data[props.name][props.index]
  const view = props.parent.get_child_view(model)
  if (view.el) {
    view.el.style.minHeight = "auto"
  }
}

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
}))

export function render({model, view}) {
  const [title] = model.useState("title")
  const [elevation] = model.useState("elevation")
  const [outlined] = model.useState("outlined")
  const [raised] = model.useState("raised")
  const [collapsible] = model.useState("collapsible")
  const [collapsed, setCollapsed] = model.useState("collapsed")
  const [sx] = model.useState("sx")
  const [hide_header] = model.useState("hide_header")
  const header = model.get_child("header")
  const objects = model.get_child("objects")

  model.on("after_layout", () => {
    for (const child_view of view.layoutable_views) {
      if (child_view.el) {
        child_view.el.style.minHeight = "auto"
      }
    }
  })

  return (
    <Card
      raised={raised}
      elevation={elevation}
      variant={outlined ? "outlined" : "elevation"}
      sx={{display: "flex", flexDirection: "column", width: "100%", height: "100%", ...sx}}
    >
      {!hide_header && (
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
          title={model.header ? header : <Typography variant="h6">{title}</Typography>}
        />
      )}
      <Collapse
        in={!collapsed}
        timeout="auto"
        unmountOnExit
        sx={{
          flexGrow: 1,
          height: "100%",
          width: "100%",
          "& .MuiCollapse-wrapper": {
            height: "100% !important",
          },
        }}
      >
        <CardContent
          sx={{
            height: "100%",
            width: "100%",
            display: "flex",
            flexDirection: "column",
            "&:last-child": {
              pb: "16px",
            },
          }}
        >
          {objects}
        </CardContent>
      </Collapse>
    </Card>
  );
}
