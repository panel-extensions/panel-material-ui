import {styled} from "@mui/material/styles"

import Box from "@mui/material/Box"
import Button from "@mui/material/Button"
import Checkbox from "@mui/material/Checkbox"
import Collapse from "@mui/material/Collapse"
import Divider from "@mui/material/Divider"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"
import Typography from "@mui/material/Typography"

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

    // spacing
    paddingTop: theme.spacing(0.75),
    paddingBottom: theme.spacing(0.75),
    paddingRight: theme.spacing(1.5),
    // base indent + per-level indent for nested nodes
    paddingLeft: theme.spacing(0.75),

    gap: theme.spacing(1),

    // default (unselected) appearance
    color: theme.palette.text.secondary,

    "&[data-selected]": showHighlight ? {
      backgroundColor: theme.palette[dataColor || "primary"].main,
      color: theme.palette[dataColor || "primary"].contrastText,
      fontWeight: 600,
      "& .MuiSvgIcon-root, & .MuiTypography-root": {
        color: theme.palette[dataColor || "primary"].contrastText
      },
    } : {
      fontWeight: 600,
    },

    "&[data-focused]": {
      outline: (props) =>
        `2px solid ${theme.palette[props["data-color"] || "primary"].main}`,
      outlineOffset: -2,
    },

    "&:not([data-selected]):hover": {
      backgroundColor: theme.palette.action.hover,
      color: theme.palette.text.primary,
    },
  })
})

function TransitionComponent(props) {
  return <Collapse {...props} />;
}

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
  const map = new Map()
  const visit = (nodes) => {
    nodes.forEach((node) => {
      if (!node || typeof node !== "object") {
        return
      }
      if (node.id) {
        map.set(node.id, node)
      }
      if (Array.isArray(node.children) && node.children.length) {
        visit(node.children)
      }
    })
  }
  visit(items)
  return map
}

const selectionsEqual = (current, next) => {
  if (Array.isArray(current) && Array.isArray(next)) {
    if (current.length !== next.length) {
      return false
    }
    return current.every((value, index) => value === next[index])
  }

  return current === next
}

/**
 * Slot component for RichTreeView.
 * Uses item metadata (`icon`, `file_type`) to choose the label icon.
 */
const CustomTreeItem = React.forwardRef(function CustomTreeItem(props, ref) {
  const {id, itemId, label, disabled, children, color, model, highlightSelection, ...other} = props

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
  } = useTreeItem({id, itemId, children, label, disabled, rootRef: ref})

  const item = useTreeItemModel(itemId)
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
  const [toggleValues, setToggleValues] = React.useState(new Map())

  const buildToggleKey = React.useCallback(
    (actionKey) => `${itemId}-${actionKey}`,
    [itemId]
  )

  React.useEffect(() => {
    const initial = new Map()
    inlineActions.forEach((action) => {
      if (action?.toggle) {
        const actionKey = action.action || action.label
        if (actionKey) {
          initial.set(buildToggleKey(actionKey), action.value ?? false)
        }
      }
    })
    setToggleValues(initial)
  }, [inlineActions, buildToggleKey])

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
      toggleValues.get(toggleKey) ?? action.value ?? false
    const newValue = !currentValue
    setToggleValues((prev) => {
      const next = new Map(prev)
      next.set(toggleKey, newValue)
      return next
    })
    sendAction(actionKey, newValue)
  }

  let IconComponent = null
  if (item && item.icon) {
    IconComponent = (iconProps) => <Icon {...iconProps}>{item.icon}</Icon>
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
        toggleValues.get(toggleKey) ?? action.value ?? false

      if (action.toggle) {
        const iconContent =
          typeof action.icon === "string" && action.icon.trim().startsWith("<") ? (
            <span
              style={{
                maskImage: `url("data:image/svg+xml;base64,${btoa(action.icon)}")`,
                backgroundColor: "currentColor",
                maskRepeat: "no-repeat",
                maskSize: "contain",
                display: "inline-block"
              }}
            />
          ) : (
            action.icon && (
              <Icon baseClassName={"material-icons-outlined"} color={action.color}>
                {action.icon}
              </Icon>
            )
          )
        const activeIconContent =
          typeof action.active_icon === "string" &&
          action.active_icon.trim().startsWith("<") ? (
              <span
                style={{
                  maskImage: `url("data:image/svg+xml;base64,${btoa(action.active_icon)}")`,
                  backgroundColor: "currentColor",
                  maskRepeat: "no-repeat",
                  maskSize: "contain",
                  display: "inline-block"
                }}
              />
            ) : (
              (action.active_icon || action.icon) && (
                <Icon color={action.active_color || action.color}>
                  {action.active_icon || action.icon}
                </Icon>
              )
            )
        return (
          <Checkbox
            key={`tree-action-toggle-${actionKey}`}
            checked={actionValue}
            color={action.color}
            disabled={disabled}
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
          sx={{ml: index > 0 ? 0 : 0.5}}
        >
          {action.icon && <Icon>{action.icon}</Icon>}
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
          startIcon={button.icon ? <Icon>{button.icon}</Icon> : null}
          onClick={(event) => {
            event.stopPropagation()
            if (!button.href) {
              event.preventDefault()
              sendAction(actionName, button.value)
            }
          }}
          sx={{ml: index ? 0.5 : 1}}
        >
          {button.label}
        </Button>
      )
    })

  return (
    <TreeItemProvider {...getContextProviderProps()}>
      <TreeItemRoot {...getRootProps(other)}>
        <TreeItemContent data-color={resolvedColor} data-highlight={highlightSelection} {...getContentProps()}>
          {children.length ? (
            <TreeItemIconContainer {...getIconContainerProps()}>
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
            <Box sx={{display: "flex", alignItems: "center", gap: 4, ml: "auto"}}>
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
                    sx={{ml: 0.5}}
                  >
                    <MoreVert />
                  </IconButton>
                  <Menu
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
                          {action.icon && <Icon sx={{mr: 1}}>{action.icon}</Icon>}
                          {action.label}
                        </MenuItem>
                      )
                    })}
                  </Menu>
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
  const [selected, setSelected] = model.useState("selected")
  const [expanded, setExpanded] = model.useState("expanded")
  const [multi_select] = model.useState("multi_select")
  const [item_children_indentation] = model.useState("item_children_indentation")
  const [propagate_to_parent] = model.useState("propagate_to_parent")
  const [propagate_to_child] = model.useState("propagate_to_child")
  const [show_children] = model.useState("show_children")
  const [sx] = model.useState("sx")

  const treeItems = React.useMemo(
    () => normalizeItems(items || [], show_children),
    [items, show_children]
  )

  const itemMetadata = React.useMemo(
    () => buildItemMetadata(treeItems),
    [treeItems]
  )

  const isItemSelectable = React.useCallback(
    (itemId) => {
      if (itemId == null) {
        return true
      }
      const meta = itemMetadata.get(itemId)
      if (!meta) {
        return true
      }
      if (meta.selectable === undefined) {
        return true
      }
      return meta.selectable
    },
    [itemMetadata]
  )

  const filterSelection = React.useCallback(
    (value) => {
      if (value == null) {
        return value
      }
      if (Array.isArray(value)) {
        return value.filter(isItemSelectable)
      }
      return isItemSelectable(value) ? value : selected
    },
    [isItemSelectable, selected]
  )

  const handleSelectedChange = (event, newSelected) => {
    const filteredSelection = filterSelection(newSelected)
    if (selectionsEqual(selected, filteredSelection)) {
      return
    }
    setSelected(filteredSelection)
    model.send_msg({
      type: "select",
      selected: filteredSelection
    })
  }

  const handleExpandedChange = (event, newExpanded) => {
    setExpanded(newExpanded)
    model.send_msg({
      type: "expand",
      expanded: newExpanded
    })
  }

  return (
    <RichTreeView
      items={treeItems}
      slots={{item: CustomTreeItem}}
      slotProps={{item: {color, model, highlightSelection: !checkboxes}}}
      selectedItems={selected}
      onSelectedItemsChange={handleSelectedChange}
      expandedItems={expanded}
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
