import Stepper from "@mui/material/Stepper"
import Step from "@mui/material/Step"
import StepLabel from "@mui/material/StepLabel"
import StepButton from "@mui/material/StepButton"
import MobileStepper from "@mui/material/MobileStepper"
import Button from "@mui/material/Button"
import Typography from "@mui/material/Typography"
import {render_icon, render_icon_text} from "./utils"

export function render({model}) {
  const [active, setActive] = model.useState("active")
  const [alternativeLabel] = model.useState("alternative_label")
  const [backText] = model.useState("back_text")
  const [color] = model.useState("color")
  const [connector] = model.useState("connector")
  const [indicator] = model.useState("indicator")
  const [items] = model.useState("items")
  const [nextText] = model.useState("next_text")
  const [nonLinear] = model.useState("non_linear")
  const [orientation] = model.useState("orientation")
  const [position] = model.useState("position")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")

  const safeItems = Array.isArray(items) ? items : []
  const steps = safeItems.length
  const compact = variant === "compact"
  const activeIndex = Number.isInteger(active) && active >= 0 && active < steps ? active : 0

  const handleStep = (index) => () => {
    setActive(index)
    model.send_msg({type: "click", item: index})
  }

  const handleNext = () => {
    setActive(Math.min(activeIndex + 1, Math.max(steps - 1, 0)))
  }

  const handleBack = () => {
    setActive(Math.max(activeIndex - 1, 0))
  }

  if (compact) {
    const mobileSteps = steps || 1
    const mobileSx = {
      width: "100%",
      "& .MuiMobileStepper-progress": {minWidth: 120},
      "& .MuiLinearProgress-bar": {backgroundColor: (theme) => theme.palette[color]?.main},
      "& .MuiMobileStepper-dotActive": {backgroundColor: (theme) => theme.palette[color]?.main},
      ...sx,
    }
    return (
      <MobileStepper
        activeStep={activeIndex}
        position={position}
        steps={mobileSteps}
        variant={indicator}
        sx={mobileSx}
        nextButton={
          <Button size="small" onClick={handleNext} disabled={activeIndex >= mobileSteps - 1}>
            {nextText}
            {render_icon("keyboard_arrow_right")}
          </Button>
        }
        backButton={
          <Button size="small" onClick={handleBack} disabled={activeIndex <= 0}>
            {render_icon("keyboard_arrow_left")}
            {backText}
          </Button>
        }
      />
    )
  }

  const stepperSx = {
    width: "100%",
    "& .MuiStepIcon-root.Mui-active": {color: (theme) => theme.palette[color]?.main},
    "& .MuiStepIcon-root.Mui-completed": {color: (theme) => theme.palette[color]?.main},
    ...sx,
  }

  return (
    <Stepper
      activeStep={activeIndex}
      alternativeLabel={alternativeLabel}
      connector={connector ? undefined : null}
      nonLinear={nonLinear}
      orientation={orientation}
      sx={stepperSx}
    >
      {safeItems.map((item, index) => {
        const isObject = item != null && typeof item === "object"
        const label = typeof item === "string" ? item : (item?.label || "")
        const baseIcon = isObject && item.icon ? item.icon : null
        const activeIcon = isObject && item.active_icon ? item.active_icon : null
        const isError = isObject && Boolean(item.error)
        const isOptional = isObject && Boolean(item.optional)
        const explicitCompleted = isObject && Boolean(item.completed)
        const isDisabled = isObject && Boolean(item.disabled)

        const isActive = index === activeIndex
        // Mirror MUI's default: steps before the active one count as completed
        const isCompleted = explicitCompleted || (!isActive && index < activeIndex)
        const highlighted = isActive || isCompleted || isError

        const optionalNode = isOptional ? (
          <Typography variant="caption" color={isError ? "error" : "inherit"}>
            Optional
          </Typography>
        ) : null

        // When an item supplies an icon, render it with state-aware styling:
        // active/completed steps use the filled `active_icon` (falling back to
        // `icon`) in the active color, while pending steps use the outlined
        // icon greyed out. Without an icon we fall back to MUI's numbered circle.
        let iconNode
        if (baseIcon) {
          const iconName = highlighted ? (activeIcon || baseIcon) : baseIcon
          const iconColor = isError ? "error" : (highlighted ? color : "disabled")
          const iconVariant = highlighted ? "" : "-outlined"
          iconNode = render_icon(iconName, iconColor, undefined, "1.5rem", iconVariant)
        }
        const labelContent = render_icon_text(label)

        // Only set completed/disabled when explicitly truthy so MUI's
        // automatic behavior (steps before active appear completed) is kept
        const stepProps = {}
        if (explicitCompleted) { stepProps.completed = true }
        if (isDisabled) { stepProps.disabled = true }

        const stepLabel = nonLinear ? (
          <StepButton icon={iconNode} optional={optionalNode} onClick={handleStep(index)}>
            {labelContent}
          </StepButton>
        ) : (
          <StepLabel error={isError} icon={iconNode} optional={optionalNode}>
            {labelContent}
          </StepLabel>
        )

        return (
          <Step key={index} {...stepProps}>
            {stepLabel}
          </Step>
        )
      })}
    </Stepper>
  )
}
