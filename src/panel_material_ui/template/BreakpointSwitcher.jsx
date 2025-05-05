import Box from "@mui/material/Box"
import useMediaQuery from "@mui/material/useMediaQuery"
import {useTheme} from "@mui/material/styles"

export function render({model}) {
  const theme = useTheme();
  const [breakpoint] = model.useState("breakpoint")
  const [media_query] = model.useState("media_query")
  const small = model.get_child("small")
  const large = model.get_child("large")
  const isLarge = media_query ? useMediaQuery(media_query) : useMediaQuery(theme.breakpoints.up(breakpoint))

  React.useEffect(() => {
    model.send_msg({type: "switch", current: isLarge ? "large" : "small"})
  }, [isLarge])

  return (
    <Box sx={{width: "100%", height: "100%"}}>
      <div style={{display: isLarge ? "block" : "none"}}>
        {large}
      </div>
      <div style={{display: isLarge ? "none" : "block"}}>
        {small}
      </div>
    </Box>
  )
}
