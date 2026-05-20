import MobileStepper from "@mui/material/MobileStepper"
import Button from "@mui/material/Button"
import Box from "@mui/material/Box"
import {apply_flex, render_icon} from "./utils"

const CONTENT_BASE_SX = {
  flex: 1,
  minWidth: 0,
  display: "flex",
  flexDirection: "column",
  overflow: "auto",
  position: "relative",
  width: "100%",
}

export function render({model, view}) {
  const [active, setActive] = model.useState("active")
  const [backText] = model.useState("back_text")
  const [color] = model.useState("color")
  const [nextText] = model.useState("next_text")
  const [position] = model.useState("position")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const objects = model.get_child("objects")

  // MUI requires steps >= 1; default to 1 when empty
  const steps = objects.length || 1
  const activeIndex = Number.isInteger(active) && active >= 0 && active < objects.length ? active : 0

  const handleNext = React.useCallback(() => {
    setActive(Math.min(active + 1, steps - 1))
  }, [active, steps, setActive])

  const handleBack = React.useCallback(() => {
    setActive(Math.max(active - 1, 0))
  }, [active, setActive])

  const stepperSx = React.useMemo(() => ({
    "& .MuiLinearProgress-bar": {backgroundColor: (theme) => theme.palette[color]?.main},
    "& .MuiMobileStepper-dotActive": {backgroundColor: (theme) => theme.palette[color]?.main},
    ...sx,
  }), [color, sx])

  const content = objects.length > 0
    ? (apply_flex(view.get_child_view(model.objects[activeIndex]), "column") || objects[activeIndex])
    : null

  return (
    <Box sx={{display: "flex", flexDirection: "column", width: "100%", height: "100%"}}>
      <Box sx={CONTENT_BASE_SX}>
        {content}
      </Box>
      <MobileStepper
        activeStep={activeIndex}
        position={position}
        steps={steps}
        variant={variant}
        sx={stepperSx}
        nextButton={
          <Button size="small" onClick={handleNext} disabled={active >= steps - 1}>
            {nextText}
            {render_icon("keyboard_arrow_right")}
          </Button>
        }
        backButton={
          <Button size="small" onClick={handleBack} disabled={active <= 0}>
            {render_icon("keyboard_arrow_left")}
            {backText}
          </Button>
        }
      />
    </Box>
  )
}
