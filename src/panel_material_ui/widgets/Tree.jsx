import {styled} from "@mui/material/styles"

import Box from "@mui/material/Box"
import Button from "@mui/material/Button"
import Checkbox from "@mui/material/Checkbox"
import Collapse from "@mui/material/Collapse"
import Divider from "@mui/material/Divider"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import MenuItem from "@mui/material/MenuItem"
import Typography from "@mui/material/Typography"
import {parseIconName, render_icon} from "./utils"

import ArticleIcon from "@mui/icons-material/Article"
import DeleteIcon from "@mui/icons-material/Delete"
import FolderOpenIcon from "@mui/icons-material/FolderOpen"
import FolderRounded from "@mui/icons-material/FolderRounded"
import ImageIcon from "@mui/icons-material/Image"
import MoreVert from "@mui/icons-material/MoreVert"
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf"
import VideoCameraBackIcon from "@mui/icons-material/VideoCameraBack"

import {RichTreeView} from "@mui/x-tree-view/RichTreeView"
import {useTreeItem} from "@mui/x-tree-view/useTreeItem"
import {
  TreeItemCheckbox,
  TreeItemIconContainer,
  TreeItemLabel
} from "@mui/x-tree-view/TreeItem"
import {TreeItemIcon} from "@mui/x-tree-view/TreeItemIcon"
import {TreeItemProvider} from "@mui/x-tree-view/TreeItemProvider"
import {TreeItemDragAndDropOverlay} from "@mui/x-tree-view/TreeItemDragAndDropOverlay"
import {useTreeItemModel} from "@mui/x-tree-view/hooks"
import {CustomMenu} from "./menu"

const TreeItemRoot = styled("li")(({theme}) => ({
  listStyle: "none",
  margin: 0,
  padding: 0,
  outline: 0,
  color: theme.palette.grey[400],
  ...theme.applyStyles("light", {
    color: theme.palette.grey[800]
  })
}))

const TreeItemContent = styled("div")(({theme, ["data-color"]: dataColor, ["data-highlight"]: dataHighlight}) => {
  const showHighlight = dataHighlight !== false && dataHighlight !== "false"

  return ({
    display: "flex",
    alignItems: "center",
    width: "100%",
    boxSizing: "border-box",
    position: "relative",
    cursor: "pointer",
    WebkitTapHighlightColor: "transparent",
    paddingTop: theme.spacing(0.75),
    paddingBottom: theme.spacing(0.75),
    paddingRight: theme.spacing(1.5),
    // base indent + per-level indent for nested nodes
    paddingLeft: "10px",
    gap: theme.spacing(1),
    // default (unselected) appearance
    color: theme.palette.text.secondary,
    "&[data-disabled='true']": {
      color: "var(--mui-palette-text-disabled)"
    },
    // selected
    "&[data-selected]": (showHighlight ? (
      {
        backgroundColor: `rgba(var(--mui-palette-${dataColor}-mainChannel) / var(--mui-palette-action-selectedOpacity))`,
        borderLeft: `6px solid var(--mui-palette-${dataColor}-main)`,
        color: theme.palette.text.primary,
        fontWeight: 600,
        "& .MuiSvgIcon-root, & .MuiTypography-root": {
          color: theme.palette.text.primary
        },
        paddingLeft: "4px",
      }) : {fontWeight: 600}
    ),
    // focused
    "&[data-focused]": {
      outline: (props) => `2px solid ${theme.palette[props["data-color"] || "primary"].main}`,
      outlineOffset: -2,
    },
    // hovered
    "&:not([data-selected]):not([data-disabled='true']):hover": {
      backgroundColor: theme.palette.action.hover,
      color: theme.palette.text.primary,
    },
  })
})

const TreeItemLabelText = styled(Typography)({
  color: "inherit",
  fontWeight: 500
})

function CustomLabel({icon: IconComponent, expandable, children, secondary, ...other}) {
  return (
    <TreeItemLabel
      {...other}
      sx={{
        display: "flex",
        alignItems: "center",
        flex: 1,
        minWidth: 0
      }}
    >
      {IconComponent && (
        <Box
          component={IconComponent}
          className="labelIcon"
          color="inherit"
          sx={{mr: 1, fontSize: "1.2rem"}}
        />
      )}
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "flex-start",
          gap: secondary ? 0.25 : 0,
          minWidth: 0
        }}
      >
        <TreeItemLabelText
          variant="body2"
          sx={{
            width: "100%",
            whiteSpace: secondary ? "normal" : "nowrap",
            textOverflow: "ellipsis",
            overflow: "hidden"
          }}
        >
          {children}
        </TreeItemLabelText>
        {secondary ? (
          <Typography
            variant="caption"
            sx={{
              color: "inherit",
              opacity: 0.8,
              lineHeight: 1.2
            }}
          >
            {secondary}
          </Typography>
        ) : null}
      </Box>
    </TreeItemLabel>
  )
}

const getIconFromFileType = (fileType) => {
  switch (fileType) {
    case "image":
      return ImageIcon
    case "pdf":
      return PictureAsPdfIcon
    case "doc":
      return ArticleIcon
    case "video":
      return VideoCameraBackIcon
    case "folder":
      return FolderRounded
    case "pinned":
      return FolderOpenIcon
    case "trash":
      return DeleteIcon
    default:
      return ArticleIcon
  }
}

/**
 * Normalize Menu-style items (children in `items`) to the
 * shape expected by RichTreeView (`children`).
 */
const pathKey = (path) => (
  Array.isArray(path) && path.length ? path.join(",") : "root"
)

const generateNodeId = (path) => `pmui-${pathKey(path)}`

const normalizeItems = (items, showChildren, parentPath = []) => {
  if (!Array.isArray(items)) { return [] }

  return items
    .filter((item) => item && typeof item === "object")
    .map((item, index) => {
      const {items: childItems, ...rest} = item
      const hasChildren =
        showChildren && Array.isArray(childItems) && childItems.length > 0
      const currentPath = parentPath.concat(index)
      const normalized = {
        ...rest,
        id: rest.id ?? generateNodeId(currentPath),
        pmui_path: currentPath
      }

      if (!hasChildren) {
        return normalized
      }

      return {
        ...normalized,
        children: normalizeItems(childItems, showChildren, currentPath)
      }
    })
}

const buildItemMetadata = (items) => {
  const byId = new Map()
  const byPath = new Map()
  const visit = (nodes) => {
    nodes.forEach((node) => {
      if (!node || typeof node !== "object") {
        return
      }
      if (node.id) {
        byId.set(node.id, node)
      }
      if (Array.isArray(node.pmui_path)) {
        byPath.set(pathKey(node.pmui_path), node)
      }
      if (Array.isArray(node.children) && node.children.length) {
        visit(node.children)
      }
    })
  }
  visit(items)
  return {byId, byPath}
}

const isPathArray = (value) => (
  Array.isArray(value) && value.every((entry) => typeof entry === "number")
)

const pathEquals = (a, b) => {
  if (a === b) {
    return true
  }
  if (!Array.isArray(a) || !Array.isArray(b)) {
    return false
  }
  if (a.length !== b.length) {
    return false
  }
  return a.every((value, index) => value === b[index])
}

const selectionsEqual = (current, next, multiple) => {
  const currentList = Array.isArray(current) ? current : []
  const nextList = Array.isArray(next) ? next : []
  if (currentList.length !== nextList.length) {
    return false
  }
  return currentList.every((path, index) => pathEquals(path, nextList[index]))
}

const selectionEntryToPath = (entry, metadata) => {
  if (entry == null) {
    return null
  }
  if (isPathArray(entry)) {
    return entry
  }
  if (typeof entry === "number") {
    return [entry]
  }
  if (typeof entry === "string") {
    return metadata.byId.get(entry)?.pmui_path ?? null
  }
  return null
}

const selectionValueToPaths = (value, metadata) => {
  const entries = Array.isArray(value)
    ? value
    : value == null
      ? []
      : [value]
  return entries
    .map((entry) => selectionEntryToPath(entry, metadata))
    .filter((path) => Array.isArray(path))
}

const idToPath = (value, metadata) => {
  if (value == null) {
    return null
  }
  if (isPathArray(value)) {
    return value
  }
  return metadata.byId.get(value)?.pmui_path ?? null
}

const idsToPaths = (values, metadata) => {
  return values
    .map((entry) => idToPath(entry, metadata))
    .filter((path) => Array.isArray(path))
}

const pathToId = (path, metadata) => {
  if (!Array.isArray(path)) {
    return null
  }
  return metadata.byPath.get(pathKey(path))?.id ?? null
}

const pathsToIds = (value, metadata) => {
  return (value || [])
    .map((path) => pathToId(path, metadata))
    .filter((id) => id != null)
}

/**
 * Slot component for RichTreeView.
 * Uses item metadata (`icon`, `file_type`) to choose the label icon.
 */
const CustomTreeItem = React.forwardRef(function CustomTreeItem(props, ref) {
  const {id, itemId, label, children, color, model, highlightSelection, setToggleValues, toggle_ref, ...other} = props

  const item = useTreeItemModel(itemId)
  const {
    getContextProviderProps,
    getRootProps,
    getContentProps,
    getIconContainerProps,
    getCheckboxProps,
    getLabelProps,
    getGroupTransitionProps,
    getDragAndDropOverlayProps,
    status
  } = useTreeItem({id, itemId, children, label, disabled: item.disabled, rootRef: ref})

  const itemPath = item?.pmui_path
  const resolvedColor = (item && item.color) || color || "primary"
  const actions = Array.isArray(item?.actions) ? item.actions : []
  const inlineActions = actions.filter((action) => action && action.inline)
  const menuActions = actions.filter((action) => !action || !action.inline)
  const buttons = Array.isArray(item?.buttons)
    ? item.buttons.filter((button) => button)
    : []
  const secondary = item?.secondary

  const [menuAnchor, setMenuAnchor] = React.useState(null)
  const menuOpen = Boolean(menuAnchor)
  const iconContainerRef = React.useRef(null)

  const setAction = (key, value) => {
    const newMap = new Map(toggle_ref.current)
    newMap.set(key, value)
    setToggleValues(newMap)
    toggle_ref.current = newMap
  }

  React.useEffect(() => {
    const handler = (msg) => {
      if (msg.type == "toggle_action") {
        const toggle_key = buildToggleKey(msg.action)
        setAction(toggle_key, msg.value)
      }
    }
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [])

  const buildToggleKey = React.useCallback(
    (actionKey) => `${itemId}-${actionKey}`,
    [itemId]
  )

  const sendAction = React.useCallback(
    (actionName, value) => {
      if (!model || !actionName) {
        return
      }
      const payload = {
        type: "action",
        action: actionName,
        item: itemPath ?? []
      }
      if (value !== undefined) {
        payload.value = value
      }
      model.send_msg(payload)
    },
    [model, itemPath]
  )

  const handleToggleAction = (action) => {
    const actionKey = action.action || action.label
    if (!actionKey) {
      return
    }
    const toggleKey = buildToggleKey(actionKey)
    const currentValue =
      toggle_ref.current.get(toggleKey) ?? action.value ?? false
    const newValue = !currentValue
    const next = new Map(toggle_ref.current)
    next.set(toggleKey, newValue)
    toggle_ref.current = next
    setToggleValues(next)
    sendAction(actionKey, newValue)
  }

  let IconComponent = null
  if (item && item.icon) {
    const iconData = parseIconName(item.icon)
    IconComponent = (iconProps) => <Icon baseClassName={iconData.baseClassName} {...iconProps}>{iconData.iconName}</Icon>
  } else if (item && item.file_type) {
    IconComponent = getIconFromFileType(item.file_type)
  } else if (status.expandable) {
    IconComponent = FolderRounded
  }

  const checkboxProps = getCheckboxProps({
    sx: (theme) => {
      const c = theme.palette[resolvedColor] || theme.palette.primary
      return {
        color: theme.palette.text.secondary,
        "&.Mui-checked": {
          color: c.main
        }
      }
    }
  })

  const handleMenuOpen = (event) => {
    event.stopPropagation()
    setMenuAnchor(event.currentTarget)
  }

  const handleMenuClose = (event) => {
    if (event) {
      event.stopPropagation()
    }
    setMenuAnchor(null)
  }

  const renderInlineActions = () =>
    inlineActions.map((action, index) => {
      if (!action) {
        return null
      }
      const actionKey = action.action || action.label
      if (!actionKey) {
        return null
      }
      const toggleKey = buildToggleKey(actionKey)
      const actionValue =
        toggle_ref.current.get(toggleKey) ?? action.value ?? false

      if (action.toggle) {
        const active_icon = action.active_icon || action.icon
        const iconContent = typeof action.icon === "string" && (action.icon ? render_icon(action.icon, action.color, null, null, "-outlined") : undefined)
        const activeIconContent = typeof active_icon === "string" && (active_icon ? render_icon(active_icon, action.active_color || action.color) : undefined)
        return (
          <Checkbox
            key={`tree-action-toggle-${actionKey}`}
            checked={actionValue}
            color={action.color}
            disabled={item.disabled}
            size="small"
            onMouseDown={(event) => {
              event.stopPropagation()
              event.preventDefault()
            }}
            onClick={(event) => {
              event.stopPropagation()
              event.preventDefault()
              handleToggleAction(action)
            }}
            icon={iconContent}
            checkedIcon={activeIconContent}
          />
        )
      }

      return (
        <IconButton
          color={action.color}
          key={`tree-action-inline-${actionKey}`}
          size="small"
          title={action.label}
          onMouseDown={(event) => {
            event.stopPropagation()
            event.preventDefault()
          }}
          onClick={(event) => {
            event.stopPropagation()
            event.preventDefault()
            sendAction(actionKey)
          }}
        >
          {action.icon && render_icon(action.icon)}
        </IconButton>
      )
    })

  const renderButtons = () =>
    buttons.map((button, index) => {
      if (!button || !button.label) {
        return null
      }
      const actionName = button.action || button.label
      return (
        <Button
          key={`tree-button-${itemId}-${index}`}
          color={button.color || resolvedColor}
          variant={button.variant || "text"}
          size={button.size || "small"}
          href={button.href}
          target={button.target}
          startIcon={button.icon && render_icon(button.icon)}
          onClick={(event) => {
            event.stopPropagation()
            if (!button.href) {
              event.preventDefault()
              sendAction(actionName, button.value)
            }
          }}
          sx={{ml: index ? 0.25 : 0.5}}
        >
          {button.label}
        </Button>
      )
    })

  const contentProps = getContentProps()
  const iconContainerProps = getIconContainerProps()

  // Wrap content onClick to prevent selection when clicking icon container
  const wrappedContentProps = {
    ...contentProps,
    ["data-disabled"]: item.disabled ?? false,
    onClick: (event) => {
      // Check if click originated from icon container
      if (iconContainerRef.current && iconContainerRef.current.contains(event.target)) {
        return
      }
      if (contentProps.onClick) {
        contentProps.onClick(event)
      }
    }
  }

  return (
    <TreeItemProvider {...getContextProviderProps()}>
      <TreeItemRoot {...getRootProps(other)}>
        <TreeItemContent data-color={resolvedColor} data-highlight={highlightSelection} {...wrappedContentProps}>
          {children.length ? (
            <TreeItemIconContainer
              {...iconContainerProps}
              ref={iconContainerRef}
            >
              <TreeItemIcon status={status} />
            </TreeItemIconContainer>
          ) : null}

          <TreeItemCheckbox {...checkboxProps} />

          <CustomLabel
            {...getLabelProps({
              icon: IconComponent,
              expandable: status.expandable && status.expanded,
              secondary
            })}
          />

          {(buttons.length || inlineActions.length || menuActions.length) ? (
            <Box sx={{display: "flex", alignItems: "center", gap: 1, ml: "auto"}}>
              {renderButtons()}
              {renderInlineActions()}
              {menuActions.length ? (
                <React.Fragment>
                  <IconButton
                    size="small"
                    onMouseDown={(event) => {
                      event.stopPropagation()
                    }}
                    onClick={handleMenuOpen}
                    sx={{color: "text.secondary"}}
                  >
                    <MoreVert />
                  </IconButton>
                  <CustomMenu
                    anchorEl={menuAnchor}
                    open={menuOpen}
                    onClose={handleMenuClose}
                  >
                    {menuActions.map((action, index) => {
                      if (action === null) {
                        return <Divider key={`tree-action-divider-${index}`} />
                      }
                      const actionKey = action.action || action.label
                      if (!actionKey) {
                        return null
                      }
                      return (
                        <MenuItem
                          key={`tree-action-menu-${actionKey}`}
                          onMouseDown={(event) => {
                            event.stopPropagation()
                          }}
                          onClick={(event) => {
                            event.stopPropagation()
                            handleMenuClose(event)
                            sendAction(actionKey)
                          }}
                        >
                          {action.icon && render_icon(action.icon)}
                          {action.label}
                        </MenuItem>
                      )
                    })}
                  </CustomMenu>
                </React.Fragment>
              ) : null}
            </Box>
          ) : null}

          <TreeItemDragAndDropOverlay {...getDragAndDropOverlayProps()} />
        </TreeItemContent>

        {children.length ? <Collapse {...getGroupTransitionProps()} /> : null}
      </TreeItemRoot>
    </TreeItemProvider>
  )
})

export function render({model}) {
  const [checkboxes] = model.useState("checkboxes")
  const [color] = model.useState("color")
  const [items] = model.useState("items")
  const [selected, setSelected] = model.useState("active")
  const [expanded, setExpanded] = model.useState("expanded")
  const [multi_select] = model.useState("multi_select")
  const [item_children_indentation] = model.useState("level_indent")
  const [propagate_to_parent] = model.useState("propagate_to_parent")
  const [propagate_to_child] = model.useState("propagate_to_child")
  const [show_children] = model.useState("show_children")
  const [sx] = model.useState("sx")

  const [toggleValues, setToggleValues] = React.useState(new Map())
  const toggle_ref = React.useRef(toggleValues)

  const treeItems = React.useMemo(
    () => normalizeItems(items || [], show_children),
    [items, show_children]
  )

  const itemMetadata = React.useMemo(
    () => buildItemMetadata(treeItems),
    [treeItems]
  )

  const allowMultipleSelection = multi_select || checkboxes

  const isPathSelectable = React.useCallback(
    (path) => {
      if (!Array.isArray(path)) {
        return true
      }
      const meta = itemMetadata.byPath.get(pathKey(path))
      if (!meta || meta.selectable === undefined) {
        return true
      }
      return meta.selectable
    },
    [itemMetadata]
  )

  const selectedPaths = React.useMemo(
    () => selectionValueToPaths(selected, itemMetadata),
    [selected, itemMetadata]
  )

  const selectedIds = React.useMemo(
    () => pathsToIds(selectedPaths, itemMetadata),
    [selectedPaths, itemMetadata, allowMultipleSelection]
  )

  const expandedPaths = React.useMemo(
    () => idsToPaths(expanded, itemMetadata),
    [expanded, itemMetadata]
  )

  const expandedIds = React.useMemo(
    () => pathsToIds(expandedPaths, itemMetadata),
    [expandedPaths, itemMetadata]
  )

  const filterSelection = React.useCallback(
    (value) => {
      if (!value) {
        return []
      }
      return value.filter(isPathSelectable)
    },
    [allowMultipleSelection, isPathSelectable, selectedPaths]
  )

  const handleSelectedChange = (_, newSelected) => {
    const selectedIds = allowMultipleSelection ? newSelected : [newSelected]
    const newSelectionPaths = idsToPaths(selectedIds, itemMetadata)
    const filteredSelection = filterSelection(newSelectionPaths)
    if (filteredSelection.length === 0 && newSelected.length > 0) {
      // If a selectable=False item is selected, do not clear the selection
      return
    }
    if (!selectionsEqual(selectedPaths, filteredSelection)) {
      setSelected(filteredSelection.slice().reverse())
    }
  }

  const handleExpandedChange = (_, newExpanded) => {
    const nextExpandedPaths = idsToPaths(newExpanded, itemMetadata)
    if (!selectionsEqual(expandedPaths, nextExpandedPaths)) {
      setExpanded(nextExpandedPaths.slice().reverse())
    }
  }

  return (
    <RichTreeView
      expansionTrigger="iconContainer"
      items={treeItems}
      isItemDisabled={(item) => item.disabled ?? false}
      slots={{item: CustomTreeItem}}
      slotProps={{item: {color, model, highlightSelection: !checkboxes, setToggleValues, toggle_ref}}}
      selectedItems={selectedIds}
      onSelectedItemsChange={handleSelectedChange}
      expandedItems={expandedIds}
      onExpandedItemsChange={handleExpandedChange}
      multiSelect={multi_select}
      checkboxSelection={checkboxes}
      itemChildrenIndentation={item_children_indentation}
      selectionPropagation={{descendants: propagate_to_child, parent: propagate_to_parent}}
      sx={{
        height: "fit-content",
        flexGrow: 1,
        maxWidth: 400,
        overflowY: "auto",
        ...(sx || {})
      }}
    />
  )
}
