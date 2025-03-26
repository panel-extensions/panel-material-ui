import CircularProgress from "@mui/material/CircularProgress";
import Box from "@mui/material/Box";
import InputAdornment from "@mui/material/InputAdornment"
import IconButton from "@mui/material/IconButton"
import Icon from "@mui/material/Icon"
import SpeedDial from "@mui/material/SpeedDial"
import SpeedDialAction from "@mui/material/SpeedDialAction"
import SendIcon from "@mui/icons-material/Send"
import StopIcon from "@mui/icons-material/Stop"
import SpeedDialIcon from "@mui/material/SpeedDialIcon"
import OutlinedInput from "@mui/material/OutlinedInput"

const SpinningStopIcon = (props) => {
  return (
    <Box sx={{position: "relative", display: "inline-block", width: 50, height: 50}}>
      {/* Spinning Circular Arc */}
      <CircularProgress
        variant="indeterminate"
        size={50}
        thickness={4}
        sx={{
          color: `${props.color}.main`,
          animationDuration: "1s",
          strokeLinecap: "round", // Makes the arc smoother
        }}
      />
      {/* Centered Stop Icon */}
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          backgroundColor: "white",
          borderRadius: "50%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: 30,
          height: 30,
        }}
      >
        <StopIcon color={props.color} sx={{fontSize: 24}} />
      </Box>
    </Box>
  );
};

export function render({model, view}) {
  const [actions] = model.useState("actions")
  const [autogrow] = model.useState("auto_grow")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [disabled_enter, setDisabledEnter] = model.useState("disabled_enter")
  const [enter_sends] = model.useState("enter_sends")
  const [error_state] = model.useState("error_state")
  const [loading, setLoading] = model.useState("loading")
  const [max_rows] = model.useState("max_rows")
  const [label] = model.useState("label")
  const [placeholder] = model.useState("placeholder")
  const [rows] = model.useState("rows")
  const [sx] = model.useState("sx")
  const [value_input, setValueInput] = model.useState("value_input")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  let props = {sx: {width: "100%", height: "100%", ...sx}}
  if (autogrow) {
    props = {minRows: rows}
  } else {
    props = {rows}
  }

  const send = () => {
    if (disabled) {
      return
    }
    model.send_msg({type: "input", value: value_input})
    setValueInput("")
  }

  const stop = () => {
    model.send_msg({type: "action", action: "stop"})
  }

  return (
    <OutlinedInput
      multiline
      color={color}
      disabled={disabled}
      startAdornment={
        Object.keys(actions).length > 0 ? (
          <InputAdornment position="start" sx={{alignItems: "end", maxHeight: "2.5em"}}>
            <SpeedDial
              ariaLabel="Actions"
              size="small"
              FabProps={{size: "small"}}
              icon={<SpeedDialIcon color={color}/>}
              sx={{zIndex: 1000}}
            >
              {Object.keys(actions).map((action) => (
                <SpeedDialAction
                  key={action}
                  icon={<Icon>{actions[action].icon}</Icon>}
                  slotProps={{popper: {container: view.container}}}
                  tooltipTitle={actions[action].label || action}
                  onClick={() => model.send_msg({type: "action", action})}
                />
              ))}
            </SpeedDial>
          </InputAdornment>
        ) : null
      }
      endAdornment={
        <InputAdornment onClick={() => disabled_enter ? stop() : send()} position="end">
          <IconButton color="primary">
            {disabled_enter ? <SpinningStopIcon color={color}/> : <SendIcon/>}
          </IconButton>
        </InputAdornment>
      }
      error={error_state}
      maxRows={max_rows}
      label={label}
      onChange={(event) => setValueInput(event.target.value)}
      onKeyDown={(event) => {
        if (
          (event.key === "Enter") && (
            (enter_sends && (!(event.ctrlKey || event.shiftKey))) ||
            (!enter_sends && (event.ctrlKey || event.shiftKey))
          )
        ) {
          send()
        }
      }}
      placeholder={placeholder}
      value={value_input}
      variant={variant}
      fullWidth
      {...props}
    />
  )
}
