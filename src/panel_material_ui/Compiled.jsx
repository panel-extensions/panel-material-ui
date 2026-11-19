import * as React from "react"
import pmui from "panel-material-ui"
import {apply_flex, child_flex, child_handle, make_host} from "./utils"

const stylesheetRequests = new Map()
const CompiledContext = React.createContext(null)
const FallbackContext = React.createContext([])

function child_nodes(node) {
  const nodes = []
  for (const children of Object.values(node.children ?? {})) {
    if (Array.isArray(children)) {
      nodes.push(...children)
    } else if (children) {
      nodes.push(children)
    }
  }
  return nodes
}

/**
 * Holds the nodes of the tree by id, so that a patch only re-renders the
 * components subscribed to the node it changes.
 */
function create_store(model, initial) {
  const nodes = new Map()
  const listeners = new Map()
  const subscribers = new Map()
  const seqs = new Map()
  const models = new Map()
  const state = {tree: null, rev: -1, shared_styles: {}, kinds: {}, sheets: [], layouts: new Map(), dirty: false}
  // Fills in what the tree only sends once: the defaults of the kind of
  // component and the stylesheets a node refers to by index.
  const expand = (node) => {
    if (node.kind === "fallback") { return node }
    const kind = state.kinds[node.kind]
    const sheet_ids = node.stylesheets ?? []
    return {
      ...node,
      props: {...kind.props, ...node.props},
      constants: node.constants ?? kind.constants,
      css_classes: node.css_classes ?? [],
      sheet_ids,
      stylesheets: sheet_ids.map(id => state.sheets[id]),
      styles: node.styles ?? {},
      visible: node.visible ?? true,
    }
  }
  const index = (node) => {
    nodes.set(node.id, expand(node))
    child_nodes(node).forEach(index)
  }
  const unindex = (node) => {
    nodes.delete(node.id)
    child_nodes(node).forEach(unindex)
  }
  const notify = (id, names) => listeners.get(id)?.forEach(callback => callback(names))
  const load = (tree) => {
    state.tree = tree
    state.rev = tree.state.rev
    state.shared_styles = tree.shared_styles
    state.kinds = tree.kinds
    state.sheets = tree.sheets
    nodes.clear()
    index(tree.root)
  }
  const apply_op = (op) => {
    const node = nodes.get(op.id)
    if (node == null) { return }
    if (op.subtree) {
      unindex(node)
      if (op.shared_styles) { state.shared_styles = {...state.shared_styles, ...op.shared_styles} }
      if (op.kinds) { state.kinds = {...state.kinds, ...op.kinds} }
      if (op.sheets) {
        state.sheets = [...state.sheets, ...op.sheets]
        notify("@sheets", null)
      }
      index(op.subtree)
      notify(op.id, null)
      return
    }
    const props = {...node.props}
    const names = []
    for (const [name, value] of Object.entries(op.props ?? {})) {
      const ack = op.acks?.[name]
      if (ack && ack[0] === model.id && ack[1] < (seqs.get(`${op.id}:${name}`) ?? 0)) { continue }
      props[name] = value
      names.push(name)
    }
    nodes.set(op.id, {...node, props, visible: op.visible ?? node.visible})
    notify(op.id, names)
  }
  load(initial)
  return {
    state,
    models,
    get: (id) => nodes.get(id),
    listen(id, callback) {
      if (!listeners.has(id)) { listeners.set(id, new Set()) }
      listeners.get(id).add(callback)
      return () => listeners.get(id)?.delete(callback)
    },
    subscriber(id) {
      if (!subscribers.has(id)) { subscribers.set(id, (callback) => this.listen(id, callback)) }
      return subscribers.get(id)
    },
    reset(tree) {
      if (tree === state.tree) { return }
      load(tree)
      for (const id of [...listeners.keys()]) { notify(id, null) }
    },
    layout_key(declarations) {
      if (!state.layouts.has(declarations)) {
        state.layouts.set(declarations, `l${state.layouts.size}`)
        state.dirty = true
      }
      return state.layouts.get(declarations)
    },
    flush_layouts() {
      if (state.dirty) {
        state.dirty = false
        notify("@layouts", null)
      }
    },
    apply(patch) {
      if (patch?.rev == null || patch.rev <= state.rev) { return }
      for (const step of [...(patch.earlier ?? []), patch]) {
        if (step.rev <= state.rev) { continue }
        if (step.rev > state.rev + 1) {
          // A patch was missed, e.g. sent before this view was listening.
          model.send_msg({type: "resync"})
          return
        }
        state.rev = step.rev
        step.ops.forEach(apply_op)
      }
    },
    set_local(id, name, value) {
      const node = nodes.get(id)
      const key = `${id}:${name}`
      const seq = (seqs.get(key) ?? 0) + 1
      seqs.set(key, seq)
      if (node) {
        nodes.set(id, {...node, props: {...node.props, [name]: value}})
        notify(id, [name])
      }
      return seq
    },
  }
}

function scoped(sheet, css) {
  if (sheet.base_url || sheet.url) {
    css = css.replace(/url\(\s*(['"]?)(?!data:|https?:|\/)([^'")]+)\1\s*\)/g,
      (_, quote, path) => `url(${quote}${new URL(path, new URL(sheet.base_url || sheet.url, document.baseURI)).href}${quote})`)
  }
  return css.replace(/:host\(([^)]*)\)/g, ":scope$1").replace(/:host\b/g, ":scope")
}

/**
 * Renders each stylesheet and each set of layout declarations once for the
 * whole tree, scoped to the hosts that refer to them, since most nodes
 * share a handful of them.
 */
function SharedStyles({store}) {
  // Nodes register their layout while they render, after this component
  // has, which the store snapshot catches before anything is painted.
  React.useSyncExternalStore(store.subscriber("@layouts"), () => store.state.layouts.size)
  React.useSyncExternalStore(store.subscriber("@sheets"), () => store.state.sheets)
  const {sheets, shared_styles, layouts} = store.state
  const rules = [...layouts].map(([declarations, key]) => `[data-pmui-layout="${key}"] { ${declarations} }`)
  return <>
    <style>{rules.join("\n")}</style>
    {sheets.map((sheet, index) => {
      const css = sheet.css ?? shared_styles[sheet.base_url]
      return css == null ? null :
        <style key={index}>{`@scope ([data-pmui-css~="s${index}"]) to ([data-pmui-host]) { ${scoped(sheet, css)} }`}</style>
    })}
  </>
}

function useNode(store, id) {
  return React.useSyncExternalStore(store.subscriber(id), () => store.get(id))
}

function NodeStyles({node, model}) {
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
    const css = sheet.url ? loaded[sheet.url] : null
    return css == null ? null :
      <style key={index}>{`@scope (#pmui-${node.id}) to ([data-pmui-host]) { ${scoped(sheet, css)} }`}</style>
  })
}

// The policies Bokeh derives from the sizing of a model, see
// LayoutDOMView.box_sizing.
function box_sizing(layout) {
  const {width, height, sizing_mode, width_policy, height_policy, align} = layout
  let horizontal = width_policy || "auto"
  let vertical = height_policy || "auto"
  if (sizing_mode === "fixed") { horizontal = vertical = "fixed" } else if (sizing_mode === "stretch_both" || sizing_mode === "scale_both") { horizontal = vertical = "max" } else if (sizing_mode === "stretch_width") { horizontal = "max" } else if (sizing_mode === "stretch_height") { vertical = "max" } else if (sizing_mode === "scale_width") { horizontal = "max"; vertical = "min" } else if (sizing_mode === "scale_height") { horizontal = "min"; vertical = "max" }
  const [halign, valign] = Array.isArray(align) ? align : [align, align]
  return {
    width_policy: horizontal, height_policy: vertical, width, height,
    halign: halign === "auto" ? undefined : halign, valign: valign === "auto" ? undefined : valign,
  }
}

function hostLayout(node, direction, extra) {
  const {width, height, min_width, max_width, min_height, max_height, margin, aspect_ratio, sizing_mode} = node.layout
  const sizing = box_sizing(node.layout)
  const horizontal = sizing.width_policy
  const vertical = sizing.height_policy

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
    const {flex, align_self, reset} = child_flex(sizing, direction)
    styles.flex = flex
    styles.alignSelf = align_self
    if (reset) { styles[reset] = "auto" }
  }
  return {...styles, ...extra}
}

// Mirrors what Panel serializes of a DOM event: the plain values on the
// event and the state of its target.
function serialize_event(event) {
  if (event == null || typeof event !== "object") {
    return {}
  }
  const plain = (source) => {
    const data = {}
    for (const name in source) {
      const value = source[name]
      if (value === null || ["string", "number", "boolean"].includes(typeof value)) { data[name] = value }
    }
    return data
  }
  const element = (el) => el instanceof Element ? {
    tagName: el.tagName, id: el.id, value: el.value ?? null, checked: el.checked ?? null,
    boundingClientRect: plain(el.getBoundingClientRect()),
  } : null
  const data = plain(event.nativeEvent ?? event)
  data.target = element(event.target)
  data.currentTarget = element(event.currentTarget)
  return data
}

/**
 * The model and host of a compiled node, the counterparts of what make_host
 * builds around a Panel view. See the component interface in utils.js.
 */
function make_node(context, id, current) {
  const {store, model, view, host: compiled_host} = context
  const node = () => store.get(id) ?? current.current.node
  const handlers = {msg: new Set(), remove: new Set()}
  const setters = new Map()
  const send = (name, value) => {
    const seq = store.set_local(id, name, value)
    model.send_msg({type: "update", id, name, value, root: model.id, seq})
  }
  const child_list = (name) => {
    const children = node().children?.[name]
    return children == null ? [] : Array.isArray(children) ? children : [children]
  }
  const fallback_model = (child) => model.get("fallbacks")?.[child.slot]
  const public_id = (child) => child.kind === "fallback" ? fallback_model(child)?.id ?? child.id : child.id
  const element = (child, options) => (
    <Node key={child.id} id={public_id(child)} nid={child.id} parentHost={host}
      direction={options.direction} extra={options.style}/>
  )
  const api = {
    get id() { return id },
    get kind() { return node().kind },
    get constants() { return node().constants ?? {} },
    get tags() { return [] },
    useState: (path) => {
      const [name, ...rest] = path.split(".")
      if (!(name in node().props)) {
        throw ReferenceError(`Could not resolve ${path} on ${node().kind}`)
      }
      const value = React.useSyncExternalStore(
        store.subscriber(id), () => rest.reduce((value, key) => value?.[key], store.get(id)?.props[name])
      )
      if (!setters.has(path)) {
        setters.set(path, (next) => {
          const previous = rest.reduce((value, key) => value?.[key], store.get(id)?.props[name])
          const updated = typeof next === "function" ? next(previous) : next
          if (rest.length) {
            throw Error(`Cannot set ${path} on a compiled ${node().kind}`)
          }
          send(name, updated)
        })
      }
      return [value, setters.get(path)]
    },
    get: (name) => name === "_custom_theme" && node().kind === "Page" ? model.get("_custom_theme") : node().props[name],
    set: (values, options = {}) => {
      for (const [name, value] of Object.entries(values)) {
        if (options.sync === false) { store.set_local(id, name, value) } else { send(name, value) }
      }
    },
    children: (name) => child_list(name).map((child) => {
      if (child.kind === "fallback") {
        const bk_model = fallback_model(child)
        return bk_model ? child_handle(bk_model) : {id: child.id, kind: "fallback", layout: {}, get: () => undefined}
      }
      return {
        id: child.id,
        kind: child.kind,
        get layout() { return store.get(child.id)?.layout ?? child.layout },
        get: (prop) => store.get(child.id)?.props[prop],
      }
    }),
    render_children: (name, options = {}) => {
      const children = node().children?.[name]
      if (Array.isArray(children)) {
        return children.map(child => element(child, options))
      }
      return children ? element(children, options) : null
    },
    send_msg: (data) => model.send_msg({type: "msg", id, data}),
    send_event: (name, event) => model.send_msg({type: "event", id, name, data: serialize_event(event)}),
    on: (event, callback) => {
      const stops = (Array.isArray(event) ? event : [event]).map((name) => {
        if (name in handlers) {
          handlers[name].add(callback)
          return () => handlers[name].delete(callback)
        } else if (name === "change") {
          return store.listen(id, () => callback())
        } else if (name.startsWith("change:")) {
          const prop = name.slice(7)
          return store.listen(id, (changed) => (changed == null || changed.includes(prop)) && callback())
        }
        // A compiled node is laid out by CSS alone, so "layout" never fires.
        return () => {}
      })
      return () => stops.forEach(stop => stop())
    },
  }
  const node_model = new Proxy(api, {
    get: (target, name) => name in target ? target[name] : node().props[name],
    has: (target, name) => name in target || name in node().props,
  })
  const is_top = () => current.current.parentHost == null
  const own_el = () => view.shadow_el.querySelector(`#pmui-${id}`)
  const host = {
    model: node_model,
    get parent() { return current.current.parentHost ?? compiled_host },
    get root() {
      let top = host
      while (top.parent != null && top.parent !== compiled_host) { top = top.parent }
      return top
    },
    // The root of the tree stands in for the Compiled view that mounts it.
    get is_root() { return is_top() && compiled_host.is_root },
    get is_document_root() { return is_top() && compiled_host.is_document_root },
    get dev() { return compiled_host.dev },
    get host_el() { return is_top() ? view.el : own_el() },
    get content_el() { return is_top() ? view.container : own_el() },
    get overlay_root() { return compiled_host.overlay_root },
    get style_root() { return view.shadow_el },
    shares_style_root: true,
    get emotion_cache() { return compiled_host.emotion_cache },
    get layout() { return node().layout },
    get document() { return compiled_host.document },
    invalidate_layout: () => view.invalidate_layout(),
    has_child: (child) => child_nodes(node()).some(({id: child_id}) => child_id === child.model.id),
  }
  return {host, handlers}
}

function MaterialNode({node, parentHost}) {
  const context = React.useContext(CompiledContext)
  const {model} = context
  const id = node.id
  const current = React.useRef({node, parentHost})
  current.current = {node, parentHost}
  const [{host, handlers}] = React.useState(() => make_node(context, id, current))
  React.useEffect(() => {
    const receive = (msg) => {
      if (msg.type === "node_msg" && msg.id === id) {
        handlers.msg.forEach(callback => callback(msg.data))
      }
    }
    const stop = model.on("msg", receive)
    return () => {
      stop()
      handlers.remove.forEach(callback => callback())
    }
  }, [model, id])
  const Component = pmui[node.kind].render
  return <Component key={id} model={host.model} host={host}/>
}

// A child that renders through its own Bokeh view is sized by Bokeh.
function Fallback({node, parentHost, direction, extra}) {
  const {model, view} = React.useContext(CompiledContext)
  const fallbacks = React.useContext(FallbackContext)
  const bk_model = model.get("fallbacks")?.[node.slot]
  if (bk_model != null) {
    view.pmui_placements.set(bk_model.id, {parent: parentHost ?? null, root: parentHost == null})
  }
  React.useEffect(() => {
    if (bk_model == null || !(direction || extra)) { return }
    const size = () => apply_flex(view.get_child_view(bk_model), direction, extra)
    size()
    return model.on("layout", size)
  }, [bk_model, direction, extra])
  return fallbacks[node.slot] ?? null
}

function Node({nid, parentHost, direction, extra}) {
  const {store, model} = React.useContext(CompiledContext)
  const node = useNode(store, nid)
  const host = React.useRef(null)
  const styles = node?.styles
  const visible = node?.visible
  React.useEffect(() => {
    const el = host.current
    if (!el || !styles) { return }
    for (const [name, value] of Object.entries(styles)) {
      el.style.setProperty(name.replace(/[A-Z]/g, char => `-${char.toLowerCase()}`), value)
    }
    if (!visible) { el.style.display = "none" }
    return () => {
      for (const name of Object.keys(styles)) {
        el.style.removeProperty(name.replace(/[A-Z]/g, char => `-${char.toLowerCase()}`))
      }
    }
  }, [styles, visible])
  React.useLayoutEffect(() => store.flush_layouts())
  if (node == null) {
    return null
  }
  if (node.kind === "fallback") {
    return <Fallback node={node} parentHost={parentHost} direction={direction} extra={extra}/>
  }
  const layout = hostLayout(node, direction, extra)
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
  const shared = node.sheet_ids.filter(index => !store.state.sheets[index]?.url).map(index => `s${index}`).join(" ")
  return <div ref={host} id={`pmui-${node.id}`} data-pmui-host="" data-pmui-layout={store.layout_key(declarations)}
    data-pmui-css={shared || undefined}
    className={[node.kind.replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase(), ...node.css_classes].join(" ")}
    style={{width: size("width", horizontal, width), height: size("height", vertical, height),
      minWidth: min_width ?? undefined, minHeight: min_height ?? undefined,
      maxWidth: max_width ?? undefined, maxHeight: max_height ?? undefined,
      display: node.visible ? undefined : "none"}}
  >
    {node.stylesheets.some(sheet => sheet.url) && <NodeStyles node={node} model={model}/>}
    <MaterialNode key={node.id} node={node} parentHost={parentHost}/>
  </div>
}

export function render(props) {
  // Compiled is the host of its nodes, so it works on the Panel view itself.
  const view = props.view
  const host = make_host(view, props.model)
  const model = host.model
  const [tree] = model.useState("tree")
  const fallbacks = model.render_children("fallbacks")
  const [store] = React.useState(() => create_store(model, tree))
  const [context] = React.useState(() => {
    view.pmui_placements = new Map()
    view.pmui_placement = (id) => view.pmui_placements.get(id)
    return {store, model, view, host}
  })
  React.useLayoutEffect(() => store.reset(tree), [tree])
  React.useEffect(() => {
    const apply = () => store.apply(model.get("patch"))
    apply()
    return model.on("change:patch", apply)
  }, [])
  return (
    <CompiledContext.Provider value={context}>
      <FallbackContext.Provider value={fallbacks}>
        <SharedStyles store={store}/>
        <Node nid={tree.root.id}/>
      </FallbackContext.Provider>
    </CompiledContext.Provider>
  )
}
