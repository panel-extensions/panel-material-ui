import ArrowBackIcon from "@mui/icons-material/ArrowBack"
import ArrowForwardIcon from "@mui/icons-material/ArrowForward"
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward"
import Box from "@mui/material/Box"
import Breadcrumbs from "@mui/material/Breadcrumbs"
import Checkbox from "@mui/material/Checkbox"
import ChevronRightIcon from "@mui/icons-material/ChevronRight"
import Chip from "@mui/material/Chip"
import Collapse from "@mui/material/Collapse"
import DeleteSweepIcon from "@mui/icons-material/DeleteSweep"
import Divider from "@mui/material/Divider"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"
import FolderIcon from "@mui/icons-material/Folder"
import IconButton from "@mui/material/IconButton"
import InputLabel from "@mui/material/InputLabel"
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile"
import Link from "@mui/material/Link"
import List from "@mui/material/List"
import ListItemButton from "@mui/material/ListItemButton"
import ListItemIcon from "@mui/material/ListItemIcon"
import ListItemText from "@mui/material/ListItemText"
import NavigateNextIcon from "@mui/icons-material/NavigateNext"
import Paper from "@mui/material/Paper"
import RefreshIcon from "@mui/icons-material/Refresh"
import TextField from "@mui/material/TextField"
import Tooltip from "@mui/material/Tooltip"
import Typography from "@mui/material/Typography"
import {render_description} from "./description"
import {formatBytes, render_icon_text} from "./utils"

const ROW_HEIGHT = "calc(1.25rem + 18px)"
// Matches the footprint of a size="small" Checkbox so rows without one stay aligned
const CHECKBOX_SIZE = 38

const ROOT_SX = {
  display: "flex",
  flexDirection: "column",
  gap: "0.5em",
  height: "100%",
  width: "100%"
}

function describe(item) {
  const parts = []
  if (item.size != null) {
    parts.push(formatBytes(item.size))
  }
  if (item.modified != null) {
    parts.push(new Date(item.modified * 1000).toLocaleString())
  }
  return parts.length ? parts.join(" \u2022 ") : null
}

export function render({model, el, view}) {
  const [can_back] = model.useState("_can_back")
  const [can_forward] = model.useState("_can_forward")
  const [can_up] = model.useState("_can_up")
  const [color] = model.useState("color")
  const [crumbs] = model.useState("_crumbs")
  const [directory, setDirectory] = model.useState("directory")
  const [disabled] = model.useState("disabled")
  const [items] = model.useState("_items")
  const [label] = model.useState("label")
  const [only_files] = model.useState("only_files")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")

  const [path, setPath] = React.useState(directory)
  const [expanded, setExpanded] = React.useState(false)

  const rootSx = React.useMemo(() => (sx ? [ROOT_SX, sx] : ROOT_SX), [sx])

  React.useEffect(() => setPath(directory), [directory])

  React.useEffect(() => {
    const cb = (msg) => {
      if (msg.type === "directory") {
        setPath(msg.directory)
      }
    }
    model.on("msg:custom", cb)
    return () => model.off("msg:custom", cb)
  }, [])

  const selected = React.useMemo(() => new Set(value), [value])

  const navigate = (target) => {
    if (disabled) {
      return
    }
    setPath(target)
    setDirectory(target)
  }

  const toggle = (item) => {
    if (disabled || item.parent || (only_files && item.type === "directory")) {
      return
    }
    setValue(
      selected.has(item.path) ?
        value.filter((p) => p !== item.path) :
        [...value, item.path]
    )
  }

  const selectable = (item) => !item.parent && !(only_files && item.type === "directory")

  // Selection chips are labelled relative to the root directory, which is the
  // first crumb, since absolute paths are too long to read in a chip.
  const relative = (target) => {
    const root = crumbs.length ? crumbs[0].path : null
    if (!root || !target.startsWith(root)) {
      return target
    }
    return target.slice(root.length).replace(/^[/\\]/, "") || crumbs[0].name
  }

  return (
    <Box sx={rootSx}>
      {label && (
        <InputLabel>
          {render_icon_text(label)}
          {model.description ? render_description({model, el, view}) : null}
        </InputLabel>
      )}
      <Paper
        sx={{display: "flex", flexDirection: "column", flexGrow: 1, minHeight: 0, overflow: "hidden"}}
        variant="outlined"
      >
        <Box className="file-selector-toolbar" sx={{alignItems: "center", display: "flex", gap: "4px", p: "4px"}}>
          <Tooltip title="Back">
            <IconButton
              aria-label="back"
              className="file-selector-back"
              disabled={disabled || !can_back}
              onClick={() => model.send_msg({type: "back"})}
              size="small"
            >
              <ArrowBackIcon fontSize="small"/>
            </IconButton>
          </Tooltip>
          <Tooltip title="Forward">
            <IconButton
              aria-label="forward"
              className="file-selector-forward"
              disabled={disabled || !can_forward}
              onClick={() => model.send_msg({type: "forward"})}
              size="small"
            >
              <ArrowForwardIcon fontSize="small"/>
            </IconButton>
          </Tooltip>
          <Tooltip title="Up">
            <IconButton
              aria-label="up"
              className="file-selector-up"
              disabled={disabled || !can_up}
              onClick={() => model.send_msg({type: "up"})}
              size="small"
            >
              <ArrowUpwardIcon fontSize="small"/>
            </IconButton>
          </Tooltip>
          <TextField
            className="file-selector-path"
            color={color}
            disabled={disabled}
            fullWidth
            onChange={(event) => setPath(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                navigate(path)
              }
            }}
            size="small"
            value={path || ""}
            variant="outlined"
          />
          <Tooltip title="Reload">
            <IconButton
              aria-label="reload"
              className="file-selector-reload"
              disabled={disabled}
              onClick={() => model.send_msg({type: "reload"})}
              size="small"
            >
              <RefreshIcon fontSize="small"/>
            </IconButton>
          </Tooltip>
        </Box>
        <Breadcrumbs
          className="file-selector-breadcrumbs"
          separator={<NavigateNextIcon fontSize="small"/>}
          sx={{p: "0 8px 4px"}}
        >
          {crumbs.map((crumb, index) => (
            index === crumbs.length - 1 ? (
              <Typography color="text.primary" key={crumb.path} variant="body2">
                {crumb.name}
              </Typography>
            ) : (
              <Link
                color={color === "default" ? "inherit" : color}
                component="button"
                key={crumb.path}
                onClick={() => navigate(crumb.path)}
                underline="hover"
                variant="body2"
              >
                {crumb.name}
              </Link>
            )
          ))}
        </Breadcrumbs>
        <Divider/>
        <List
          className="file-selector-items"
          dense
          sx={{
            flexGrow: 1,
            maxHeight: `calc(${ROW_HEIGHT} * ${size})`,
            overflow: "auto",
            py: 0
          }}
        >
          {items.map((item) => (
            <ListItemButton
              className={`file-selector-item file-selector-${item.type}`}
              disabled={disabled}
              key={item.path + item.name}
              onClick={() => (item.parent ? navigate(item.path) : toggle(item))}
              onDoubleClick={() => {
                if (item.type === "directory") {
                  navigate(item.path)
                }
              }}
              sx={{height: ROW_HEIGHT, px: "4px"}}
              title={describe(item) || undefined}
            >
              <ListItemIcon sx={{minWidth: 0}}>
                {selectable(item) ? (
                  <Checkbox
                    checked={selected.has(item.path)}
                    color={color}
                    disableRipple
                    onClick={(event) => {
                      event.stopPropagation()
                      toggle(item)
                    }}
                    size="small"
                    tabIndex={-1}
                  />
                ) : (
                  <Box sx={{height: CHECKBOX_SIZE, width: CHECKBOX_SIZE}}/>
                )}
              </ListItemIcon>
              <ListItemIcon sx={{minWidth: "32px"}}>
                {item.type === "directory" ?
                  <FolderIcon color="action" fontSize="small"/> :
                  <InsertDriveFileIcon color="action" fontSize="small"/>}
              </ListItemIcon>
              <ListItemText
                primary={item.name}
                slotProps={{primary: {noWrap: true, variant: "body2"}}}
              />
              {item.size != null && (
                <Typography color="text.secondary" sx={{ml: "8px", whiteSpace: "nowrap"}} variant="caption">
                  {formatBytes(item.size)}
                </Typography>
              )}
              {item.type === "directory" && (
                <IconButton
                  aria-label={`enter ${item.name}`}
                  className="file-selector-enter"
                  onClick={(event) => {
                    event.stopPropagation()
                    navigate(item.path)
                  }}
                  size="small"
                >
                  <ChevronRightIcon fontSize="small"/>
                </IconButton>
              )}
            </ListItemButton>
          ))}
        </List>
        <Divider/>
        <Box
          className="file-selector-selection"
          sx={{alignItems: "center", display: "flex", gap: "4px", p: "2px 4px"}}
        >
          <IconButton
            aria-label="toggle selection"
            className="file-selector-expand"
            onClick={() => setExpanded(!expanded)}
            size="small"
            sx={{transform: expanded ? "rotate(0deg)" : "rotate(-90deg)", transition: "transform 150ms"}}
          >
            <ExpandMoreIcon fontSize="small"/>
          </IconButton>
          <Typography
            onClick={() => setExpanded(!expanded)}
            sx={{cursor: "pointer", flexGrow: 1}}
            variant="body2"
          >
            {`Selected (${value.length})`}
          </Typography>
          <Tooltip title="Clear selection">
            <IconButton
              aria-label="clear selection"
              className="file-selector-clear"
              disabled={disabled || value.length === 0}
              onClick={() => setValue([])}
              size="small"
            >
              <DeleteSweepIcon fontSize="small"/>
            </IconButton>
          </Tooltip>
        </Box>
        <Collapse in={expanded} unmountOnExit>
          <Box sx={{display: "flex", flexWrap: "wrap", gap: "4px", maxHeight: "8em", overflow: "auto", p: "4px"}}>
            {value.map((selected_path) => (
              <Chip
                color={color}
                key={selected_path}
                label={relative(selected_path)}
                onDelete={disabled ? undefined : () => setValue(value.filter((p) => p !== selected_path))}
                size="small"
                title={selected_path}
                variant="outlined"
              />
            ))}
          </Box>
        </Collapse>
      </Paper>
    </Box>
  )
}
