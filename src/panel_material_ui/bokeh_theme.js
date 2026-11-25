const themed_values = new WeakMap()

export function apply_plot_theme(model, values) {
  let previous = themed_values.get(model)
  if (previous == null) {
    previous = new Map()
    themed_values.set(model, previous)
  }
  const prior = new Map(previous)
  const updates = {}
  for (const [name, value] of Object.entries(values)) {
    const property = model.properties[name]
    if (name.endsWith("_alpha")) {
      const color = name.replace(/_alpha$/, "_color")
      // Bokeh omits explicit values equal to their defaults, including alpha=1.
      if (model.properties[color]?.dirty && (
        !prior.has(color) || !Object.is(model[color], prior.get(color))
      )) {
        previous.delete(name)
        continue
      }
    }
    if (prior.has(name)) {
      if (!Object.is(model[name], prior.get(name))) {
        previous.delete(name)
        continue
      }
    } else if (property.dirty) {
      continue
    }
    updates[name] = value
    previous.set(name, value)
  }
  model.setv(updates)
}
