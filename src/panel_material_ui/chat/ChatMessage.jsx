import Avatar from "@mui/material/Avatar"
import Box from "@mui/material/Box"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import Paper from "@mui/material/Paper"
import Stack from "@mui/material/Stack"
import Tooltip from "@mui/material/Tooltip"
import Typography from "@mui/material/Typography"
import CheckIcon from "@mui/icons-material/Check"
import ContentCopyIcon from "@mui/icons-material/ContentCopy"
import EditOutlinedIcon from "@mui/icons-material/EditOutlined"
import {parseIconName, render_icon_text} from "./utils"

const AVATAR_SIZE = 32

// Bubble-scoped overrides read by _MESSAGE_STYLESHEET, since links and inline
// code use the primary and hover colors that vanish on a primary background.
const BUBBLE_VARS = {
  "--pmui-chat-link-color": "currentColor",
  "--pmui-chat-code-bg": "rgba(255, 255, 255, 0.18)",
}
const ICON_SX = {fontSize: 16}

function PlaceholderDots() {
  const dot = (delay) => ({
    width: 8,
    height: 8,
    borderRadius: "50%",
    bgcolor: "text.disabled",
    animation: "pmui-chat-pulse 1.4s ease-in-out infinite",
    animationDelay: delay,
    "@keyframes pmui-chat-pulse": {
      "0%, 80%, 100%": {opacity: 0.3, transform: "scale(0.7)"},
      "40%": {opacity: 1, transform: "scale(1)"},
    },
    "@media (prefers-reduced-motion: reduce)": {
      animation: "none",
      opacity: 0.6,
    },
  })
  return (
    <Box
      role="status"
      aria-label="Waiting for response"
      sx={{display: "flex", alignItems: "center", gap: 0.75, height: AVATAR_SIZE, px: "10px"}}
    >
      <Box sx={dot("0s")} />
      <Box sx={dot("0.2s")} />
      <Box sx={dot("0.4s")} />
    </Box>
  )
}

function isEmoji(str) {
  return /\p{Extended_Pictographic}|\p{Regional_Indicator}/u.test(str)
}

function ActionButton({label, onClick, children, className = "chat-message-hover", ...props}) {
  return (
    <Tooltip title={label} placement="top" disableInteractive>
      <IconButton
        size="small"
        aria-label={label}
        className={className}
        onClick={onClick}
        sx={{color: "text.secondary", p: "4px"}}
        {...props}
      >
        {children}
      </IconButton>
    </Tooltip>
  )
}

export function render({model, view}) {
  const [placement] = model.useState("placement")
  const [elevation] = model.useState("elevation")
  const [user] = model.useState("user")
  const [show_avatar] = model.useState("show_avatar")
  const [show_edit_icon] = model.useState("show_edit_icon")
  const [show_user_param] = model.useState("show_user")
  const [auto_user] = model.useState("_internal_state.show_user")
  const show_user = show_user_param === "auto" ? auto_user : show_user_param
  const [show_timestamp] = model.useState("show_timestamp")
  const [show_reaction_icons] = model.useState("show_reaction_icons")
  const [show_copy_icon] = model.useState("show_copy_icon")
  const [reaction_options] = model.useState("_internal_state.reaction_options")
  const [reactions] = model.useState("reactions")
  const [avatar] = model.useState("_internal_state.avatar")
  const [timestamp] = model.useState("_internal_state.timestamp")
  const [grouped] = model.useState("_internal_state.grouped")
  const [has_text] = model.useState("_internal_state.has_text")
  const [is_help] = model.useState("_internal_state.help")
  const object = model.get_child("_object_panel")

  const header = model.get_child("header_objects")
  const footer = model.get_child("footer_objects")

  const [copied, setCopied] = React.useState(false)
  React.useEffect(() => {
    let timer = null
    const onMsg = (msg) => {
      if (msg.type !== "copy") { return }
      navigator.clipboard.writeText(msg.text).then(() => {
        setCopied(true)
        clearTimeout(timer)
        timer = setTimeout(() => setCopied(false), 1500)
      })
    }
    model.on("msg:custom", onMsg)
    return () => {
      model.off("msg:custom", onMsg)
      clearTimeout(timer)
    }
  }, [])

  const right = placement === "right"
  const placeholder = avatar.type === "text" && avatar.text === "PLACEHOLDER"
  // Grouped and help messages keep the avatar column so their content stays aligned.
  const hide_identity = grouped || is_help
  // Without elevation, own messages get a filled bubble and others render
  // directly on the feed; any elevation restores the classic paper card.
  const flat = !elevation
  const bubble = flat && right
  const name_height = show_user && !hide_identity ? AVATAR_SIZE / 2 : 0

  let avatar_component = null
  if (show_avatar && (hide_identity || placeholder)) {
    avatar_component = <Box sx={{width: AVATAR_SIZE, flexShrink: 0}} />
  } else if (show_avatar) {
    const emoji = avatar.type === "text" && isEmoji(avatar.text)
    avatar_component = (
      <Avatar
        alt={typeof user === "string" ? user : undefined}
        src={avatar.type === "image" ? avatar.src : null}
        sx={{
          width: AVATAR_SIZE,
          height: AVATAR_SIZE,
          flexShrink: 0,
          // Centers the avatar on the first line of the message rather than the name.
          mt: `${name_height + (bubble ? 4 : 0)}px`,
          fontSize: emoji ? "1.1rem" : "0.875rem",
          bgcolor: "background.paper",
          border: 1,
          borderColor: "divider",
          color: "text.primary",
        }}
      >
        {avatar.type !== "image" && (avatar.type === "text" ? (emoji ? avatar.text : [...avatar.text][0]) : (() => {
          const iconData = parseIconName(avatar.icon)
          return <Icon baseClassName={iconData.baseClassName} sx={{fontSize: 18}}>{iconData.iconName}</Icon>
        })())}
      </Avatar>
    )
  }

  const obj_model = view.model.data._object_panel
  const isResponsive = obj_model.sizing_mode && (obj_model.sizing_mode.includes("width") || obj_model.sizing_mode.includes("both"))

  const paperRef = React.useRef(null)

  // Detect when the edit area is swapped into the Paper and stretch width accordingly.
  const [isEditing, setIsEditing] = React.useState(false)
  React.useEffect(() => {
    if (!paperRef.current) { return }
    const observer = new MutationObserver(() => {
      setIsEditing(!!paperRef.current?.querySelector(".edit-area"))
    })
    observer.observe(paperRef.current, {childList: true, subtree: true})
    return () => observer.disconnect()
  }, [])

  // Find and cache the scrollable feed ancestor once on mount.
  // Walk up from view.el, crossing shadow DOM boundaries via getRootNode().host.
  const scrollContainerRef = React.useRef(null)
  // Track whether the user has manually scrolled up. Reset when they
  // scroll back near the bottom. This lets us distinguish "user scrolled
  // up to read history" from "content grew and pushed the scroll position".
  const userScrolledUpRef = React.useRef(false)
  React.useEffect(() => {
    let el = view.el
    while (el) {
      // +1 accounts for subpixel rounding differences across browsers
      if (el.scrollHeight > el.clientHeight + 1) {
        const style = getComputedStyle(el)
        if (style.overflowY === "auto" || style.overflowY === "scroll") {
          scrollContainerRef.current = el
          break
        }
      }
      if (el.parentElement) {
        el = el.parentElement
      } else {
        const root = el.getRootNode()
        el = root instanceof ShadowRoot ? root.host : null
      }
    }
    // Listen for user-initiated scroll events on the feed container.
    const feed = scrollContainerRef.current
    if (!feed) { return }
    let prevScrollTop = feed.scrollTop
    const onScroll = () => {
      const currentTop = feed.scrollTop
      const distFromBottom = feed.scrollHeight - currentTop - feed.clientHeight
      if (currentTop < prevScrollTop) {
        userScrolledUpRef.current = true
      } else if (distFromBottom < 50) {
        userScrolledUpRef.current = false
      }
      prevScrollTop = currentTop
    }
    feed.addEventListener("scroll", onScroll)
    return () => feed.removeEventListener("scroll", onScroll)
  }, [])

  React.useEffect(() => {
    if (!paperRef.current || (view.parent?.model.type != "panel.models.feed.Feed")) { return }
    let layoutTimer = null
    const observer = new ResizeObserver(() => {
      // Debounce layout invalidation to avoid thrashing during streaming.
      clearTimeout(layoutTimer)
      layoutTimer = setTimeout(() => view.invalidate_layout(), 50)
      // Scroll the feed to show new/expanded content after React paints,
      // but only if the user hasn't manually scrolled up.
      if (!userScrolledUpRef.current) {
        requestAnimationFrame(() => {
          const feed = scrollContainerRef.current
          if (feed) {
            feed.scrollTop = feed.scrollHeight
          }
        })
      }
    })
    observer.observe(paperRef.current)
    return () => {
      observer.disconnect()
      clearTimeout(layoutTimer)
    }
  }, [])

  // Unboxed content keeps Panel's default 10px pane margin, so the name and
  // actions are inset to line up with the text.
  const inset = flat && !right ? "10px" : 0
  const paper_sx = {
    bgcolor: flat ? (bubble && !isEditing ? "primary.main" : "transparent") : "background.paper",
    borderRadius: bubble ? 3 : undefined,
    p: bubble ? "4px" : 0,
    color: is_help ? "text.secondary" : (bubble && !isEditing ? "primary.contrastText" : "text.primary"),
    ...(bubble && !isEditing ? BUBBLE_VARS : {}),
    maxWidth: bubble && !isEditing ? "80%" : "100%",
    minWidth: 0,
    width: (isResponsive || isEditing) ? "100%" : "fit-content",
  }

  const show_copy = show_copy_icon && has_text
  const show_edit = show_edit_icon && has_text
  const reaction_names = show_reaction_icons ? Object.keys(reaction_options) : []
  const has_footer = footer?.length > 0
  const has_meta = show_copy || show_edit || reaction_names.length > 0 || (show_timestamp && !is_help)

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: right ? "row-reverse" : "row",
        alignItems: "flex-start",
        gap: 1.5,
        maxWidth: "100%",
        pt: hide_identity ? 0 : 1,
        // Active reactions stay visible; other actions appear on hover or focus.
        "& .chat-message-hover": {
          opacity: 0,
          transition: (theme) => theme.transitions.create("opacity", {duration: theme.transitions.duration.shorter}),
        },
        "&:hover .chat-message-hover, &:focus-within .chat-message-hover": {opacity: 1},
        "@media (hover: none)": {"& .chat-message-hover": {opacity: 1}},
      }}
    >
      {avatar_component}
      {placeholder ? (
        <Stack direction="row" spacing={1} sx={{alignItems: "center", minWidth: 0}}>
          <PlaceholderDots />
          {has_text && object}
        </Stack>
      ) : (
        <Stack
          direction="column"
          spacing={0}
          sx={{flexGrow: 1, minWidth: 0, alignItems: right ? "flex-end" : "flex-start"}}
        >
          {show_user && !hide_identity && (
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{fontWeight: 500, lineHeight: `${name_height}px`, pl: inset}}
            >
              {render_icon_text(user)}
            </Typography>
          )}
          <Stack direction="column" spacing={0}>
            {header}
          </Stack>
          <Paper ref={paperRef} elevation={elevation} sx={paper_sx}>
            {object}
          </Paper>
          {(has_footer || has_meta) && (
            <Stack
              direction={right ? "row-reverse" : "row"}
              spacing={1}
              // Line the leading item up with the content edge: footer panes
              // keep Panel's default 10px margin, which on the right would
              // inset them from the bubble, and icon buttons have 4px padding.
              sx={{
                alignItems: "center",
                ...(has_footer
                  ? {mt: 0.5, mr: right ? "-10px" : 0}
                  : {ml: right ? 0 : (flat ? "6px" : "-4px"), mr: right ? "-4px" : 0})
              }}
            >
              {has_footer && (
                <Stack direction="column" spacing={0} sx={{alignItems: right ? "flex-end" : "flex-start"}}>
                  {footer}
                </Stack>
              )}
              {has_meta && (
                <Stack
                  className="chat-message-meta"
                  direction={right ? "row-reverse" : "row"}
                  spacing={0.25}
                  sx={{alignItems: "center", minHeight: 24}}
                >
                  {/* Reactions lead the row so active ones sit at the content edge while the rest is hidden. */}
                  {reaction_names.map((reaction) => {
                    const active = reactions.includes(reaction)
                    const {icon, active_icon} = reaction_options[reaction]
                    return (
                      <ActionButton
                        key={`reaction-${reaction}`}
                        label={reaction}
                        aria-pressed={active}
                        className={active ? "" : "chat-message-hover"}
                        onClick={() => model.send_msg({type: "reaction", reaction})}
                      >
                        <Icon
                          baseClassName={active ? "material-icons" : "material-icons-outlined"}
                          sx={{...ICON_SX, color: active ? "primary.main" : undefined}}
                        >
                          {active ? active_icon : icon}
                        </Icon>
                      </ActionButton>
                    )
                  })}
                  {show_copy && (
                    <ActionButton label={copied ? "Copied" : "Copy"} onClick={() => model.send_msg("copy")}>
                      {copied ? <CheckIcon sx={ICON_SX} /> : <ContentCopyIcon sx={ICON_SX} />}
                    </ActionButton>
                  )}
                  {show_edit && (
                    <ActionButton label="Edit" onClick={() => model.send_msg("edit")}>
                      <EditOutlinedIcon sx={ICON_SX} />
                    </ActionButton>
                  )}
                  {show_timestamp && !is_help && (
                    <Typography className="chat-message-hover" variant="caption" color="text.secondary" sx={{px: 0.75}}>
                      {timestamp}
                    </Typography>
                  )}
                </Stack>
              )}
            </Stack>
          )}
        </Stack>
      )}
    </Box>
  )
}
