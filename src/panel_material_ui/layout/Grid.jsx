import Grid from "@mui/material/Grid"

const GRID_BASE_SX = {height: "100%", width: "100%"}

export function render({model, host}) {
  const [columns] = model.useState("columns")
  const [direction] = model.useState("direction")
  const [columnSpacing] = model.useState("column_spacing")
  const [rowSpacing] = model.useState("row_spacing")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [container] = model.useState("container")
  const [spacing] = model.useState("spacing")
  const objects = model.render_children("objects")
  const models = model.children("objects")
  const gridSx = React.useMemo(() => (sx ? [GRID_BASE_SX, sx] : GRID_BASE_SX), [sx])

  if (host.parent?.model.kind === "Grid") {
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
      sx={gridSx}
    >
      {models.map((child, index) => {
        const object = objects[index]
        return child.kind === "Grid" ? (
          <Grid
            columns={child.get("columns")}
            columnSpacing={child.get("column_spacing")}
            direction={child.get("direction")}
            rowSpacing={child.get("row_spacing")}
            size={child.get("size")}
            spacing={child.get("spacing")}
          >
            {object}
          </Grid>
        ) : object
      })}
    </Grid>
  )
}
