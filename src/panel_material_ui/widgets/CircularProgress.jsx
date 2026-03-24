import Box from "@mui/material/Box"
import CircularProgress from "@mui/material/CircularProgress"
import Typography from "@mui/material/Typography"
import {useTheme} from "@mui/material/styles"
import {render_icon_text} from "./utils"

const CIRCULAR_PROGRESS_ROOT_SX = {display: "flex", alignItems: "center", flexDirection: "row"}
const CIRCULAR_PROGRESS_CONTAINER_SX = {position: "relative", overflow: "hidden"}
const CIRCULAR_PROGRESS_BASE_SX = {position: "absolute", left: 0}

export function render({model, el}) {
  const [bgcolor] = model.useState("bgcolor")
  const [color] = model.useState("color")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [thickness] = model.useState("thickness")
  const [value] = model.useState("value")
  const [variant] = model.useState("variant")
  const [with_label] = model.useState("with_label")

  //el.style.overflow = "hidden"
  const theme = useTheme()
  const progressSx = React.useMemo(
    () => (sx ? [CIRCULAR_PROGRESS_BASE_SX, sx] : CIRCULAR_PROGRESS_BASE_SX),
    [sx]
  )

  const idle = (variant == "indeterminate" && !value)
  return (
    <Box sx={CIRCULAR_PROGRESS_ROOT_SX}>
      <Box sx={[CIRCULAR_PROGRESS_CONTAINER_SX, {width: `${size}px`, height: `${size}px`}]}>
        {bgcolor && (
          <CircularProgress
            sx={{
              color: bgcolor === "dark" ? theme.palette.grey[800] : theme.palette.grey[200],
            }}
            size={size}
            thickness={thickness}
            variant="determinate"
            value={100}
          />
        )}
        <CircularProgress
          color={idle ? (model.dark_theme ? "dark" : "light") : color}
          size={size}
          sx={progressSx}
          thickness={thickness}
          value={idle ? 100 : (typeof value === "boolean") ? 0 : value}
          variant={idle ? "determinate" : variant}
        />
        {with_label && variant == "determinate" && (
          <Box
            sx={{
              top: 0,
              left: 0,
              bottom: 0,
              right: 0,
              position: "absolute",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Typography
              variant="caption"
              component="div"
              sx={{color: "text.secondary"}}
            >
              {`${Math.round(value)}%`}
            </Typography>
          </Box>
        )}
      </Box>
      {label && (
        <Typography sx={{color: "text.primary", ml: 1, fontSize: `${size/2}px`}}>
          {render_icon_text(label)}
        </Typography>
      )}
    </Box>
  )
}
