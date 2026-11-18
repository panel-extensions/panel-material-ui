import pmui from "panel-material-ui"

const stylesheetRequests = new Map()
const NOOP_SIGNAL = {connect: () => {}, disconnect: () => {}}

function NodeStyles({node, model, shared_styles}) {
  const [loaded, setLoaded] = React.useState({})
  const urls = node.stylesheets.filter(sheet => sheet.url).map(sheet => sheet.url)
  const urlKey = urls.join("\n")
  React.useEffect(() => {
    let active = true
    Promise.all(urls.map(url => {
      if (!stylesheetRequests.has(url)) {
        stylesheetRequests.set(url, fetch(url).then(response => {
          if (!response.ok) { throw new Error(`Failed to load stylesheet: ${url}`) }
          return response.text()
        }).catch(() => {
          stylesheetRequests.delete(url)
          return null
        }))
      }
      return stylesheetRequests.get(url)
    })).then(css => {
      if (!active) { return }
      if (css.some(content => content === null || /@import\b/i.test(content))) {
        model.send_msg({type: "stylesheet_failure", id: node.id})
      } else {
        setLoaded(Object.fromEntries(urls.map((url, index) => [url, css[index]])))
      }
    })
    return () => { active = false }
  }, [urlKey])

  return node.stylesheets.map((sheet, index) => {
    let css = sheet.css ?? shared_styles[sheet.base_url] ?? loaded[sheet.url]
    if (css === undefined) { return null }
    if (css === null) { return null }
    if (sheet.base_url || sheet.url) {
      css = css.replace(/url\(\s*(['"]?)(?!data:|https?:|\/)([^'")]+)\1\s*\)/g,
        (_, quote, path) => `url(${quote}${new URL(path, new URL(sheet.base_url || sheet.url, document.baseURI)).href}${quote})`)
    }
    css = css.replace(/:host\(([^)]*)\)/g, ":scope$1").replace(/:host\b/g, ":scope")
    return <style key={index}>{`@scope (#pmui-${node.id}) to ([data-pmui-host]) { ${css} }`}</style>
  })
}

function hostLayout(node, direction) {
  const {width, height, min_width, max_width, min_height, max_height, margin,
    aspect_ratio, sizing_mode, width_policy, height_policy, align} = node.layout
  let horizontal = width_policy || "auto"
  let vertical = height_policy || "auto"
  if (sizing_mode === "fixed") { horizontal = vertical = "fixed" } else if (sizing_mode === "stretch_both" || sizing_mode === "scale_both") { horizontal = vertical = "max" } else if (sizing_mode === "stretch_width") { horizontal = "max" } else if (sizing_mode === "stretch_height") { vertical = "max" } else if (sizing_mode === "scale_width") { horizontal = "max"; vertical = "min" } else if (sizing_mode === "scale_height") { horizontal = "min"; vertical = "max" }

  const margins = Array.isArray(margin) ? margin.length === 2 ?
    [margin[0] * 2, margin[1] * 2] : [margin[0] + margin[2], margin[1] + margin[3]] :
    [margin == null ? 0 : margin * 2, margin == null ? 0 : margin * 2]
  const cssSize = (policy, size, marginSize) => {
    if (policy === "max") { return marginSize ? `calc(100% - ${marginSize}px)` : "100%" }
    if (policy === "min") { return "min-content" }
    if (policy === "fit") { return "fit-content" }
    return size == null ? "fit-content" : `${size}px`
  }
  let cssWidth = cssSize(horizontal, width, margins[1])
  let cssHeight = cssSize(vertical, height, margins[0])
  const aspect = aspect_ratio ?? (sizing_mode?.startsWith("scale_") ? "auto" : null)
  const ratio = aspect === "auto" ? width != null && height != null ? width / height : null : aspect
  if (aspect != null && horizontal !== vertical) {
    if (horizontal === "fixed" || horizontal === "max") { cssHeight = "auto" } else if (vertical === "fixed" || vertical === "max") { cssWidth = "auto" } else { cssWidth = cssHeight = "auto" }
  } else if (ratio != null && horizontal === vertical && horizontal !== "fixed") {
    if (ratio >= 1) { cssHeight = "auto" } else { cssWidth = "auto" }
  }

  const styles = {
    width: cssWidth, height: cssHeight,
    margin: margin == null ? undefined : Array.isArray(margin) ? margin.map(value => `${value}px`).join(" ") : `${margin}px`,
    minWidth: min_width == null ? undefined : `${min_width}px`,
    minHeight: min_height == null ? undefined : `${min_height}px`,
    maxWidth: max_width != null ? `${max_width}px` :
      direction && horizontal !== "fixed" ? "100%" : undefined,
    maxHeight: max_height != null ? `${max_height}px` :
      direction && vertical !== "fixed" ? "100%" : undefined,
    aspectRatio: aspect == null ? undefined : aspect === "auto" && ratio != null ? `${width} / ${height}` : `${aspect}`,
  }
  if (direction) {
    const along = direction === "row" ? horizontal : vertical
    const across = direction === "row" ? vertical : horizontal
    const basis = direction === "row" ? width : height
    styles.flex = along === "max" ? "1 0 0px" : along === "fit" ? "1 1 auto" :
      along === "min" ? "0 1 auto" : `0 0 ${basis == null ? "auto" : `${basis}px`}`
    const alignment = Array.isArray(align) ? align[direction === "row" ? 1 : 0] : align
    styles.alignSelf = across === "max" ? "stretch" : alignment === "auto" ? undefined : alignment
    if (across === "max") { styles[direction === "row" ? "height" : "width"] = "auto" }
  }
  return styles
}

function MaterialNode({node, model, view, parentView, fallbacks, shared_styles}) {
  const current = React.useRef({node, model, view, parentView, fallbacks, shared_styles})
  current.current = {node, model, view, parentView, fallbacks, shared_styles}
  const listeners = React.useRef(new Set())
  React.useEffect(() => {
    const receive = (msg) => {
      if (msg.type === "node_msg" && msg.id === node.id) {
        listeners.current.forEach(callback => callback(msg.data))
      }
    }
    model.on("msg:custom", receive)
    return () => model.off("msg:custom", receive)
  }, [model, node.id])

  const [componentModel] = React.useState(() => new Proxy({
    useState: (name) => {
      const incoming = current.current.node.props[name]
      const ack = current.current.node.acks[model.id]?.[name] ?? 0
      const [value, setValue] = React.useState(incoming)
      const latest = React.useRef({seq: ack, value: incoming})
      React.useEffect(() => {
        if (ack < latest.current.seq) { return }
        latest.current = {seq: ack, value: incoming}
        setValue(incoming)
      }, [incoming, ack])
      return [value, (next) => {
        const updated = typeof next === "function" ? next(latest.current.value) : next
        const seq = latest.current.seq + 1
        latest.current = {seq, value: updated}
        setValue(updated)
        current.current.model.send_msg({type: "update", id: current.current.node.id, name, value: updated,
          root: current.current.model.id, seq})
      }]
    },
    get_child: (name) => {
      const {node, model, view, fallbacks, shared_styles} = current.current
      const children = node.children[name]
      if (Array.isArray(children)) {
        return children.map(child => (
          <Node key={child.id} node={child} model={model} view={view} fallbacks={fallbacks} shared_styles={shared_styles}
            parentView={childView}
            direction={node.kind === "Row" || node.kind === "Page" && name === "header" ? "row" :
              node.kind === "Column" || node.kind === "Page" ? "column" : null}
          />
        ))
      }
      return children ? <Node key={children.id} node={children} model={model} view={view} parentView={childView}
        fallbacks={fallbacks} shared_styles={shared_styles}
      /> : null
    },
    send_event: (name) => current.current.model.send_msg({type: name, id: current.current.node.id}),
    send_msg: (data) => current.current.model.send_msg({type: "msg", id: current.current.node.id, data}),
    on: (name, callback) => name === "msg:custom" ? listeners.current.add(callback) : current.current.model.on(name, callback),
    off: (name, callback) => name === "msg:custom" ? listeners.current.delete(callback) : current.current.model.off(name, callback),
  }, {
    get: (target, name) => name === "esm_constants" ? current.current.node.constants :
      name in target ? target[name] : current.current.node.props[name],
  }))
  const [childView] = React.useState(() => ({
    el: view.container,
    container: view.container,
    root: view.root,
    shadow_el: view.shadow_el,
    model_proxy: view.model_proxy,
    is_root: false,
    get parent() { return current.current.parentView ?? current.current.view },
    get compiled_host_id() { return current.current.node.id },
    get theme_revision() { return current.current.node.theme_revision },
    get compiled_host() { return current.current.view.shadow_el.querySelector(`#pmui-${current.current.node.id}`) },
    get_child_view: (child) => child?.kind === "fallback" ?
      current.current.view.get_child_view(current.current.model.fallbacks[child.slot]) : null,
    model: {
      get id() { return current.current.node.id },
      get class_name() { return current.current.node.kind },
      get data() {
        return {...current.current.node.props,
          _custom_theme: current.current.node.kind === "Page" ? current.current.model._custom_theme : current.current.node.props._custom_theme,
          properties: {}, change: NOOP_SIGNAL}
      },
      get document() { return current.current.model.document },
    },
  }))
  const Component = pmui[node.kind].render
  return <Component key={node.id} model={componentModel} view={childView} el={view.container}/>
}

function Node({node, fallbacks, model, view, parentView, direction, shared_styles}) {
  const host = React.useRef(null)
  React.useEffect(() => {
    const el = host.current
    if (!el) { return }
    for (const [name, value] of Object.entries(node.styles)) {
      el.style.setProperty(name.replace(/[A-Z]/g, char => `-${char.toLowerCase()}`), value)
    }
    if (!node.visible) { el.style.display = "none" }
    return () => {
      for (const name of Object.keys(node.styles)) {
        el.style.removeProperty(name.replace(/[A-Z]/g, char => `-${char.toLowerCase()}`))
      }
    }
  }, [node.styles, node.visible])
  if (node.kind === "fallback") {
    return fallbacks[node.slot]
  }
  const content = <MaterialNode key={node.id} node={node} model={model} view={view} parentView={parentView}
    fallbacks={fallbacks} shared_styles={shared_styles}
  />
  const layout = hostLayout(node, direction)
  const declarations = Object.entries(layout).filter(([, value]) => value !== undefined)
    .map(([name, value]) => `${name.replace(/[A-Z]/g, char => `-${char.toLowerCase()}`)}: ${value};`).join(" ")
  const {width, height, min_width, min_height, max_width, max_height, sizing_mode, margin} = node.layout
  const horizontal = ["stretch_width", "stretch_both", "scale_width", "scale_both"].includes(sizing_mode)
  const vertical = ["stretch_height", "stretch_both", "scale_height", "scale_both"].includes(sizing_mode)
  const marginSize = (axis) => margin == null ? 0 : Array.isArray(margin) ?
    margin.length === 2 ? margin[axis === "width" ? 1 : 0] * 2 :
      axis === "width" ? margin[1] + margin[3] : margin[0] + margin[2] : margin * 2
  const size = (axis, stretch, value) => stretch ?
    marginSize(axis) ? `calc(100% - ${marginSize(axis)}px)` : "100%" : value ?? undefined
  return <div ref={host} id={`pmui-${node.id}`} data-pmui-host="" className={node.css_classes.join(" ")}
    style={{width: size("width", horizontal, width), height: size("height", vertical, height),
      minWidth: min_width ?? undefined, minHeight: min_height ?? undefined,
      maxWidth: max_width ?? undefined, maxHeight: max_height ?? undefined,
      display: node.visible ? undefined : "none"}}
  >
    <style>{`@scope (#pmui-${node.id}) { :scope { ${declarations} } }`}</style>
    <NodeStyles node={node} model={model} shared_styles={shared_styles}/>{content}
  </div>
}

export function render({model, view}) {
  const [tree] = model.useState("tree")
  const fallbacks = model.get_child("fallbacks")
  return <Node node={tree} fallbacks={fallbacks} model={model} view={view} shared_styles={tree.shared_styles}/>
}
