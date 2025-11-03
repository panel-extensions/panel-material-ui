import Avatar from "@mui/material/Avatar"
import Box from "@mui/material/Box"
import Breadcrumbs from "@mui/material/Breadcrumbs"
import Link from "@mui/material/Link"
import Typography from "@mui/material/Typography"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import MenuItem from "@mui/material/MenuItem"
import NavigateNextIcon from "@mui/icons-material/NavigateNext"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import {useTheme, styled} from "@mui/material/styles"
import {CustomMenu} from "./menu"

const StyledAvatar = styled(Avatar)(({color, spacing}) => ({
  backgroundColor: color,
  fontSize: "1em",
  width: 24,
  height: 24,
  marginRight: spacing
}))

function selectedRoot(items, active) {
  const roots = Array.isArray(items) ? items : [items]
  const rIdx = (active && active.length ? active[0] : 0) ?? 0
  return roots[rIdx] ?? roots[0] ?? null
}

function chainFromActive(items, active) {
  const chain = []
  const roots = Array.isArray(items) ? items : [items]
  if (!roots.length) { return chain }

  // depth 0: pick the root from active[0]
  let node = selectedRoot(items, active)
  if (!node) { return chain }
  chain.push(node)

  // depth >=1: walk children using active[1:], active[2:], ...
  for (let d = 1; d < (active?.length ?? 0); d++) {
    const idx = active[d] ?? 0
    const kids = Array.isArray(node.items) ? node.items : []
    if (!kids.length || idx < 0 || idx >= kids.length) { break }
    node = kids[idx]
    chain.push(node)
  }
  return chain
}

// Siblings available at a given depth
function siblingsForChainDepth(items, active, depth) {
  if (depth === 0) {
    // root-level siblings are the roots themselves
    return Array.isArray(items) ? items : [items]
  }
  const parentDepth = depth - 1
  const parentChain = chainFromActive(items, active.slice(0, parentDepth + 1))
  const parent = parentChain[parentDepth]
  return (parent && Array.isArray(parent.items)) ? parent.items : []
}

// Auto-descend tail (first-child path) starting from a node
function descendFirsts(node) {
  const tail = []
  let cur = node
  while (cur && Array.isArray(cur.items) && cur.items.length) {
    tail.push(0)
    cur = cur.items[0]
  }
  return tail
}

function overlapPrefix(a, b) {
  const out = []
  const n = Math.min(a.length, b.length)
  for (let i = 0; i < n; i++) {
    if (a[i] !== b[i]) { break }
    out.push(a[i])
  }
  return out
}

export function render({model}) {
  const [active, setActive] = model.useState("active")
  const [auto_descend] = model.useState("auto_descend")
  const [color] = model.useState("color")
  const [items] = model.useState("items")
  const [max_items] = model.useState("max_items")
  const [path] = model.useState("path")
  const [separator] = model.useState("separator")
  const [sx] = model.useState("sx")

  const theme = useTheme()

  let activeArr = Array.isArray(active)
    ? active : (active != null ? [active] : [])

  if (path && path.length) {
    const overlap = overlapPrefix(activeArr, path)
    if (overlap.length !== activeArr.length) {
      activeArr = overlap
      setActive(activeArr)
    }
  }

  // Resolved path for rendering depends on auto_descend
  const resolvedActive = React.useMemo(() => {
    if (!auto_descend) { return activeArr }
    const pathArr = path || (activeArr.length ? activeArr : [0])
    const ch = chainFromActive(items, pathArr)
    const last = ch.at(-1)
    const tail = last ? descendFirsts(last) : []
    return pathArr.concat(tail)
  }, [items, activeArr, path, auto_descend])

  // Build the visible chain from whichever path we render from
  const chain = React.useMemo(() => {
    return chainFromActive(items, resolvedActive)
  }, [items, resolvedActive])

  const explicitActiveDepth = activeArr.length - 1

  // If auto_descend is disabled and the last explicit node has children,
  // we show an extra *placeholder selector* segment at the end (unselected).
  const lastExplicitNode = chain.at(-1) || null
  const hasUnresolvedChildren =
    !auto_descend &&
    lastExplicitNode &&
    Array.isArray(lastExplicitNode.items) &&
    lastExplicitNode.items.length > 0

  // Menu UI state (single anchor, keyed by depth)
  const [menuDepth, setMenuDepth] = React.useState(null)
  const [anchorEl, setAnchorEl] = React.useState(null)

  function openMenu(event, depth) {
    setAnchorEl(event.currentTarget)
    setMenuDepth(depth)
  }

  function closeMenu() {
    setAnchorEl(null)
    setMenuDepth(null)
  }

  // Depth here is *chain index*. If we render the placeholder, its depth is chain.length.
  function siblingsAtDepth(depth) {
    if (depth === 0) { return Array.isArray(items) ? items : [] }
    // For placeholder depth === chain.length, siblings are children of lastExplicitNode
    const parent = depth === chain.length ? chain[depth - 1] : chain[depth - 1]
    return parent && Array.isArray(parent.items) ? parent.items : []
  }

  function selectedIdxAtDepth(depth, siblings) {
    // If placeholder depth (no explicit selection at that depth), return -1
    if ((hasUnresolvedChildren && depth === chain.length) || activeArr.length == 0) { return -1 }
    const idx = Number.isInteger(activeArr[depth]) ? activeArr[depth] : 0
    return idx >= 0 && idx < siblings.length ? idx : 0
  }

  function truncateTo(depth) {
    // Include the index for this depth, store explicitly up to this depth
    const base = resolvedActive.slice(0, depth + 1)
    setActive(base)

    const item = depth < chain.length ? chain[depth] : null
    const full = (() => {
      if (!auto_descend) { return base }
      const ch0 = chainFromActive(items, base)
      const last = ch0.at(-1)
      return base.concat(last ? descendFirsts(last) : [])
    })()

    model.send_msg({
      type: "click",
      item: base,   // explicit
      path: full    // resolved for rendering
    })
  }

  function selectAtDepth(depth, idx) {
    // Replace index at this depth
    const base = resolvedActive.slice(0, depth) // keep up to depth-1
    const newExplicit = base.concat([idx])      // set depth
    setActive(newExplicit)                      // store explicit

    const ch = chainFromActive(items, newExplicit)
    const item = ch.at(-1)
    const resolved = (() => {
      if (!auto_descend) { return newExplicit }
      return newExplicit.concat(item ? descendFirsts(item) : [])
    })()

    closeMenu()
    model.send_msg({
      type: "click",
      item: newExplicit, // explicit
      path: resolved     // resolved
    })
  }

  function renderSegment(item, depth) {
    const isActiveDepth = depth === explicitActiveDepth
    const colorStr = isActiveDepth ? color : "inherit"

    const labelBits = (
      <>
        {item.icon ? <Icon color={colorStr} sx={{mr: 0.5}}>{item.icon}</Icon> : null}
        {item.avatar ? (
          <StyledAvatar
            color={theme.palette[colorStr]?.main || colorStr}
            spacing={theme.spacing(0.5)}
            sx={{width: 24, height: 24, mr: 0.5}}
          >
            {item.avatar}
          </StyledAvatar>
        ) : null}
        {item.label}
      </>
    )

    const commonProps = {
      key: depth,
      color: colorStr,
      sx: {
        display: "inline-flex",
        alignItems: "center",
        lineHeight: 1.2
      },
      onClick: () => truncateTo(depth)
    }

    // Non-terminal segments can be links if href is provided
    const isLastRendered = depth === chain.length - 1 && !hasUnresolvedChildren
    if (!isLastRendered && item.href) {
      return (
        <Link href={item.href} target={item.target} {...commonProps}>
          {labelBits}
        </Link>
      )
    }
    return (
      <Typography {...commonProps}>
        {labelBits}
      </Typography>
    )
  }

  const breadcrumbItems = [
    // Render actual chain segments
    ...chain.map((item, depth) => {
      const seg = renderSegment(item, depth)
      const siblings = siblingsAtDepth(depth)
      const isOpen = menuDepth === depth
      const selectedIdx = selectedIdxAtDepth(depth, siblings)
      const showChevron = siblings.length > 1

      return (
        <span key={`seg-${depth}`} style={{display: "inline-flex", alignItems: "center"}}>
          {seg}
          {showChevron && (
            <>
              <IconButton
                size="small"
                aria-label="Change selection"
                onClick={(e) => openMenu(e, depth)}
                sx={{ml: 0.25}}
              >
                <ArrowDropDownIcon fontSize="small" />
              </IconButton>
              <CustomMenu anchorEl={anchorEl} open={isOpen} onClose={closeMenu} keepMounted>
                {siblings.map((sib, idx) => {
                  const isSelectable = sib.selectable ?? true
                  return (
                    <MenuItem
                      disabled={!isSelectable}
                      key={`d${depth}-i${idx}`}
                      selected={selectedIdx === idx}
                      onClick={() => isSelectable && selectAtDepth(depth, idx)}
                    >
                      {sib.icon ? <Icon sx={{mr: 1}}>{sib.icon}</Icon> : null}
                      {sib.avatar ? (
                        <StyledAvatar spacing={theme.spacing(0.5)} sx={{mr: 1}}>
                          {sib.avatar}
                        </StyledAvatar>
                      ) : null}
                      <Typography>{sib.label}</Typography>
                    </MenuItem>
                  )
                })}
              </CustomMenu>
            </>
          )}
        </span>
      )
    }),

    // If auto_descend is OFF and the last explicit node has children,
    // render a *placeholder* selector with NO selection.
    ...(hasUnresolvedChildren
      ? (() => {
        const depth = chain.length
        const siblings = siblingsAtDepth(depth)
        const isOpen = menuDepth === depth
        const selectedIdx = -1 // none selected

        return [
          <span key={`seg-placeholder-${depth}`} style={{display: "inline-flex", alignItems: "center"}}>
            <Typography
              key={depth}
              color="inherit"
              sx={{display: "inline-flex", alignItems: "center", lineHeight: 1.2, fontStyle: "italic"}}
              onClick={(e) => openMenu(e, depth)}
            >
                Select…
            </Typography>
            {siblings.length > 0 && (
              <>
                <IconButton
                  size="small"
                  aria-label="Choose item"
                  onClick={(e) => openMenu(e, depth)}
                  sx={{ml: 0.25}}
                >
                  <ArrowDropDownIcon fontSize="small" />
                </IconButton>
                <CustomMenu anchorEl={anchorEl} open={isOpen} onClose={closeMenu} keepMounted>
                  {siblings.map((sib, idx) => {
                    const isSelectable = sib.selectable ?? true
                    return (
                      <MenuItem
                        disabled={!isSelectable}
                        key={`d${depth}-i${idx}`}
                        selected={selectedIdx === idx /* always false */}
                        onClick={() => isSelectable && selectAtDepth(depth, idx)}
                      >
                        {sib.icon ? <Icon sx={{mr: 1}}>{sib.icon}</Icon> : null}
                        {sib.avatar ? (
                          <StyledAvatar spacing={theme.spacing(0.5)} sx={{mr: 1}}>
                            {sib.avatar}
                          </StyledAvatar>
                        ) : null}
                        <Typography>{sib.label}</Typography>
                      </MenuItem>
                    )
                  })}
                </CustomMenu>
              </>
            )}
          </span>
        ]
      })()
      : [])
  ]

  return (
    <Breadcrumbs
      maxItems={max_items || undefined}
      separator={separator || <NavigateNextIcon fontSize="small" />}
      sx={{
        ...sx,
        "& .MuiBreadcrumbs-li": {display: "flex", alignItems: "center"},
        "& .MuiBreadcrumbs-separator": {mx: 0.5, display: "flex", alignItems: "center"}
      }}
    >
      {breadcrumbItems}
    </Breadcrumbs>
  )
}
