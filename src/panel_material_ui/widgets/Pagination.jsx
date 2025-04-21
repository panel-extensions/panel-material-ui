import Pagination from "@mui/material/Pagination"

export function render({model, view}) {
  const [color] = model.useState("color")
  const [count] = model.useState("count")
  const [disabled] = model.useState("disabled")
  const [value, setValue] = model.useState("value")
  const [sx] = model.useState("sx")
  const [shape] = model.useState("shape")
  const [size] = model.useState("size")
  const [sibling_count] = model.useState("sibling_count")
  const [boundary_count] = model.useState("boundary_count")
  const [show_first_button] = model.useState("show_first_button")
  const [show_last_button] = model.useState("show_last_button")
  const [variant] = model.useState("variant")

  return (
    <Pagination
      boundaryCount={boundary_count}
      color={color}
      count={count}
      disabled={disabled}
      page={value+1}
      onChange={(event, value) => setValue(value-1)}
      shape={shape}
      showFirstButton={show_first_button}
      showLastButton={show_last_button}
      size={size}
      siblingCount={sibling_count}
      sx={sx}
      variant={variant}
    />
  )
}
