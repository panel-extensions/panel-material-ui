import Stepper from "@mui/material/Stepper"
import Step from "@mui/material/Step"
import StepLabel from "@mui/material/StepLabel"
import StepContent from "@mui/material/StepContent"
import StepButton from "@mui/material/StepButton"
import MobileStepper from "@mui/material/MobileStepper"
import Button from "@mui/material/Button"
import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"
import {apply_flex, render_icon} from "./utils"

const CONTENT_BASE_SX = {
  flex: 1,
  minWidth: 0,
  minHeight: 0,
  display: "flex",
  flexDirection: "column",
  overflow: "auto",
  width: "100%",
}

export function render({model, view}) {
  const [active, setActive] = model.useState("active")
  const [alternativeLabel] = model.useState("alternative_label")
  const [backText] = model.useState("back_text")
  const [color] = model.useState("color")
  const [completed] = model.useState("completed")
  const [connector] = model.useState("connector")
  const [disabled] = model.useState("disabled")
  const [error] = model.useState("error")
  const [icons] = model.useState("icons")
  const [indicator] = model.useState("indicator")
  const [names] = model.useState("_names")
  const [nextText] = model.useState("next_text")
  const [nonLinear] = model.useState("non_linear")
  const [optional] = model.useState("optional")
  const [orientation] = model.useState("orientation")
  const [position] = model.useState("position")
  const [showButtons] = model.useState("show_buttons")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const headers = model.get_child("_headers")
  const objects = model.get_child("objects")

  const compact = variant === "compact"
  const steps = objects.length
  const activeIndex = Number.isInteger(active) && active >= 0 && active < steps ? active : 0

  const handleStep = React.useCallback((index) => () => {
    setActive(index)
  }, [setActive])

  const handleNext = React.useCallback(() => {
    setActive(Math.min(active + 1, steps - 1))
  }, [active, steps, setActive])

  const handleBack = React.useCallback(() => {
    setActive(Math.max(active - 1, 0))
  }, [active, setActive])

  const stepperSx = React.useMemo(() => ({
    "& .MuiStepIcon-root.Mui-active": {color: (theme) => theme.palette[color]?.main},
    "& .MuiStepIcon-root.Mui-completed": {color: (theme) => theme.palette[color]?.main},
    ...sx,
  }), [color, sx])

  const mobileSx = React.useMemo(() => ({
    "& .MuiLinearProgress-bar": {backgroundColor: (theme) => theme.palette[color]?.main},
    "& .MuiMobileStepper-dotActive": {backgroundColor: (theme) => theme.palette[color]?.main},
    ...sx,
  }), [color, sx])

  // Resolve (and flex) the active step's content. For the 'standard'
  // variant this is only needed in horizontal orientation (vertical
  // renders content inline via StepContent); 'compact' always shows it.
  const content = (compact || orientation === "horizontal") && steps > 0
    ? (apply_flex(view.get_child_view(model.objects[activeIndex]), "column") || objects[activeIndex])
    : null

  if (compact) {
    // MUI requires steps >= 1; default to 1 when empty
    const mobileSteps = steps || 1
    return (
      <Box sx={{display: "flex", flexDirection: "column", width: "100%", height: "100%"}}>
        <Box sx={{...CONTENT_BASE_SX, position: "relative"}}>
          {content}
        </Box>
        <MobileStepper
          activeStep={activeIndex}
          position={position}
          steps={mobileSteps}
          variant={indicator}
          sx={mobileSx}
          nextButton={
            <Button size="small" onClick={handleNext} disabled={active >= mobileSteps - 1}>
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

  const buttonRow = showButtons && steps > 0 ? (
    <Box sx={{display: "flex", flexDirection: "row", pt: 2}}>
      <Button
        color="inherit"
        disabled={active <= 0}
        onClick={handleBack}
        sx={{mr: 1}}
      >
        {backText}
      </Button>
      <Box sx={{flex: "1 1 auto"}} />
      <Button onClick={handleNext} disabled={active >= steps - 1}>
        {nextText}
      </Button>
    </Box>
  ) : null

  return (
    <Box sx={{display: "flex", flexDirection: "column", width: "100%", height: "100%"}}>
      <Stepper
        activeStep={activeIndex}
        alternativeLabel={alternativeLabel}
        connector={connector ? undefined : null}
        nonLinear={nonLinear}
        orientation={orientation}
        sx={stepperSx}
      >
        {names.map((label, index) => {
          const isError = error.includes(index)

          const optionalNode = optional.includes(index) ? (
            <Typography variant="caption" color={isError ? "error" : "inherit"}>
              Optional
            </Typography>
          ) : null

          const labelContent = label
            ? <span dangerouslySetInnerHTML={{__html: label}} />
            : headers[index]

          // Only override MUI's automatic completion/disabled state
          // when the user has explicitly provided indices
          const stepProps = {
            ...(completed.length > 0 && {completed: completed.includes(index)}),
            ...(disabled.length > 0 && {disabled: disabled.includes(index)}),
          }

          const iconNode = icons[index] ? render_icon(icons[index]) : undefined

          const stepLabel = nonLinear ? (
            <StepButton
              icon={iconNode}
              onClick={handleStep(index)}
              optional={optionalNode}
            >
              {labelContent}
            </StepButton>
          ) : (
            <StepLabel
              error={isError}
              icon={iconNode}
              optional={optionalNode}
            >
              {labelContent}
            </StepLabel>
          )

          return (
            <Step key={`step-${index}`} {...stepProps}>
              {stepLabel}
              {orientation === "vertical" && (
                <StepContent>
                  <Box sx={{py: 1}}>{objects[index]}</Box>
                </StepContent>
              )}
            </Step>
          )
        })}
      </Stepper>
      {orientation === "horizontal" && (
        <Box sx={CONTENT_BASE_SX}>
          {content}
        </Box>
      )}
      {buttonRow}
    </Box>
  )
}
