import Avatar from "@mui/material/Avatar"
import Box from "@mui/material/Box"
import Breadcrumbs from "@mui/material/Breadcrumbs"
import Link from "@mui/material/Link"
import Typography from "@mui/material/Typography"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import Menu from "@mui/material/Menu"
import MenuItem from "@mui/material/MenuItem"
import NavigateNextIcon from "@mui/icons-material/NavigateNext"
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown"
import { useTheme, styled } from "@mui/material/styles"

const StyledAvatar = styled(Avatar)(({ color, spacing }) => ({
  backgroundColor: color,
  fontSize: "1em",
  width: 24,
  height: 24,
  marginRight: spacing
}))

// ---------- helpers (correct depth mapping) ----------
function selectedRoot(items, active) {
  const roots = Array.isArray(items) ? items : [items]
  const rIdx = (active && active.length ? active[0] : 0) ?? 0
  return roots[rIdx] ?? roots[0] ?? null
}

function chainFromActive(items, active) {
  const chain = []
  const roots = Array.isArray(items) ? items : [items]
  if (!roots.length) return chain

  // depth 0: pick the root from active[0]
  let node = selectedRoot(items, active)
  if (!node) return chain
  chain.push(node)

  // depth >=1: walk children using active[1:], active[2:], ...
  for (let d = 1; d < (active?.length ?? 0); d++) {
    const idx = active[d] ?? 0
    const kids = Array.isArray(node.items) ? node.items : []
    if (!kids.length || idx < 0 || idx >= kids.length) break
    node = kids[idx]
    chain.push(node)
  }
  return chain
}

// Siblings available at a given depth
function siblingsAtDepth(items, active, depth) {
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


export function render({ model }) {
  const [active, setActive] = model.useState("active")
  const [color] = model.useState("color")
  const [items] = model.useState("items")
  const [max_items] = model.useState("max_items")
  const [separator] = model.useState("separator")
  const [sx] = model.useState("sx")

  const theme = useTheme()

  const activeArr = Array.isArray(active) ? active : (active != null ? [active] : (items.length ? [0] : []))
  const resolvedActive = React.useMemo(() => {
    const ch = chainFromActive(items, activeArr)
    const last = ch.at(-1)
    const tail = last ? descendFirsts(last) : []
    return activeArr.concat(tail)
  }, [items, activeArr])

  const chain = chainFromActive(items, resolvedActive)
  const explicitActiveDepth = Math.max(0, activeArr.length - 1)

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

  function siblingsAtDepth(depth) {
    // depth is the chain index: 0=root segment
    if (depth === 0) return Array.isArray(items) ? items : []
    const parent = chain[depth - 1]
    return parent && Array.isArray(parent.items) ? parent.items : []
  }

  function selectedIdxAtDepth(depth, siblings) {
    const idx = Number.isInteger(activeArr[depth]) ? activeArr[depth] : 0
    return idx >= 0 && idx < siblings.length ? idx : 0
  }

  function truncateTo(depth) {
    // active[d] exists for chain[d], so include it:
    const base = resolvedActive.slice(0, depth + 1)

    setActive(base) // store explicit only

    const item = chain[depth]
    const full = (() => {
      const ch0 = chainFromActive(items, base)
      const last = ch0.at(-1)
      return base.concat(last ? descendFirsts(last) : [])
    })()

    model.send_msg({
      type: "click",
      item: base,
      path: full
    })
  }

  function selectAtDepth(depth, idx) {
    // Replace index at this depth
    const base = resolvedActive.slice(0, depth)     // keep up to depth-1
    const newExplicit = base.concat([idx])          // set depth
    setActive(newExplicit)                          // store explicit

    const ch = chainFromActive(items, newExplicit)
    const item = ch.at(-1)
    const resolved = newExplicit.concat(item ? descendFirsts(item) : [])

    closeMenu()
    model.send_msg({
      type: "click",
      item: newExplicit,
      path: resolved
    })
  }

  function renderSegment(item, depth) {
    const isLast = depth === chain.length - 1
    const isActiveDepth = depth === explicitActiveDepth
    const colorStr = isActiveDepth ? color : "inherit"

    const labelBits = (
      <>
        {item.icon ? <Icon color={colorStr} sx={{ mr: 0.5 }}>{item.icon}</Icon> : null}
        {item.avatar ? (
          <StyledAvatar
            color={theme.palette[colorStr]?.main || colorStr}
            spacing={theme.spacing(0.5)}
            sx={{ width: 24, height: 24, mr: 0.5 }}
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

    if (!isLast && item.href) {
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

  const breadcrumbItems = chain.map((item, depth) => {
    const seg = renderSegment(item, depth)
    const siblings = siblingsAtDepth(depth)
    const isOpen = menuDepth === depth
    const selectedIdx = selectedIdxAtDepth(depth, siblings)

    return (
      <span key={`seg-${depth}`} style={{ display: "inline-flex", alignItems: "center" }}>
        {seg}
	{(siblings.length > 1) && (
	  <>
          <IconButton
            size="small"
            aria-label="Change selection"
            onClick={(e) => openMenu(e, depth)}
            sx={{ ml: 0.25 }}
          >
            <ArrowDropDownIcon fontSize="small" />
          </IconButton>
          <Menu anchorEl={anchorEl} open={isOpen} onClose={closeMenu} keepMounted>
            {siblings.map((sib, idx) => {
	      const isSelectable = sib.selectable ?? true
              return (
		<MenuItem
		  disabled={!isSelectable}
		  key={`d${depth}-i${idx}`}
		  selected={selectedIdx === idx}
		  onClick={() => isSelectable && selectAtDepth(depth, idx)}
		>
		  {sib.icon ? <Icon sx={{ mr: 1 }}>{sib.icon}</Icon> : null}
		  {sib.avatar ? (
                    <StyledAvatar spacing={theme.spacing(0.5)} sx={{ mr: 1 }}>
                      {sib.avatar}
                    </StyledAvatar>
		  ) : null}
		  <Typography>{sib.label}</Typography>
		</MenuItem>
	      )
	    })}
          </Menu>
	  </>
	)}
      </span>
    )
  })

  return (
    <Breadcrumbs
      maxItems={max_items || undefined}
      separator={separator || <NavigateNextIcon fontSize="small" />}
      sx={{
        ...sx,
        "& .MuiBreadcrumbs-li": { display: "flex", alignItems: "center" },
        "& .MuiBreadcrumbs-separator": { mx: 0.5, display: "flex", alignItems: "center" }
      }}
    >
      {breadcrumbItems}
    </Breadcrumbs>
  )
}
