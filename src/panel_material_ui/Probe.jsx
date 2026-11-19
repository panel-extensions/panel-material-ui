export function render({model, host}) {
  const [value, setValue] = model.useState("value")
  const [direction] = model.useState("direction")
  const key = model.get("key")
  const objects = model.render_children("objects", {direction})

  React.useEffect(() => {
    const probes = window.pmui_probes = window.pmui_probes ?? {}
    const probe = probes[key] = {model, host, setValue, msgs: [], changes: 0, removed: false}
    model.on("remove", () => { probe.removed = true })
    const stops = [
      model.on("msg", (msg) => probe.msgs.push(msg)),
      model.on("change:value", () => { probe.changes++ }),
    ]
    probe.stop = () => stops.forEach(stop => stop())
    return probe.stop
  }, [])

  return (
    <div className="probe" data-key={key} style={{display: "flex", flexDirection: direction, width: "100%", height: "100%"}}>
      <span className="probe-value">{value}</span>
      {objects}
    </div>
  )
}
