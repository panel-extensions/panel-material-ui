import {apply_flex} from "./utils"

const WRAPPER_STYLE = {
  display: "flex",
  flexDirection: "column",
  width: "100%",
  height: "100%",
}

export function render({model, view}) {
  const objects = model.get_child("objects")

  React.useEffect(() => {
    const handler = () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
      })
    }
    model.on("lifecycle:update_layout", handler)
    return () => model.off("lifecycle:update_layout", handler)
  }, [])

  return (
    <div style={WRAPPER_STYLE}>
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </div>
  )
}
