import Box from "@mui/material/Box"
import FormControl from "@mui/material/FormControl"
import FormHelperText from "@mui/material/FormHelperText"
import InputLabel from "@mui/material/InputLabel"
import MenuItem from "@mui/material/MenuItem"
import Select from "@mui/material/Select"
import {render_description} from "./description"
import {CustomMenu, detect_nb} from "./menu"
import {render_icon_text} from "./utils"

const paletteStyle = (colors, height, width, fit) => ({
  backgroundImage: `linear-gradient(to right, ${colors.join(", ")})`,
  height,
  width: "100%",
  minWidth: fit ? 0 : width,
  maxWidth: fit ? "100%" : undefined,
  flexShrink: fit ? 1 : 0,
  borderRadius: 1,
})

export function render({model, el, view}) {
  const [disabled] = model.useState("disabled")
  const [error_state] = model.useState("error_state")
  const [helper_text] = model.useState("helper_text")
  const [label] = model.useState("label")
  const [description] = model.useState("description")
  const [ncols] = model.useState("ncols")
  const [items] = model.useState("options")
  const [swatch_height] = model.useState("swatch_height")
  const [swatch_width] = model.useState("swatch_width")
  const [value, setValue] = model.useState("value")

  const options = Object.entries(items || {})
  const selected = options.find(([name]) => name === value)
  const labelId = `colormap-label-${model.id}`
  const isNotebook = Boolean(detect_nb(view))
  const [open, setOpen] = React.useState(false)
  const anchorEl = React.useRef(null)

  const palette = (colors, fit = false) => (
    <Box aria-hidden="true" sx={paletteStyle(colors || [], swatch_height, swatch_width, fit)} />
  )

  const handleSelect = (name) => {
    setValue(name)
    setOpen(false)
  }

  const menuItems = options.map(([name, colors]) => (
    <MenuItem key={name} value={name} onClick={isNotebook ? () => handleSelect(name) : undefined} sx={{display: "flex", flexDirection: "column", alignItems: "stretch", gap: 0.5, minWidth: 0}}>
      {palette(colors, ncols > 1)}
      <Box component="span" sx={{overflow: "hidden", textOverflow: "ellipsis"}}>{render_icon_text(name)}</Box>
    </MenuItem>
  ))

  return (
    <FormControl disabled={disabled} fullWidth error={error_state}>
      {label && <InputLabel id={labelId}>{render_icon_text(label)}{description ? render_description({model, el, view}) : null}</InputLabel>}
      <Select
        label={label}
        labelId={labelId}
        value={value || ""}
        onChange={(event) => setValue(event.target.value)}
        onClick={() => setOpen(true)}
        onClose={() => setOpen(false)}
        open={!isNotebook && open}
        ref={anchorEl}
        renderValue={() => selected ? (
          <Box sx={{display: "flex", flexDirection: "column", alignItems: "stretch", gap: 0.5, minWidth: 0, width: "100%"}}>
            {palette(selected[1])}
            <Box component="span" sx={{minWidth: 0, maxWidth: "100%", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap"}}>
              {render_icon_text(selected[0])}
            </Box>
          </Box>
        ) : ""}
        MenuProps={!isNotebook ? {
          PaperProps: {
            sx: {
              "& .MuiList-root": {
                display: "grid",
                gridTemplateColumns: `repeat(${Math.max(1, ncols)}, minmax(0, 1fr))`,
                gap: 0.5,
                p: 1,
              },
            },
          },
        } : undefined}
      >
        {!isNotebook && menuItems}
      </Select>
      {isNotebook && (
        <CustomMenu
          anchorEl={() => anchorEl.current}
          open={open}
          onClose={() => setOpen(false)}
          paperProps={{sx: {"& .MuiList-root": {display: "grid", gridTemplateColumns: `repeat(${Math.max(1, ncols)}, minmax(0, 1fr))`, gap: 0.5, p: 1}}}}
          view={view}
        >
          {menuItems}
        </CustomMenu>
      )}
      {helper_text && <FormHelperText>{helper_text}</FormHelperText>}
    </FormControl>
  )
}
