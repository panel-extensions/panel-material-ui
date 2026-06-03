import Avatar from "@mui/material/Avatar"

const sizeSettings = {
  small: {width: 24, height: 24},
  medium: {width: 40, height: 40},
  large: {width: 56, height: 56},
}

export function render({model}) {
  const [alt_text] = model.useState("alt_text")
  const [color] = model.useState("color")
  const [content] = model.useState("content")
  const [size] = model.useState("size")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  // Determine if content is an image URL or text content
  const isImageUrl = content && (
    content.startsWith("http") ||
    content.startsWith("data:") ||
    // More specific check for common image file extensions
    /\.(jpg|jpeg|png|gif|svg|webp|bmp|ico)(\?.*)?$/i.test(content)
  )

  const avatarSx = {
    margin: "auto",
    verticalAlign: "center",
    ...(color && {bgcolor: color}),
    ...sizeSettings[size],
    ...sx
  }

  return (
    <Avatar
      alt={alt_text}
      sx={avatarSx}
      size={size}
      src={isImageUrl ? content : undefined}
      variant={variant}
      onClick={(e) => model.send_event("click", e)}
    >
      {!isImageUrl && content ? content : undefined}
    </Avatar>
  )
}
