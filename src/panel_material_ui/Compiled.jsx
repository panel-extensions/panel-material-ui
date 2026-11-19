import * as React from "react"
import {createPortal, flushSync} from "react-dom"
import createCache from "@emotion/cache"
import {CacheProvider} from "@emotion/react"
import pmui from "panel-material-ui"
import {apply_flex, child_flex, child_handle, make_host, overlay_container, theme_document_early} from "./utils"

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
  // The parent of each node, and of each child that renders through its
  // own view, which is known by the slot it renders into.
  const parents = new Map()
  const slots = new Map()
  const hosts = new Map()
  // The shadow roots of the nodes a JSComponent places in the DOM itself,
  // which seal a child off from its parent as the view of a child would.
  const roots = new Map()
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
  const index = (node, parent = null) => {
    nodes.set(node.id, expand(node))
    parents.set(node.id, parent)
    if (node.kind === "fallback") { slots.set(node.slot, parent) }
    child_nodes(node).forEach(child => index(child, node.id))
  }
  const unindex = (node) => {
    nodes.delete(node.id)
    parents.delete(node.id)
    hosts.delete(node.id)
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
    parents.clear()
    slots.clear()
    index(tree.root)
  }
  const apply_op = (op) => {
    const node = nodes.get(op.id)
    if (node == null) { return }
    if (op.subtree) {
      const parent = parents.get(op.id) ?? null
      unindex(node)
      if (op.shared_styles) { state.shared_styles = {...state.shared_styles, ...op.shared_styles} }
      if (op.kinds) { state.kinds = {...state.kinds, ...op.kinds} }
      if (op.sheets) {
        state.sheets = [...state.sheets, ...op.sheets]
        notify("@sheets", null)
      }
      index(op.subtree, parent)
      const renotify = (child) => {
        notify(child.id, null)
        child_nodes(child).forEach(renotify)
      }
      renotify(op.subtree)
      // The parent may lay its children out by their sizing.
      if (parent != null && nodes.has(parent)) {
        nodes.set(parent, {...nodes.get(parent)})
        notify(parent, null)
      }
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
    nodes.set(op.id, {
      ...node, props, visible: op.visible ?? node.visible,
      css_classes: op.css_classes ?? node.css_classes, styles: op.styles ?? node.styles,
    })
    notify(op.id, names)
  }
  load(initial)
  return {
    state,
    hosts,
    roots,
    root_of(id) {
      for (let current = id; current != null; current = parents.get(current)) {
        if (roots.has(current)) { return roots.get(current) }
      }
      return null
    },
    get: (id) => nodes.get(id),
    parent: (id) => parents.get(id) ?? null,
    slot_parent: (slot) => slots.get(slot),
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
  // The wrapper Panel mounts a child view in takes no part in the layout.
  rules.unshift(".error-wrapper, .child-wrapper { display: contents; }")
  return <>
    <style>{rules.join("\n")}</style>
    {sheets.map((sheet, index) => {
      const css = sheet.css ?? shared_styles[sheet.base_url]
      return css == null ? null :
        <style key={index}>{`@scope ([data-pmui-css~="s${index}"]) to (:scope [data-pmui-host] > *) { ${scoped(sheet, css)} }`}</style>
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
      <style key={index}>{`@scope (#pmui-${node.id}) to (:scope [data-pmui-host] > *) { ${scoped(sheet, css)} }`}</style>
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
    // As for the host of a Bokeh view, which e.g. the loading overlay of a
    // component is positioned against.
    position: "relative",
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
function make_node(context, id) {
  const {store, model, view, host: compiled_host} = context
  let last = store.get(id)
  const node = () => (last = store.get(id) ?? last)
  const parent = () => {
    const parent_id = store.parent(id)
    return parent_id == null ? null : node_host(context, parent_id).host
  }
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
    <Node key={child.id} id={public_id(child)} nid={child.id}
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
  const is_top = () => store.parent(id) == null
  const style_root = () => store.root_of(id)?.root ?? view.shadow_el
  const own_el = () => style_root().querySelector(`#pmui-${id}`)
  const host = {
    model: node_model,
    get parent() { return parent() ?? compiled_host },
    get root() {
      let top = host
      while (top.parent != null && top.parent !== compiled_host) { top = top.parent }
      return top
    },
    // The root of the tree stands in for the Compiled view that mounts it.
    get is_root() { return is_top() && compiled_host.is_root },
    get is_document_root() { return is_top() && !node().substitute && compiled_host.is_document_root },
    get dev() { return compiled_host.dev },
    get host_el() { return is_top() ? view.el : own_el() },
    get content_el() { return is_top() ? view.container : own_el() },
    get overlay_root() {
      const sealed = store.root_of(id)
      return sealed ? overlay_container(sealed.overlays) : compiled_host.overlay_root
    },
    get style_root() { return style_root() },
    shares_style_root: true,
    get emotion_cache() { return store.root_of(id)?.cache ?? compiled_host.emotion_cache },
    get layout() { return node().layout },
    get document() { return compiled_host.document },
    invalidate_layout: () => view.invalidate_layout(),
    has_child: (child) => child_nodes(node()).some(({id: child_id}) => child_id === child.model.id),
  }
  return {host, handlers}
}

// Hosts are created on demand, so one exists before its component renders,
// e.g. for a child that looks up its ancestors while it is being built.
function node_host(context, id) {
  const hosts = context.store.hosts
  if (!hosts.has(id)) {
    hosts.set(id, make_node(context, id))
  }
  return hosts.get(id)
}

function MaterialNode({node}) {
  const context = React.useContext(CompiledContext)
  const {model} = context
  const id = node.id
  const {host, handlers} = node_host(context, id)
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

// Panel renders the view of a child when the child mounts. A tree mounts in
// one commit, so its children would all render before the browser paints
// anything. They mount after the first paint instead, a few at a time.
const MOUNT_BUDGET = 12
const mounts = []
let mounting = false

function run_mounts() {
  const start = performance.now()
  while (mounts.length) {
    const entry = mounts.shift()
    if (entry.mount) {
      flushSync(entry.mount)
    }
    if (performance.now() - start > MOUNT_BUDGET) {
      setTimeout(run_mounts)
      return
    }
  }
  mounting = false
}

function schedule_mount(mount) {
  const entry = {mount}
  mounts.push(entry)
  if (!mounting) {
    mounting = true
    // A hidden page does not animate, so a timer backs the frame up.
    let started = false
    const start = () => {
      if (!started) {
        started = true
        run_mounts()
      }
    }
    requestAnimationFrame(() => setTimeout(start))
    setTimeout(start, 100)
  }
  return () => { entry.mount = null }
}

// A child that renders through its own Bokeh view is sized by Bokeh.
function Fallback({node, direction, extra, immediate}) {
  const {model, view} = React.useContext(CompiledContext)
  const fallbacks = React.useContext(FallbackContext)
  const bk_model = model.get("fallbacks")?.[node.slot]
  // A JSComponent measures its children once it has placed them.
  const [mounted, setMounted] = React.useState(Boolean(immediate))
  React.useEffect(() => immediate ? undefined : schedule_mount(() => setMounted(true)), [])
  React.useEffect(() => {
    if (bk_model == null || !(direction || extra)) { return }
    const size = () => apply_flex(view.get_child_view(bk_model), direction, extra)
    size()
    return model.on("layout", size)
  }, [bk_model, direction, extra, mounted])
  return mounted ? fallbacks[node.slot] ?? null : null
}

const LAYOUT_PROPS = new Set([
  "width", "height", "min_width", "max_width", "min_height", "max_height", "margin", "sizing_mode",
  "aspect_ratio", "width_policy", "height_policy", "align",
])
const PROTOTYPE_PROPS = new Set(["class_name", "dev", "events", "render_policy", "importmap", "bundle", "type"])
const LIFECYCLE = ["after_render", "after_layout", "mounted", "remove", "resize"]
const esm_renderers = new Map()

function same_value(a, b) {
  if (a === b) { return true }
  if (a == null || b == null || typeof a !== "object" || typeof b !== "object") { return false }
  try {
    return JSON.stringify(a) === JSON.stringify(b)
  } catch {
    return false
  }
}

/**
 * Stands in for the model and the view Panel passes to the render function
 * of a JSComponent. Whatever of the two a component reaches for that has no
 * counterpart here is reported, and the component then renders through its
 * own view instead.
 */
function make_esm(context, id, prototype) {
  const {store, model, view} = context
  let last = store.get(id)
  const node = () => (last = store.get(id) ?? last)
  const slots = new Map()
  const child_models = new Map()
  const child_values = new WeakMap()
  const lifecycle = new Map(LIFECYCLE.map(name => [name, []]))
  const accessed = new Set()
  const state = {
    watchers: [], msg: [], container: null, host: null, render: null, mounted: false,
    reported: false, generation: 0, children: new Map(),
  }

  const report = (reason) => {
    if (state.reported) { return }
    state.reported = true
    console.warn(`${node().kind} cannot be compiled, it uses ${reason}`)
    model.send_msg({type: "esm_unsupported", id, reason})
  }
  const is_child = (name) => node().children != null && name in node().children
  const is_prop = (name) => name in node().props
  const child_list = (name) => {
    const children = node().children?.[name]
    return children == null ? [] : Array.isArray(children) ? children : [children]
  }
  const fallback_model = (child) => model.get("fallbacks")?.[child.slot]
  const child_model = (child) => {
    if (child.kind === "fallback") { return fallback_model(child) }
    if (!child_models.has(child.id)) {
      child_models.set(child.id, new Proxy({id: child.id}, {
        get: (target, name) => name in target ? target[name] :
          store.get(child.id)?.layout?.[name] ?? store.get(child.id)?.props?.[name] ?? null,
      }))
    }
    return child_models.get(child.id)
  }
  const child_value = (name) => {
    const children = node().children[name]
    if (children == null) { return null }
    if (!Array.isArray(children)) { return child_model(children) }
    if (child_values.has(children)) { return child_values.get(children) }
    const models = children.map(child_model)
    if (models.every(child => child != null)) { child_values.set(children, models) }
    return models
  }
  const slot = (child) => {
    if (!slots.has(child.id)) { slots.set(child.id, document.createElement("div")) }
    return slots.get(child.id)
  }
  const read = (name) => {
    if (is_child(name)) { return child_value(name) }
    if (is_prop(name)) { return node().props[name] }
    if (LAYOUT_PROPS.has(name)) { return node().layout[name] ?? null }
    if (name === "css_classes") { return node().css_classes }
    if (name === "visible") { return node().visible }
    return undefined
  }
  const watchable = (name) => is_child(name) || is_prop(name) || LAYOUT_PROPS.has(name) ||
    name === "css_classes" || name === "visible"
  const snapshot = (name) => is_child(name) ? child_list(name).map(child => child.id).join(" ") : read(name)
  const write = (name, value) => {
    if (!is_prop(name) || is_child(name)) { return false }
    if (same_value(node().props[name], value)) { return true }
    const seq = store.set_local(id, name, value)
    model.send_msg({type: "update", id, name, value, root: model.id, seq})
    return true
  }
  const strip = (name) => name.startsWith("change:") ? name.slice(7) : name
  const methods = {
    get_child: (name) => {
      accessed.add(name)
      if (!state.children.has(name)) { state.children.set(name, snapshot(name)) }
      const children = node().children?.[name]
      return Array.isArray(children) ? children.map(slot) : children ? slot(children) : null
    },
    send_msg: (data) => model.send_msg({type: "msg", id, data}),
    send_event: (name, event) => model.send_msg({type: "event", id, name, data: serialize_event(event)}),
    on: (names, callback) => {
      for (let name of [].concat(names)) {
        name = strip(name)
        if (name === "msg:custom") {
          state.msg.push(callback)
        } else if (watchable(name)) {
          state.watchers.push({name, callback, seen: snapshot(name)})
        } else if (lifecycle.has(name.replace(/^lifecycle:/, ""))) {
          lifecycle.get(name.replace(/^lifecycle:/, "")).push(callback)
        } else if (name.split(".")[0] in node().props || name in prototype) {
          report(`model.on("${name}")`)
        } else {
          console.warn(`Could not register callback for event type '${name}'`)
        }
      }
    },
    off: (names, callback) => {
      for (let name of [].concat(names)) {
        name = strip(name)
        if (name === "msg:custom") {
          state.msg = state.msg.filter(handler => handler !== callback)
        } else if (watchable(name)) {
          state.watchers = state.watchers.filter(watcher => watcher.name !== name || watcher.callback !== callback)
        } else if (lifecycle.has(name.replace(/^lifecycle:/, ""))) {
          const key = name.replace(/^lifecycle:/, "")
          lifecycle.set(key, lifecycle.get(key).filter(handler => handler !== callback))
        }
      }
    },
  }
  const data = new Proxy({}, {
    get: (_, name) => {
      if (typeof name !== "string") { return undefined }
      if (name === "attributes") { return node().props }
      if (name === "esm_constants") { return node().constants }
      return is_child(name) || is_prop(name) ? read(name) : undefined
    },
    set: (_, name, value) => write(name, value),
    has: (_, name) => is_child(name) || is_prop(name),
  })
  const model_proxy = new Proxy({}, {
    get: (_, name) => {
      if (typeof name !== "string") { return undefined }
      if (name in methods) { return methods[name] }
      if (watchable(name)) { return read(name) }
      if (name === "id") { return id }
      if (name === "data") { return data }
      if (name === "document") { return view.model.document }
      if (name === "children") { return Object.keys(node().children ?? {}) }
      if (PROTOTYPE_PROPS.has(name)) { return prototype[name] }
      if (name in prototype) { report(`model.${name}`) }
      return undefined
    },
    set: (_, name, value) => {
      if (write(name, value)) { return true }
      if (name in prototype) { report(`model.${name}`) }
      return false
    },
    has: (_, name) => name in methods || watchable(name) || name in prototype,
  })
  const child_view = (child) => {
    const real = child.kind === "fallback" && fallback_model(child) ? view.get_child_view(fallback_model(child)) : null
    return {
      el: slot(child), model: child_model(child),
      // Resolves once React has committed the child into its element.
      get ready() { return new Promise(resolve => setTimeout(resolve)).then(() => real?.ready) },
      child_views: [], rerender: () => restyle(child), rerender_: () => restyle(child), render: () => {},
      after_render: () => {}, r_after_render: () => restyle(child),
      invalidate_layout: () => {}, has_finished: () => true,
    }
  }
  // Attaching or moving an element drops the rules its stylesheets were
  // given through the CSSOM, which the views below it then restore.
  const recover = (moved) => {
    // What r_after_render does for a React view, without laying the view
    // and everything below it out again.
    if (moved.use_shadow_dom && moved._dom_reinserted?.()) {
      moved.force_update()
      moved._mark_dom()
    }
    for (const nested of moved.child_views ?? []) { recover(nested) }
  }
  const restyle = (child) => {
    const visit = (current) => {
      if (current.kind === "fallback") {
        const bk_model = fallback_model(current)
        const child_view = bk_model && view.get_child_view(bk_model)
        if (child_view?.el.isConnected) { recover(child_view) }
      } else {
        child_nodes(store.get(current.id) ?? current).forEach(visit)
      }
    }
    visit(child)
  }
  const child_views = () => Object.keys(node().children ?? {}).flatMap(name => child_list(name).map(child_view))
  const view_api = {
    get el() { return state.host },
    get container() { return state.container },
    get shadow_el() { return view.shadow_el },
    get model() { return model_proxy },
    get model_proxy() { return model_proxy },
    get child_views() { return child_views() },
    get root() { return view.root },
    get parent() { return view },
    get is_destroyed() { return !state.mounted },
    get ready() { return Promise.resolve() },
    _child_rendered: new Map(),
    get_child_view: (child) => {
      const match = Object.keys(node().children ?? {}).flatMap(child_list).find(
        candidate => child_model(candidate) === child || candidate.id === child?.id
      )
      return match ? child_view(match) : undefined
    },
    invalidate_layout: () => {},
    update_layout: () => {},
    compute_layout: () => {},
    notify_finished: () => {},
  }
  const view_proxy = new Proxy(view_api, {
    get: (target, name) => {
      if (name in target || typeof name !== "string") { return target[name] }
      if (name in view) { report(`view.${name}`) }
      return undefined
    },
  })

  const call = (handlers) => {
    for (const handler of [...handlers]) {
      try {
        handler()
      } catch (error) {
        console.error(error)
      }
    }
  }
  const run = () => {
    const generation = ++state.generation
    state.container.replaceChildren()
    state.watchers = []
    state.msg = []
    accessed.clear()
    state.children.clear()
    for (const name of LIFECYCLE) { lifecycle.set(name, []) }
    let output
    try {
      output = state.render({view: view_proxy, model: model_proxy, data, el: state.container})
    } catch (error) {
      console.error(error)
      report(`a render function that fails: ${error}`)
      return
    }
    Promise.resolve(output).then((out) => {
      if (generation !== state.generation || !state.mounted) { return }
      if (out instanceof Element) { state.container.replaceChildren(out) }
      call(lifecycle.get("after_render"))
      call(lifecycle.get("mounted"))
      call(lifecycle.get("after_layout"))
    }, (error) => {
      console.error(error)
      report(`a render function that fails: ${error}`)
    })
  }
  // The views of the children that render through Bokeh are built
  // asynchronously, after the patch that adds them has been applied.
  const children_ready = async () => {
    const fallbacks = () => Object.keys(node().children ?? {}).flatMap(child_list).filter(child => child.kind === "fallback")
    for (let attempt = 0; attempt < 40; attempt++) {
      if (fallbacks().every(child => fallback_model(child) && view.get_child_view(fallback_model(child)))) { return }
      await new Promise(resolve => setTimeout(resolve, attempt < 5 ? 0 : 25))
    }
  }
  const notify = () => {
    if (!state.mounted) { return }
    const changed = state.watchers.filter((watcher) => {
      const current = snapshot(watcher.name)
      const differs = !same_value(watcher.seen, current)
      watcher.seen = current
      return differs
    })
    let rerender = false
    for (const [name, seen] of state.children) {
      const current = snapshot(name)
      if (seen !== current) {
        state.children.set(name, current)
        rerender = true
      }
    }
    const fire = (watcher) => {
      const event = prototype.events?.includes(watcher.name)
      if (event && !node().props[watcher.name]) { return }
      try {
        watcher.callback()
      } catch (error) {
        console.error(error)
      }
      if (event) { store.set_local(id, watcher.name, false) }
    }
    changed.filter(watcher => !is_child(watcher.name)).forEach(fire)
    const children = changed.filter(watcher => is_child(watcher.name))
    if (!children.length && !rerender) { return }
    const generation = state.generation
    children_ready().then(() => {
      if (!state.mounted || generation !== state.generation) { return }
      if (rerender && store.state.kinds[node().kind].render_policy !== "manual") {
        run()
      } else {
        children.forEach(fire)
      }
    })
  }
  let unlisten = null
  let observer = null
  let moves = null
  const attachments = new Map()
  const moved = (records) => {
    const added = records.flatMap(record => [...record.addedNodes]).filter(added => added.nodeType === 1)
    if (!added.length) { return }
    for (const child of Object.keys(node().children ?? {}).flatMap(child_list)) {
      const el = slots.get(child.id)
      if (el && added.some(parent => parent === el || parent.contains(el))) {
        attachments.get(el)?.forEach(callback => callback())
        restyle(child)
      }
    }
  }
  return {
    slot,
    // Calls back whenever the component places the element in the page.
    on_attach(el, callback) {
      if (!attachments.has(el)) { attachments.set(el, new Set()) }
      attachments.get(el).add(callback)
      return () => attachments.get(el)?.delete(callback)
    },
    prune(ids) {
      for (const child_id of [...slots.keys()]) {
        if (!ids.has(child_id)) {
          attachments.delete(slots.get(child_id))
          slots.get(child_id).remove()
          slots.delete(child_id)
          child_models.delete(child_id)
        }
      }
    },
    receive: (data) => state.msg.forEach(handler => handler(data)),
    mount(container, render) {
      state.container = container
      state.host = container.parentElement
      state.render = render
      state.mounted = true
      unlisten = store.listen(id, notify)
      observer = new ResizeObserver(() => {
        call(lifecycle.get("resize"))
        call(lifecycle.get("after_layout"))
      })
      observer.observe(state.host)
      moves = new MutationObserver(moved)
      moves.observe(container, {childList: true, subtree: true})
      run()
    },
    unmount() {
      state.mounted = false
      state.generation++
      unlisten?.()
      observer?.disconnect()
      moves?.disconnect()
      call(lifecycle.get("remove"))
    },
  }
}

function EsmNode({node}) {
  const context = React.useContext(CompiledContext)
  const {model, view} = context
  const id = node.id
  const [prototype, setPrototype] = React.useState(() => view.model.data._prototypes?.[node.kind])
  const [render, setRender] = React.useState(() => esm_renderers.get(node.kind))
  const container = React.useRef(null)
  const instance = React.useRef(null)
  React.useEffect(() => {
    if (prototype != null) { return }
    const update = () => setPrototype(view.model.data._prototypes?.[node.kind])
    update()
    view.model_proxy.on("_prototypes", update)
    return () => view.model_proxy.off("_prototypes", update)
  }, [prototype])
  React.useEffect(() => {
    if (prototype == null || render != null) { return }
    let active = true
    Promise.resolve(prototype.compiled_module).then((mod) => {
      const fn = mod?.default?.render ?? mod?.render
      if (fn == null) {
        model.send_msg({type: "esm_unsupported", id, reason: "a module without a render function"})
      } else if (active) {
        esm_renderers.set(node.kind, fn)
        setRender(() => fn)
      }
    })
    return () => { active = false }
  }, [prototype, render])
  if (prototype != null && instance.current == null) {
    instance.current = make_esm(context, id, prototype)
  }
  React.useLayoutEffect(() => {
    if (render == null || instance.current == null) { return }
    const esm = instance.current
    esm.mount(container.current, render)
    const stop = model.on("msg", (msg) => {
      if (msg.type === "node_msg" && msg.id === id) { esm.receive(msg.data) }
    })
    return () => {
      stop()
      esm.unmount()
    }
  }, [render, id])
  const children = child_nodes(node)
  React.useEffect(() => instance.current?.prune(new Set(children.map(child => child.id))))
  return <>
    <div ref={container} style={{display: "contents"}}/>
    {instance.current && children.map(child => (
      <SlotNode key={child.id} nid={child.id} slot={instance.current.slot(child)} esm={instance.current}/>
    ))}
  </>
}

function same_style(a, b) {
  if (a === b) { return true }
  if (a == null || b == null) { return false }
  const names = Object.keys(a)
  return names.length === Object.keys(b).length && names.every(name => a[name] === b[name])
}

// A node renders when its own state changes, not when its parent does.
const Node = React.memo(NodeHost, (prev, next) => (
  prev.nid === next.nid && prev.direction === next.direction && prev.fill === next.fill &&
  same_style(prev.extra, next.extra)
))

const FILL = {
  width: "100%", height: "100%", margin: "0px", minWidth: undefined, minHeight: undefined,
  maxWidth: undefined, maxHeight: undefined, aspectRatio: undefined,
}

// Renders a child of a JSComponent into the element the component places
// in the DOM itself. A compiled child gets a shadow root, so that it is as
// opaque to the queries and the stylesheets of its parent as a view.
function SlotNode({nid, slot, esm}) {
  const {store} = React.useContext(CompiledContext)
  const node = useNode(store, nid)
  // A view renders once its element is in the page, as it does when Panel
  // renders the children of a component, so that it is sized only once.
  const [attached, setAttached] = React.useState(slot.isConnected)
  React.useEffect(() => {
    if (slot.isConnected) { setAttached(true) }
    return esm.on_attach(slot, () => setAttached(true))
  }, [slot, esm])
  const sealed = React.useMemo(() => {
    if (node == null || node.kind === "fallback") { return null }
    const root = slot.shadowRoot ?? slot.attachShadow({mode: "open"})
    const overlays = document.createElement("div")
    overlays.style.display = "contents"
    root.append(overlays)
    // The parent attaches and moves the element, which drops the rules a
    // stylesheet was given through the CSSOM, so they are written as text.
    const cache = createCache({key: "pnl", prepend: true, container: root, speedy: false})
    const entry = {root, overlays, cache}
    store.roots.set(nid, entry)
    return entry
  }, [slot, nid, node == null || node.kind === "fallback"])
  React.useEffect(() => () => { store.roots.delete(nid) }, [nid])
  const fallback = node?.kind === "fallback"
  const layout = node == null ? null : fallback ? {
    width: ["stretch_width", "stretch_both", "scale_width", "scale_both"].includes(node.sizing_mode) ? "100%" : "fit-content",
    height: ["stretch_height", "stretch_both", "scale_height", "scale_both"].includes(node.sizing_mode) ? "100%" : "fit-content",
  } : {...hostLayout(node), display: node.visible ? undefined : "none"}
  const declared = layout == null ? [] : Object.entries(layout).filter(([, value]) => value !== undefined)
    .map(([name, value]) => [name.replace(/[A-Z]/g, char => `-${char.toLowerCase()}`), value])
  const applied = React.useRef([])
  // Only the declarations of the layout, the parent styles the element too.
  React.useLayoutEffect(() => {
    slot.dataset.pmuiSlot = ""
    for (const name of applied.current) {
      if (!declared.some(([current]) => current === name)) { slot.style.removeProperty(name) }
    }
    for (const [name, value] of declared) { slot.style.setProperty(name, value) }
    applied.current = declared.map(([name]) => name)
  }, [slot, JSON.stringify(declared)])
  if (node == null) {
    return null
  }
  if (fallback) {
    return attached ? createPortal(<Fallback node={node} immediate/>, slot) : null
  }
  return createPortal(
    <CacheProvider value={sealed.cache}>
      <SharedStyles store={store}/>
      <Node nid={nid} extra={FILL} fill/>
    </CacheProvider>, sealed.root
  )
}

function NodeHost({nid, direction, extra, fill}) {
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
    return <Fallback node={node} direction={direction} extra={extra}/>
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
  const esm = Boolean(store.state.kinds[node.kind]?.esm)
  const className = [
    node.kind.split(".").pop().replace(/([a-z])([A-Z])/g, "$1-$2").toLowerCase(), ...node.css_classes,
  ].join(" ")
  // A node that fills a slot is sized by the slot.
  const style = fill ? {} : {
    width: size("width", horizontal, width), height: size("height", vertical, height),
    minWidth: min_width ?? undefined, minHeight: min_height ?? undefined,
    maxWidth: max_width ?? undefined, maxHeight: max_height ?? undefined,
    display: node.visible ? undefined : "none",
  }
  const content = <>
    {node.stylesheets.some(sheet => sheet.url) && <NodeStyles node={node} model={model}/>}
    {esm ? <EsmNode key={node.id} node={node}/> : <MaterialNode key={node.id} node={node}/>}
  </>
  return <div ref={host} id={`pmui-${node.id}`} data-pmui-host="" data-pmui-layout={store.layout_key(declarations)}
    data-pmui-css={shared || undefined} className={className} style={style}
  >
    {content}
  </div>
}

// Runs when the model is created, before the views of the children that
// render through Bokeh are built.
export function initialize({model}) {
  const tree = model.tree
  const root = tree?.root
  if (root?.kind !== "Page") {
    return
  }
  const props = {...tree.kinds.Page.props, ...root.props}
  theme_document_early(model.document, props.theme_config, props.dark_theme, model._custom_theme)
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
    const context = {store, model, view, host}
    // Tells the host of a child that renders through its own view where
    // the tree places it, see make_host.
    view.pmui_placement = (id) => {
      const slot = (model.get("fallbacks") ?? []).findIndex(fallback => fallback.id === id)
      const parent_id = store.slot_parent(slot)
      if (parent_id === undefined) {
        return undefined
      }
      return {parent: parent_id == null ? null : node_host(context, parent_id).host, root: parent_id == null}
    }
    return context
  })
  React.useLayoutEffect(() => store.reset(tree), [tree])
  React.useEffect(() => {
    // A patch that arrives with a rebuilt tree builds on that tree, which
    // the store only loads once this component has rendered it.
    const apply = () => {
      store.reset(model.get("tree"))
      store.apply(model.get("patch"))
    }
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
