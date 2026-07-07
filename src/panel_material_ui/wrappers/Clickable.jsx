import ButtonBase from "@mui/material/ButtonBase"
import Box from "@mui/material/Box"

export function render({model}) {
  const [disabled] = model.useState("disabled")
  const [disableRipple] = model.useState("disable_ripple")
  const [sx] = model.useState("sx")
  const object = model.get_child("object")

  const mergedSx = React.useMemo(() => ({
    display: "inline-flex",
    width: "100%",
    height: "100%",
    textAlign: "inherit",
    ...sx,
  }), [sx])

  return (
    <ButtonBase
      disabled={disabled}
      disableRipple={disableRipple}
      onClick={() => model.send_event("click", {})}
      sx={mergedSx}
    >
      <Box sx={{width: "100%", height: "100%"}}>
        {object || null}
      </Box>
    </ButtonBase>
  )
}
