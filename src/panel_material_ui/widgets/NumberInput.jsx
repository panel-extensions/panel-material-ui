import { Unstable_NumberInput as NumberInput, numberInputClasses } from "@mui/base/Unstable_NumberInput";
import { styled } from "@mui/system";

const FormattedNumberInput = React.forwardRef(function FormattedNumberInput(
  { format, value, onChange, onBlur, onFocus, ...props },
  ref
) {
  const [isEditing, setIsEditing] = React.useState(false);

  const handleFocus = (event) => {
    setIsEditing(true);
    onFocus?.(event);
  };

  const handleBlur = (event) => {
    setIsEditing(false);
    onBlur?.(event);
  };

  const handleChange = (event, val) => {
    onChange({ target: { value: val } });
  };

  const displayValue = isEditing || !format ? value : format.doFormat([value])[0];

  return (
    <StyledNumberInput
      {...props}
      ref={ref}
      value={displayValue}
      onChange={handleChange}
      onFocus={handleFocus}
      onBlur={handleBlur}
    />
  );
});


const blue = {
  100: '#DAECFF',
  200: '#80BFFF',
  400: '#3399FF',
  500: '#007FFF',
  600: '#0072E5',
  700: '#0059B2',
};

const grey = {
  50: '#F3F6F9',
  100: '#E5EAF2',
  200: '#DAE2ED',
  300: '#C7D0DD',
  400: '#B0B8C4',
  500: '#9DA8B7',
  600: '#6B7A90',
  700: '#434D5B',
  800: '#303740',
  900: '#1C2025',
};

export function render({ model }) {
  const [color] = model.useState("color");
  const [disabled] = model.useState("disabled");
  const [format] = model.useState("format");
  const [label] = model.useState("label");
  const [placeholder] = model.useState("placeholder");
  const [step] = model.useState("step");
  const [min] = model.useState("start");
  const [max] = model.useState("end");
  const [sx] = model.useState("sx");
  const [value, setValue] = model.useState("value");

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  return (
    <FormattedNumberInput
      aria-label={label}
      placeholder={placeholder}
      value={value}
      disabled={disabled}
      step={step}
      min={min}
      max={max}
      format={format}
      onChange={handleChange}
      sx={{ width: "100%", ...sx }}
    />
  );
}

const StyledNumberInput = styled(NumberInput)(
  ({ theme }) => `
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 400;
  border-radius: 8px;
  color: ${theme.palette.mode === "dark" ? "#C7D0DD" : "#1C2025"};
  background: ${theme.palette.mode === "dark" ? "#1C2025" : "#fff"};
  border: 1px solid ${theme.palette.mode === "dark" ? "#434D5B" : "#DAE2ED"};
  box-shadow: 0 2px 4px ${
    theme.palette.mode === "dark" ? "rgba(0,0,0, 0.5)" : "rgba(0,0,0, 0.05)"
  };
  display: grid;
  grid-template-columns: 1fr 19px;
  grid-template-rows: 1fr 1fr;
  align-items: center;
  padding: 4px;

  &:focus-within {
    border-color: #3399FF;
    box-shadow: 0 0 0 3px ${theme.palette.mode === "dark" ? "#0059B2" : "#80BFFF"};
  }

  &:hover {
    border-color: #3399FF;
  }

  input {
    font-size: 0.875rem;
    font-family: inherit;
    flex: 1;
    border: none;
    background: inherit;
    padding: 8px;
    outline: none;
    color: ${theme.palette.mode === "dark" ? "#C7D0DD" : "#1C2025"};
  }
`
);

const StyledInputRoot = styled('div')(
  ({ theme }) => `
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 400;
  border-radius: 8px;
  color: ${theme.palette.mode === 'dark' ? grey[300] : grey[900]};
  background: ${theme.palette.mode === 'dark' ? grey[900] : '#fff'};
  border: 1px solid ${theme.palette.mode === 'dark' ? grey[700] : grey[200]};
  box-shadow: 0 2px 4px ${
    theme.palette.mode === 'dark' ? 'rgba(0,0,0, 0.5)' : 'rgba(0,0,0, 0.05)'
  };
  display: grid;
  grid-template-columns: 1fr 19px;
  grid-template-rows: 1fr 1fr;
  overflow: hidden;
  column-gap: 8px;
  padding: 4px;

  &.${numberInputClasses.focused} {
    border-color: ${blue[400]};
    box-shadow: 0 0 0 3px ${theme.palette.mode === 'dark' ? blue[700] : blue[200]};
  }

  &:hover {
    border-color: ${blue[400]};
  }

  /* firefox */
  &:focus-visible {
    outline: 0;
  }
`,
);

const StyledInputElement = styled('input')(
  ({ theme }) => `
  font-size: 0.875rem;
  font-family: inherit;
  font-weight: 400;
  line-height: 1.5;
  grid-column: 1/2;
  grid-row: 1/3;
  color: ${theme.palette.mode === 'dark' ? grey[300] : grey[900]};
  background: inherit;
  border: none;
  border-radius: inherit;
  padding: 8px 12px;
  outline: 0;
`,
);

const StyledButton = styled('button')(
  ({ theme }) => `
  display: flex;
  flex-flow: row nowrap;
  justify-content: center;
  align-items: center;
  appearance: none;
  padding: 0;
  width: 19px;
  height: 19px;
  font-family: system-ui, sans-serif;
  font-size: 0.875rem;
  line-height: 1;
  box-sizing: border-box;
  background: ${theme.palette.mode === 'dark' ? grey[900] : '#fff'};
  border: 0;
  color: ${theme.palette.mode === 'dark' ? grey[300] : grey[900]};
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 120ms;

  &:hover {
    cursor: pointer;
    color: #FFF;
    background: ${theme.palette.mode === 'dark' ? blue[600] : blue[500]};
    border-color: ${theme.palette.mode === 'dark' ? blue[400] : blue[600]};
  }

  &.${numberInputClasses.incrementButton} {
    grid-column: 2/3;
    grid-row: 1/2;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border: 1px solid;
    border-bottom: 0;
    border-color: ${theme.palette.mode === 'dark' ? grey[700] : grey[200]};
    background: ${theme.palette.mode === 'dark' ? grey[900] : grey[50]};
    color: ${theme.palette.mode === 'dark' ? grey[200] : grey[900]};

    &:hover {
      cursor: pointer;
      color: #FFF;
      background: ${theme.palette.mode === 'dark' ? blue[600] : blue[500]};
      border-color: ${theme.palette.mode === 'dark' ? blue[400] : blue[600]};
    }
  }

  &.${numberInputClasses.decrementButton} {
    grid-column: 2/3;
    grid-row: 2/3;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    border: 1px solid;
    border-color: ${theme.palette.mode === 'dark' ? grey[700] : grey[200]};
    background: ${theme.palette.mode === 'dark' ? grey[900] : grey[50]};
    color: ${theme.palette.mode === 'dark' ? grey[200] : grey[900]};
  }

  & .arrow {
    transform: translateY(-1px);
  }
`,
);

StyledNumberInput.defaultProps = {
  slots: {
    root: StyledInputRoot,
    input: StyledInputElement,
    incrementButton: StyledButton,
    decrementButton: StyledButton,
  },
  slotProps: {
    incrementButton: { children: "▴" },
    decrementButton: { children: "▾" },
  },
};
