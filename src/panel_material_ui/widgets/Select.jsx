import InputLabel from "@mui/material/InputLabel"
import MenuItem from "@mui/material/MenuItem"
import FormControl from "@mui/material/FormControl"
import Select from "@mui/material/Select"
import ListSubheader from "@mui/material/ListSubheader"

export function render({model, view, el}) {
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [disabled_options] = model.useState("disabled_options")
  const [label] = model.useState("label")
  const [options] = model.useState("options")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [value, setValue] = model.useState("value")
  const [variant] = model.useState("variant")

  let option_list;
  if (Array.isArray(options)) {
    option_list = options.map((opt, index) => {
      const optValue = Array.isArray(opt) ? opt[1] : opt;
      const optLabel = Array.isArray(opt) ? opt[0] : opt;
      return (
        <MenuItem
          key={index}
          value={optValue}
          disabled={disabled_options?.includes(optValue)}
        >
          {optLabel}
        </MenuItem>
      )
    });
  } else if (typeof options === "object" && options !== null) {
    option_list = Object.entries(options).flatMap(([groupLabel, groupOptions]) => [
      <ListSubheader key={`${groupLabel}-header`}>{groupLabel}</ListSubheader>,
      ...groupOptions.map((option, idx) => {
        const optValue = Array.isArray(option) ? option[1] : option;
        const optLabel = Array.isArray(option) ? option[0] : option;
        return (
          <MenuItem
            key={`${groupLabel}-${idx}`}
            value={optValue}
            disabled={disabled_options?.includes(optValue)}
          >
            {optLabel}
          </MenuItem>
        );
      }),
    ]);
  }

  const [anchorPosition, setAnchorPosition] = React.useState(null);

  const calculate_anchor = (event) => {
    const elRect = event.currentTarget.getBoundingClientRect()
    let parentRect
    if (view.parent) {
      parentRect = view.parent.el.getBoundingClientRect()
    } else {
      parentRect = document.body.getBoundingClientRect()
    }
    const res = {
      top: elRect.bottom - parentRect.top + 5,
      left: elRect.left - parentRect.left + 5
    }
    setAnchorPosition(res)
  }

  return (
    <FormControl fullWidth disabled={disabled}>
      {label && <InputLabel id={`select-label-${model.id}`}>{label}</InputLabel>}
      <Select
        onOpen={calculate_anchor}
        MenuProps={{
          anchorReference: "anchorPosition",
          anchorPosition,
          disablePortal: true,
          transformOrigin: {
            vertical: "top",
            horizontal: "left",
          },
        }}
        color={color}
        disabled={disabled}
        value={value}
        label={label}
        labelId={`select-label-${model.id}`}
        variant={variant}
        onChange={(event) => { setValue(event.target.value) }}
        sx={sx}
      >
        {option_list}
      </Select>
    </FormControl>
  );
}
