import Avatar from "@mui/material/Avatar"
import Box from "@mui/material/Box"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import Paper from "@mui/material/Paper"
import Stack from "@mui/material/Stack"
import Typography from "@mui/material/Typography"
import ContentCopyIcon from "@mui/icons-material/ContentCopy"
import EditNoteIcon from "@mui/icons-material/EditNote"
import {parseIconName} from "./utils"

function PlaceholderAvatar() {
  return (
    <Box sx={{
      margin: "1em 0.5em 0 0",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "8px",
      width: "90px" // Increased width to space dots further apart
    }}
    >
      <Box
        component="span"
        sx={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          backgroundColor: "text.disabled",
          animation: "grow 2.4s ease-in-out infinite, fade 2.4s ease-in-out infinite",
          "@keyframes grow": {
            "0%, 100%": {transform: "scale(0)"},
            "50%": {transform: "scale(1)"}
          },
          "@keyframes fade": {
            "0%, 100%": {opacity: 0.3},
            "50%": {opacity: 1}
          }
        }}
      />
      <Box
        component="span"
        sx={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          backgroundColor: "text.disabled",
          animation: "grow 2.4s ease-in-out infinite, fade 2.4s ease-in-out infinite",
          animationDelay: "0.6s"
        }}
      />
      <Box
        component="span"
        sx={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          backgroundColor: "text.disabled",
          animation: "grow 2.4s ease-in-out infinite, fade 2.4s ease-in-out infinite",
          animationDelay: "1.2s"
        }}
      />
      <Box
        component="span"
        sx={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          backgroundColor: "text.disabled",
          animation: "grow 2.4s ease-in-out infinite, fade 2.4s ease-in-out infinite",
          animationDelay: "1.8s"
        }}
      />
    </Box>
  )
}

function isEmoji(str) {
  const emojiRegex = /[\p{Emoji}]/u;
  return emojiRegex.test(str);
}

export function render({model, view}) {
  const [placement] = model.useState("placement")
  const [elevation] = model.useState("elevation")
  const [user] = model.useState("user")
  const [show_avatar] = model.useState("show_avatar")
  const [show_edit_icon] = model.useState("show_edit_icon")
  const [show_user] = model.useState("show_user")
  const [show_timestamp] = model.useState("show_timestamp")
  const [show_reaction_icons] = model.useState("show_reaction_icons")
  const [show_copy_icon] = model.useState("show_copy_icon")
  const [reaction_icons] = model.useState("reaction_icons")
  const [reactions] = model.useState("reactions")
  const [avatar] = model.useState("_internal_state.avatar")
  const [timestamp] = model.useState("_internal_state.timestamp")
  const object = model.get_child("_object_panel")

  const header = model.get_child("header_objects")
  const footer = model.get_child("footer_objects")

  model.on("msg:custom", (msg) => {
    navigator.clipboard.writeText(msg.text)
  })

  const placeholder = show_avatar && (avatar.type === "text" && avatar.text == "PLACEHOLDER")
  const avatar_component = (placeholder ? (
    <PlaceholderAvatar />
  ) : (
    <Avatar
      src={avatar.type === "image" ? avatar.src : null}
      sx={{margin: placement === "left" ? "1em 0.5em 0 0" : "1em 0 0 0.5em", bgcolor: "background.paper", color: "text.primary", boxShadow: 3}}
    >
      {avatar.type !== "image" && (avatar.type == "text" ? isEmoji(avatar.text) ? avatar.text : [...avatar.text][0] : (() => {
        const iconData = parseIconName(avatar.icon)
        return <Icon baseClassName={iconData.baseClassName}>{iconData.iconName}</Icon>
      })())}
    </Avatar>
  ))

  const obj_model = view.model.data._object_panel
  const isResponsive = obj_model.sizing_mode && (obj_model.sizing_mode.includes("width") || obj_model.sizing_mode.includes("both"))

  const paperRef = React.useRef(null);

  // Find and cache the scrollable feed ancestor once on mount.
  // Walk up from view.el, crossing shadow DOM boundaries via getRootNode().host.
  const scrollContainerRef = React.useRef(null);
  // Track whether the user has manually scrolled up. Reset when they
  // scroll back near the bottom. This lets us distinguish "user scrolled
  // up to read history" from "content grew and pushed the scroll position".
  const userScrolledUpRef = React.useRef(false);
  React.useEffect(() => {
    let el = view.el;
    while (el) {
      // +1 accounts for subpixel rounding differences across browsers
      if (el.scrollHeight > el.clientHeight + 1) {
        const style = getComputedStyle(el);
        if (style.overflowY === "auto" || style.overflowY === "scroll") {
          scrollContainerRef.current = el;
          break;
        }
      }
      if (el.parentElement) {
        el = el.parentElement;
      } else {
        const root = el.getRootNode();
        el = root instanceof ShadowRoot ? root.host : null;
      }
    }
    // Listen for user-initiated scroll events on the feed container.
    const feed = scrollContainerRef.current;
    if (!feed) { return; }
    let prevScrollTop = feed.scrollTop;
    const onScroll = () => {
      const currentTop = feed.scrollTop;
      const distFromBottom = feed.scrollHeight - currentTop - feed.clientHeight;
      if (currentTop < prevScrollTop) {
        // User scrolled up
        userScrolledUpRef.current = true;
      } else if (distFromBottom < 50) {
        // User scrolled back to (near) the bottom — re-enable auto-scroll
        userScrolledUpRef.current = false;
      }
      prevScrollTop = currentTop;
    };
    feed.addEventListener("scroll", onScroll);
    return () => feed.removeEventListener("scroll", onScroll);
  }, []);

  React.useEffect(() => {
    if (!paperRef.current) { return; }
    let layoutTimer = null;
    const observer = new ResizeObserver(() => {
      // Debounce layout invalidation to avoid thrashing during streaming.
      clearTimeout(layoutTimer);
      layoutTimer = setTimeout(() => view.invalidate_layout(), 50);
      // Scroll the feed to show new/expanded content after React paints,
      // but only if the user hasn't manually scrolled up.
      if (!userScrolledUpRef.current) {
        requestAnimationFrame(() => {
          const feed = scrollContainerRef.current;
          if (feed) {
            feed.scrollTop = feed.scrollHeight;
          }
        });
      }
    });
    observer.observe(paperRef.current);
    return () => {
      observer.disconnect();
      clearTimeout(layoutTimer);
    };
  }, []);

  return (
    <Box sx={{flexDirection: "row", display: "flex", maxWidth: "100%"}}>
      {placement === "left" && avatar_component}
      {!placeholder && <Stack direction="column" spacing={0} sx={{flexGrow: 1, maxWidth: "calc(100% - 60px)", alignItems: placement === "left" ? "flex-start" : "flex-end"}}>
        {show_user && <Typography variant="caption">
          {user}
        </Typography>}
        <Stack direction="row" spacing={0}>
          {header}
        </Stack>
        <Paper ref={paperRef} elevation={elevation} sx={{bgcolor: "background.paper", width: isResponsive ? "100%" : "fit-content"}}>
          {object}
        </Paper>
        <Stack direction="row" spacing={0}>
          {show_edit_icon && <IconButton disableRipple size="small" sx={{padding: "0 0.1em"}} onClick={() => { model.send_msg("edit") }}>
            <EditNoteIcon sx={{width: "0.8em"}} color="lightgray"/>
          </IconButton>}
          {show_copy_icon && <IconButton disableRipple size="small" sx={{padding: "0 0.1em"}} onClick={() => { model.send_msg("copy") }}>
            <ContentCopyIcon sx={{width: "0.5em"}} color="lightgray"/>
          </IconButton>}
          {show_reaction_icons && reactions.map((reaction) => (
            <IconButton key={`reaction-${reaction}`} disableRipple size="small" sx={{padding: "0 0.1em"}} onClick={() => { model.send_msg(reaction) }}>
              {(() => {
                const iconName = reaction_icons[reaction] || reaction
                const iconData = parseIconName(iconName)
                return <Icon baseClassName={iconData.baseClassName} sx={{width: "0.5em"}}>{iconData.iconName}</Icon>
              })()}
            </IconButton>
          ))}
        </Stack>
        <Stack direction="row" spacing={0}>
          {footer}
        </Stack>
        {show_timestamp && <Typography variant="caption" color="text.secondary">
          {timestamp}
        </Typography>}
      </Stack>}
      {placement === "right" && avatar_component}
    </Box>
  );
};
