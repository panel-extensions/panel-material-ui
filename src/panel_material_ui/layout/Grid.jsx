import Grid from "@mui/material/Grid2"

export function render({model, view}) {
  const [columns] = model.useState("columns")
  const [direction] = model.useState("direction")
  const [columnSpacing] = model.useState("column_spacing")
  const [rowSpacing] = model.useState("row_spacing")
  const [size] = model.useState("size")
  const [models] = model.useState("objects")
  const [container] = model.useState("container")
  const [spacing] = model.useState("spacing")
  const objects = model.get_child("objects")

  if (view.parent?.model?.class_name === "Grid") {
    return <div style={{display: "contents"}}>{objects}</div>
  }
  return (
    <Grid
      container={container}
      columns={columns}
      direction={direction}
      columnSpacing={columnSpacing}
      rowSpacing={rowSpacing}
      size={size}
      spacing={spacing}
      sx={{height: "100%", width: "100%"}}
    >
      {models.map((model, index) => {
        const object = objects[index]
        return model.class_name === "Grid" ? (
          <Grid
            size={model.data.size}
            columns={model.data.columns}
            direction={model.data.direction}
            columnSpacing={model.data.column_spacing}
            rowSpacing={model.data.row_spacing}
            spacing={model.data.spacing}
            direction={model.data.direction}
          >
            {object}
          </Grid>
        ) : object
      })}
    </Grid>
  )
}
