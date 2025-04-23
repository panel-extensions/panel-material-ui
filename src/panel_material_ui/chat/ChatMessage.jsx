import Avatar from "@mui/material/Avatar"
import Box from "@mui/material/Box"
import Icon from "@mui/material/Icon"
import IconButton from "@mui/material/IconButton"
import Paper from "@mui/material/Paper"
import Stack from "@mui/material/Stack"
import Typography from "@mui/material/Typography"
import ContentCopyIcon from "@mui/icons-material/ContentCopy"
import EditNoteIcon from "@mui/icons-material/EditNote"

function PlaceholderAvatar() {
  return (
    <Box sx={{
      margin: "1em 0.5em 0 0",
      width: 40,
      height: 40,
      position: "relative",
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }}
    >
      <Box
        component="span"
        sx={{
          position: "absolute",
          width: "100%",
          height: "100%",
          borderRadius: "50%",
          border: "3px solid",
          borderColor: "black",
          borderTopColor: "transparent",
          strokeLinecap: "round",
          animation: "spin 1s linear infinite",
          "@keyframes spin": {
            "0%": {transform: "rotate(0deg)"},
            "100%": {transform: "rotate(360deg)"}
          }
        }}
      />
      <Box
        component="span"
        sx={{
          position: "absolute",
          width: "80%",
          height: "80%",
          borderRadius: "50%",
          border: "3px solid",
          borderColor: "black",
          borderTopColor: "transparent",
          strokeLinecap: "round",
          animation: "spin 1.5s linear infinite",
          "@keyframes spin": {
            "0%": {transform: "rotate(0deg)"},
            "100%": {transform: "rotate(-360deg)"}
          }
        }}
      />
      <Box
        component="span"
        sx={{
          position: "absolute",
          width: "50%",
          height: "50%",
          borderRadius: "50%",
          border: "3px solid",
          borderColor: "black",
          borderTopColor: "transparent",
          strokeLinecap: "round",
          animation: "spin 2.5s linear infinite",
          "@keyframes spin": {
            "0%": {transform: "rotate(0deg)"},
            "100%": {transform: "rotate(360deg)"}
          }
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

  const [header] = model.get_child("header_objects")
  const [footer] = model.get_child("footer_objects")

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
      {avatar.type !== "image" && (avatar.type == "text" ? isEmoji(avatar.text) ? avatar.text : [...avatar.text][0] : <Icon>{avatar.icon}</Icon>)}
    </Avatar>
  ))

  const obj_model = view.model.data._object_panel
  const isResponsive = obj_model.sizing_mode && (obj_model.sizing_mode.includes("width") || obj_model.sizing_mode.includes("both"))

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
        <Paper elevation={elevation} sx={{bgcolor: "background.paper", width: isResponsive ? "100%" : "fit-content"}}>
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
              <Icon sx={{width: "0.5em"}}>{reaction_icons[reaction] || reaction}</Icon>
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
