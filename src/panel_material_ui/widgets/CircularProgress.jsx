import Box from "@mui/material/Box"
import CircularProgress from "@mui/material/CircularProgress"
import Typography from "@mui/material/Typography"
import {useTheme} from "@mui/material/styles"

export function render({model}) {
  const [bgcolor] = model.useState("bgcolor")
  const [color] = model.useState("color")
  const [label] = model.useState("label")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [thickness] = model.useState("thickness")
  const [value] = model.useState("value")
  const [variant] = model.useState("variant")
  const [with_label] = model.useState("with_label")

  const theme = useTheme()

  const idle = (variant == "indeterminate" && !value)
  return (
    <Box sx={{display: "flex", alignItems: "center", flexDirection: "row"}}>
      <Box sx={{position: "relative"}}>
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
          sx={{
            position: "absolute",
            left: 0,
            ...sx
          }}
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
      {label && <Typography sx={{color: "text.primary", ml: 1, fontSize: `${size/2}px`}}>{label}</Typography>}
    </Box>
  )
}
