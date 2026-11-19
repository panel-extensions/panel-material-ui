
const WRAPPER_STYLE = {
  display: "flex",
  flexDirection: "column",
  width: "100%",
  height: "100%",
}

export function render({model, host}) {
  const objects = model.render_children("objects", {direction: "column"})

  return (
    <div style={WRAPPER_STYLE}>
      {objects}
    </div>
  )
}
