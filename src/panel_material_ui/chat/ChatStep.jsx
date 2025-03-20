import {styled} from "@mui/material/styles"
import Avatar from "@mui/material/Avatar"
import Box from "@mui/material/Box"
import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import CardHeader from "@mui/material/CardHeader"
import Collapse from "@mui/material/Collapse"
import IconButton from "@mui/material/IconButton"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"

function set_flex(props) {
  const model = props.parent.model.data[props.name][props.index]
  const view = props.parent.get_child_view(model)
  if (view.el) {
    view.el.style.minHeight = "auto"
  }
}

const status_colors = {
  "failed": "red",
  "success": "green",
  "pending": "transparent",
  "running": "gold",
  "completed": "green"
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
}));

export function render({model, view}) {
  const [collapsible] = model.useState("collapsible")
  const [collapsed, setCollapsed] = model.useState("collapsed")
  const [hide_header] = model.useState("hide_header")
  const [elevation] = model.useState("elevation")
  const [title] = model.useState("title")
  const [outlined] = model.useState("outlined")
  const [raised] = model.useState("raised")
  const [sx] = model.useState("sx")
  const header = model.get_child("header")
  const objects = model.get_child("objects")
  const [status] = model.useState("status")

  React.useEffect(() => {
    view.update_layout()
  }, [])

  model.on("after_layout", () => {
    for (const child_view of view.layoutable_views) {
      if (view.el) {
        view.el.style.minHeight = "auto"
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
        avatar={
          <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            mr: 2
          }}
        >
          <Box
            sx={{
              width: 15,
              height: 15,
              borderRadius: '50%',
              border: '1px solid',
              borderColor: 'black',
              bgcolor: status_colors[status]
            }}
          />
        </Box>
        }
        sx={{
          padding: "0.5em 0.5em 0.5em 1em",
        }}
        title={model.header ? header : <Typography variant="h8">{title}</Typography>}
      />
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
            padding: "0 8px 0 16px",
            "&:last-child": {
              pb: "0px",
            },
          }}
        >
          {objects.map((object) => {
            set_flex(object.props)
            return object
          })}
        </CardContent>
      </Collapse>
    </Card>
  )
}
