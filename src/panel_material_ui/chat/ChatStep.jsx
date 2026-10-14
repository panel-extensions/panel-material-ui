import * as React from "react"
import {styled} from "@mui/material/styles"
import Box from "@mui/material/Box"
import Card from "@mui/material/Card"
import CardContent from "@mui/material/CardContent"
import CardHeader from "@mui/material/CardHeader"
import StepProgress from "@mui/material/CircularProgress"
import Collapse from "@mui/material/Collapse"
import IconButton from "@mui/material/IconButton"
import CheckCircleIcon from "@mui/icons-material/CheckCircle"
import ErrorIcon from "@mui/icons-material/Error"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked"
import Typography from "@mui/material/Typography"
import {apply_flex, render_icon_text} from "../utils"

const STATUS_SIZE = 20
// Lines the body up with the title: header padding, status icon and its
// margin, minus the default 10px margin of the panes in the body.
const CONTENT_INSET = `calc(1em + ${STATUS_SIZE}px + 12px - 10px)`

function StatusIcon({status}) {
  const sx = {fontSize: STATUS_SIZE}
  let icon
  if (status === "running") {
    icon = <StepProgress size={STATUS_SIZE - 4} thickness={5} aria-hidden />
  } else if (status === "failed") {
    icon = <ErrorIcon color="error" sx={sx} />
  } else if (status === "success" || status === "completed") {
    icon = <CheckCircleIcon color="success" sx={sx} />
  } else {
    icon = <RadioButtonUncheckedIcon sx={{...sx, color: "text.disabled"}} />
  }
  return (
    <Box
      role="img"
      aria-label={status}
      sx={{display: "flex", alignItems: "center", justifyContent: "center", width: STATUS_SIZE, height: STATUS_SIZE}}
    >
      {icon}
    </Box>
  )
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

  if (model.header) {
    apply_flex(view.get_child_view(model.header), "row")
  }

  return (
    <Card
      raised={raised}
      elevation={elevation}
      variant={outlined ? "outlined" : "elevation"}
      sx={{
        display: "flex",
        flexDirection: "column",
        width: "100%",
        height: "100%",
        // An unelevated paper is darker than the elevated surfaces it sits on in dark mode.
        ...(outlined ? {bgcolor: "transparent"} : {}),
        ...sx
      }}
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
        avatar={<StatusIcon status={status} />}
        sx={{
          display: "flex",
          minWidth: 0,
          padding: "0.25em 0.5em 0.25em 1em",
          "& .MuiCardHeader-avatar": {mr: "12px"},
          "& .MuiCardHeader-content": {minWidth: 0},
          "& .MuiCardHeader-title .step-header": {minWidth: 0}
        }}
        title={model.header ? header : <Typography variant="subtitle2">{render_icon_text(title)}</Typography>}
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
            padding: `0 8px 0 ${CONTENT_INSET}`,
            "&:last-child": {
              pb: "8px",
            },
          }}
        >
          {objects}
        </CardContent>
      </Collapse>
    </Card>
  )
}
