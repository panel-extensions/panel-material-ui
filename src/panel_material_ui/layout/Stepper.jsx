import Stepper from "@mui/material/Stepper"
import Step from "@mui/material/Step"
import StepLabel from "@mui/material/StepLabel"
import StepContent from "@mui/material/StepContent"
import StepButton from "@mui/material/StepButton"
import Box from "@mui/material/Box"
import Typography from "@mui/material/Typography"
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
  const [alternativeLabel] = model.useState("alternative_label")
  const [color] = model.useState("color")
  const [completed] = model.useState("completed")
  const [connector] = model.useState("connector")
  const [disabled] = model.useState("disabled")
  const [error] = model.useState("error")
  const [icons] = model.useState("icons")
  const [names] = model.useState("_names")
  const [nonLinear] = model.useState("non_linear")
  const [optional] = model.useState("optional")
  const [orientation] = model.useState("orientation")
  const [sx] = model.useState("sx")
  const headers = model.get_child("_headers")
  const objects = model.get_child("objects")

  const activeIndex = Number.isInteger(active) && active >= 0 && active < objects.length ? active : 0

  const handleStep = React.useCallback((index) => () => {
    setActive(index)
  }, [setActive])

  const stepperSx = React.useMemo(() => ({
    "& .MuiStepIcon-root.Mui-active": {color: (theme) => theme.palette[color]?.main},
    "& .MuiStepIcon-root.Mui-completed": {color: (theme) => theme.palette[color]?.main},
    ...sx,
  }), [color, sx])

  const content = orientation === "horizontal" && objects.length > 0
    ? (apply_flex(view.get_child_view(model.objects[activeIndex]), "column") || objects[activeIndex])
    : null

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
    </Box>
  )
}
