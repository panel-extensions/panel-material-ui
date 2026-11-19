import pmui from "panel-material-ui"

const stylesheetRequests = new Map()
const NOOP_SIGNAL = {connect: () => {}, disconnect: () => {}}
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
      theme_revision: node.theme_revision ?? 0,
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
      if (patch.rev > state.rev + 1) {
        // A patch was missed, e.g. sent before this view was listening.
        model.send_msg({type: "resync"})
        return
      }
      state.rev = patch.rev
      for (const op of patch.ops) {
        const node = nodes.get(op.id)
        if (node == null) { continue }
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
          continue
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

function MaterialNode({node, parentView}) {
  const {store, model, view} = React.useContext(CompiledContext)
  const id = node.id
  const current = React.useRef({node, parentView})
  current.current = {node, parentView}
  const listeners = React.useRef(new Set())
  const setters = React.useRef(new Map())
  React.useEffect(() => {
    const receive = (msg) => {
      if (msg.type === "node_msg" && msg.id === id) {
        listeners.current.forEach(callback => callback(msg.data))
      }
    }
    model.on("msg:custom", receive)
    return () => model.off("msg:custom", receive)
  }, [model, id])

  const [componentModel] = React.useState(() => {
    const watchers = new Map()
    return new Proxy({
      useState: (name) => {
        const value = React.useSyncExternalStore(store.subscriber(id), () => store.get(id)?.props[name])
        if (!setters.current.has(name)) {
          setters.current.set(name, (next) => {
            const previous = store.get(id)?.props[name]
            const updated = typeof next === "function" ? next(previous) : next
            const seq = store.set_local(id, name, updated)
            model.send_msg({type: "update", id, name, value: updated, root: model.id, seq})
          })
        }
        return [value, setters.current.get(name)]
      },
      get_child: (name) => {
        const {node} = current.current
        const children = node.children[name]
        if (Array.isArray(children)) {
          const direction = node.kind === "Row" || node.kind === "Page" && name === "header" ? "row" :
            node.kind === "Column" || node.kind === "Page" ? "column" : null
          return children.map(child => <Node key={child.id} id={child.id} parentView={childView} direction={direction}/>)
        }
        return children ? <Node key={children.id} id={children.id} parentView={childView}/> : null
      },
      send_event: (name) => model.send_msg({type: name, id}),
      send_msg: (data) => model.send_msg({type: "msg", id, data}),
      on: (name, callback) => {
        if (name === "msg:custom") {
          listeners.current.add(callback)
        } else {
          const names = Array.isArray(name) ? name : [name]
          watchers.set(callback, store.listen(id, (changed) => {
            if (changed == null || changed.some(prop => names.includes(prop))) { callback() }
          }))
        }
      },
      off: (name, callback) => {
        if (name === "msg:custom") {
          listeners.current.delete(callback)
        } else {
          watchers.get(callback)?.()
          watchers.delete(callback)
        }
      },
    }, {
      get: (target, name) => {
        if (name in target) { return target[name] }
        const node = store.get(id) ?? current.current.node
        if (name === "esm_constants") { return node.constants }
        return name in node.props ? node.props[name] : node.children[name]
      },
    })
  })
  const [childView] = React.useState(() => ({
    el: view.container,
    container: view.container,
    root: view.root,
    shadow_el: view.shadow_el,
    model_proxy: view.model_proxy,
    is_root: false,
    get parent() { return current.current.parentView ?? view },
    get compiled_root() { return current.current.parentView == null ? view : null },
    get compiled_host_id() { return id },
    get theme_revision() { return current.current.node.theme_revision },
    get compiled_host() { return view.shadow_el.querySelector(`#pmui-${id}`) },
    get_child_view: (child) => child?.kind === "fallback" ?
      view.get_child_view(model.fallbacks[child.slot]) : null,
    model: {
      get id() { return id },
      get class_name() { return current.current.node.kind },
      get data() {
        const node = store.get(id) ?? current.current.node
        // Components identify their children by model, e.g. to tell
        // whether they are rendered in the header of the Page.
        const resolve = (child) => child && (store.models.get(child.id) ?? child)
        const children = Object.fromEntries(Object.entries(node.children).map(
          ([name, value]) => [name, Array.isArray(value) ? value.map(resolve) : resolve(value)]
        ))
        return {...children, ...node.props,
          _custom_theme: node.kind === "Page" ? model._custom_theme : node.props._custom_theme,
          properties: {}, change: NOOP_SIGNAL}
      },
      get document() { return model.document },
    },
  }))
  store.models.set(id, childView.model)
  React.useEffect(() => () => {
    if (store.models.get(id) === childView.model) { store.models.delete(id) }
  }, [])
  const Component = pmui[node.kind].render
  return <Component key={id} model={componentModel} view={childView} el={view.container}/>
}

function Node({id, parentView, direction}) {
  const {store, model} = React.useContext(CompiledContext)
  const fallbacks = React.useContext(FallbackContext)
  const node = useNode(store, id)
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
    return fallbacks[node.slot] ?? null
  }
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
    <MaterialNode key={node.id} node={node} parentView={parentView}/>
  </div>
}

export function render({model, view}) {
  const [tree] = model.useState("tree")
  const fallbacks = model.get_child("fallbacks")
  const [store] = React.useState(() => create_store(model, tree))
  const [context] = React.useState(() => ({store, model, view}))
  React.useLayoutEffect(() => store.reset(tree), [tree])
  React.useEffect(() => {
    const apply = () => store.apply(model.patch)
    model.on("patch", apply)
    apply()
    return () => model.off("patch", apply)
  }, [])
  return (
    <CompiledContext.Provider value={context}>
      <FallbackContext.Provider value={fallbacks}>
        <SharedStyles store={store}/>
        <Node id={tree.root.id}/>
      </FallbackContext.Provider>
    </CompiledContext.Provider>
  )
}
