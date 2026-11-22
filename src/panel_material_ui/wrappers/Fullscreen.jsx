import Box from "@mui/material/Box"
import IconButton from "@mui/material/IconButton"
import FullscreenIcon from "@mui/icons-material/Fullscreen"
import FullscreenExitIcon from "@mui/icons-material/FullscreenExit"
import {useTheme} from "@mui/material/styles"

const TOGGLE_CLASS = "pmui-fullscreen-toggle"
const EXIT_CLASS = "pmui-fullscreen-exit"
const KEEP_CLASS = "pmui-fullscreen-keep"
const TOGGLE_EVENT = "pmui:fullscreen-toggle"
const HOST_ATTR = "data-pmui-fullscreen-host"
const ACTIVE_ATTR = "data-pmui-fullscreen"

// Above app bars (1100) and drawers (1200), below modals (1300) and
// snackbars (1400), so what the child opens still shows over it.
const COVER_CSS = `
:host([${ACTIVE_ATTR}]) {
  position: fixed !important;
  inset: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  height: 100dvh !important;
  min-width: 0 !important;
  min-height: 0 !important;
  max-width: none !important;
  max-height: none !important;
  margin: 0 !important;
  box-sizing: border-box !important;
  padding: env(safe-area-inset-top, 0) env(safe-area-inset-right, 0) env(safe-area-inset-bottom, 0) env(safe-area-inset-left, 0) !important;
  z-index: 1250 !important;
  background: var(--pmui-fullscreen-background) !important;
  color: var(--pmui-fullscreen-color) !important;
  color-scheme: var(--pmui-fullscreen-scheme, normal);
}
:host([${ACTIVE_ATTR}]) > div {
  width: 100% !important;
  height: 100% !important;
}
`

// Every wrapper on the page, in the order they were rendered.
if (globalThis.__pmuiFullscreen == null) {
  globalThis.__pmuiFullscreen = []
}
const WRAPPERS = globalThis.__pmuiFullscreen

// Safari before 16.4 only offers the prefixed API; iPhone Safari offers none,
// so the child covers the window instead.
function fullscreenElement() {
  return document.fullscreenElement ?? document.webkitFullscreenElement ?? null
}

function fullscreenSupported() {
  const page = document.documentElement
  return !!(
    (document.fullscreenEnabled && page.requestFullscreen) ||
    (document.webkitFullscreenEnabled && page.webkitRequestFullscreen)
  )
}

function requestFullscreen(el) {
  try {
    const result = el.requestFullscreen ? el.requestFullscreen({navigationUI: "hide"}) : el.webkitRequestFullscreen()
    return Promise.resolve(result)
  } catch (error) {
    return Promise.reject(error)
  }
}

function exitFullscreen() {
  try {
    return Promise.resolve(document.exitFullscreen ? document.exitFullscreen() : document.webkitExitFullscreen())
  } catch (error) {
    return Promise.reject(error)
  }
}

function typing(target) {
  const tag = target?.tagName
  return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || !!target?.isContentEditable
}

function isOverlay(node) {
  return node instanceof Element && (
    node.getAttribute("role") === "dialog" || node.getAttribute("aria-modal") === "true" ||
    node.getAttribute("role") === "presentation" || node.hasAttribute("popover") ||
    node.classList.contains("MuiModal-root") || node.classList.contains("MuiPopover-root") ||
    node.classList.contains("MuiPopper-root")
  )
}

// Never made inert: dialogs, menus and notifications the child opens may be
// rendered outside it.
const LIVE_TAGS = new Set(["SCRIPT", "STYLE", "LINK", "HEAD", "TEMPLATE"])
const LIVE_SELECTORS = [`.${KEEP_CLASS}`, ".dialog", ".notification-area", "#notistack-container", ".MuiModal-root"]

// A node and, for Panel's wrappers, the component elements directly inside it.
function hosts(node) {
  return [node, ...node.children].filter((el) => el.shadowRoot)
}

function inertable(node) {
  if (!(node instanceof HTMLElement) || node.inert || LIVE_TAGS.has(node.tagName) || isOverlay(node)) {
    return false
  }
  return !LIVE_SELECTORS.some((sel) => (
    node.matches(sel) || hosts(node).some((host) => [...host.shadowRoot.children].some((el) => el.matches(sel)))
  ))
}

// The focused element, which may sit in shadow roots, and its ancestors.
function focusPath() {
  const path = []
  let node = document.activeElement
  while (node?.shadowRoot?.activeElement) {
    node = node.shadowRoot.activeElement
  }
  while (node) {
    path.push(node)
    node = node.parentNode ?? node.host
  }
  return path
}

function chosen() {
  const live = WRAPPERS.filter((c) => c.host.isConnected && !c.model.disabled)
  const path = focusPath()
  return live.find((c) => path.includes(c.host)) ?? live.find((c) => c.model.active) ?? live[0]
}

class Controller {
  constructor(model, view, onActivity) {
    this.model = model
    this.view = view
    this.onActivity = onActivity
    this.owned = false
    this.pending = false
    this.wasNative = false
    this.covering = false
    this.inerted = []
    this.observers = []
    this.saved = null
  }

  get host() {
    return this.view.el
  }

  isNative() {
    return this.owned && fullscreenElement() === document.documentElement
  }

  requestNative() {
    if (!this.model.supported || this.pending || fullscreenElement() != null) {
      return
    }
    // Without a gesture the browser refuses, so the child stays in the window
    // rather than logging a refused request.
    if (navigator.userActivation && !navigator.userActivation.isActive) {
      return
    }
    this.pending = true
    requestFullscreen(document.documentElement)
      .then(() => { this.owned = true; this.sync() })
      .catch(() => {})
      .finally(() => { this.pending = false })
  }

  exitNative() {
    if (this.isNative()) {
      exitFullscreen().catch(() => {})
    }
  }

  enter() {
    if (this.model.disabled) {
      return
    }
    if (!this.model.active) {
      this.model.active = true
    }
    this.requestNative()
  }

  leave() {
    if (this.model.active) {
      this.model.active = false
    }
    this.exitNative()
  }

  toggle() {
    if (this.model.active) {
      this.leave()
    } else {
      this.enter()
    }
  }

  // Reflects the browser's full screen state in the model.
  sync() {
    if (fullscreenElement() !== document.documentElement) {
      this.owned = false
    }
    const now = this.isNative()
    if (this.model.native !== now) {
      this.model.native = now
    }
    if (this.wasNative && !now && this.model.active) {
      this.model.active = false
    }
    this.wasNative = now
    this.onActivity()
  }

  apply(active, initial = false) {
    if (active) {
      this.cover()
      // Rendered already active, e.g. from a link: no gesture, so no real full screen.
      if (!initial) {
        this.requestNative()
      }
    } else {
      this.uncover()
      this.exitNative()
    }
  }

  cover() {
    const host = this.host
    const root = host.shadowRoot
    if (root && root.querySelector(":scope > style[data-pmui-fullscreen-style]") == null) {
      const style = document.createElement("style")
      style.dataset.pmuiFullscreenStyle = ""
      style.textContent = COVER_CSS
      root.prepend(style)
    }
    if (!this.covering) {
      const scroller = document.scrollingElement ?? document.documentElement
      this.saved = {
        top: scroller.scrollTop,
        left: scroller.scrollLeft,
        overflow: document.documentElement.style.overflow,
        // The trigger, e.g. a toggle outside the child, turns inert below.
        focus: focusPath()[0] ?? null,
      }
      // Keeps the page behind from scrolling, e.g. on iOS where the cover is not real full screen.
      document.documentElement.style.overflow = "hidden"
      this.covering = true
    }
    host.setAttribute(ACTIVE_ATTR, "")
    if (this.model.inert) {
      this.contain()
    } else {
      this.release()
    }
    // Focus moves into the child; a tabindex on the host itself would take
    // its whole shadow tree out of the tab order.
    const box = root?.querySelector(".pmui-fullscreen")
    if (box && !focusPath().includes(host)) {
      box.focus({preventScroll: true})
    }
  }

  uncover() {
    this.host.removeAttribute(ACTIVE_ATTR)
    this.host.style.cursor = ""
    this.release()
    if (this.covering) {
      this.covering = false
      const {top, left, overflow, focus} = this.saved
      document.documentElement.style.overflow = overflow
      const scroller = document.scrollingElement ?? document.documentElement
      scroller.scrollTo(left, top)
      // Back to the trigger, unless focus has moved on outside the child.
      const path = focusPath()
      if (focus?.isConnected && (path.length === 0 || path.includes(this.host) || path[0] === document.body)) {
        focus.focus({preventScroll: true})
      }
    }
  }

  makeInert(node) {
    if (inertable(node)) {
      node.inert = true
      this.inerted.push(node)
    }
  }

  // Everything outside the child is inert: every sibling at each level from
  // the wrapper up to the body, across shadow roots. Siblings rendered later
  // are made inert too.
  contain() {
    this.release()
    let node = this.host
    while (node && node !== document.body) {
      const parent = node.parentNode
      if (parent == null) {
        break
      }
      const keep = node
      for (const sibling of parent.children) {
        if (sibling !== keep) {
          this.makeInert(sibling)
        }
      }
      const observer = new MutationObserver((records) => {
        for (const record of records) {
          record.addedNodes.forEach((added) => added !== keep && this.makeInert(added))
        }
      })
      observer.observe(parent, {childList: true})
      this.observers.push(observer)
      node = parent instanceof ShadowRoot ? parent.host : parent
    }
  }

  release() {
    this.observers.forEach((observer) => observer.disconnect())
    this.inerted.forEach((node) => { node.inert = false })
    this.observers = []
    this.inerted = []
  }

  onClick(event) {
    const host = this.host
    const path = event.composedPath()
    const own = this.model.toggle_class
    if (own && path.some((node) => node instanceof Element && node.classList.contains(own))) {
      this.toggle()
      return
    }
    if (!path.includes(host)) {
      return
    }
    for (const node of path) {
      if (node === host || (node instanceof Element && node.hasAttribute(HOST_ATTR))) {
        // Toggles inside a nested wrapper belong to that wrapper.
        return
      }
      if (!(node instanceof Element)) {
        continue
      }
      if (node.classList.contains(EXIT_CLASS)) {
        this.leave()
        return
      }
      if (node.classList.contains(TOGGLE_CLASS)) {
        this.toggle()
        return
      }
    }
  }

  onRequest(event) {
    if (!event.defaultPrevented && chosen() === this) {
      event.preventDefault()
      this.toggle()
    }
  }

  onKey(event) {
    // The browser leaves real full screen on Escape itself; the cover follows it.
    if (event.key !== "Escape" || !this.model.active || this.isNative() || event.defaultPrevented) {
      return
    }
    const path = event.composedPath()
    const inDialog = path.some((node) => node instanceof Element && (
      node.getAttribute("role") === "dialog" || node.getAttribute("aria-modal") === "true"
    ))
    if (!inDialog && !typing(path[0])) {
      this.leave()
    }
  }

  connect() {
    this.host.setAttribute(HOST_ATTR, "")
    this.model.supported = fullscreenSupported()
    this.handlers = {
      change: () => this.sync(),
      click: (event) => this.onClick(event),
      request: (event) => this.onRequest(event),
      key: (event) => this.onKey(event),
    }
    for (const name of ["fullscreenchange", "webkitfullscreenchange"]) {
      document.addEventListener(name, this.handlers.change)
    }
    document.addEventListener("click", this.handlers.click, true)
    document.addEventListener(TOGGLE_EVENT, this.handlers.request)
    document.addEventListener("keydown", this.handlers.key)
    WRAPPERS.push(this)
  }

  disconnect() {
    for (const name of ["fullscreenchange", "webkitfullscreenchange"]) {
      document.removeEventListener(name, this.handlers.change)
    }
    document.removeEventListener("click", this.handlers.click, true)
    document.removeEventListener(TOGGLE_EVENT, this.handlers.request)
    document.removeEventListener("keydown", this.handlers.key)
    this.uncover()
    this.exitNative()
    const index = WRAPPERS.indexOf(this)
    if (index >= 0) {
      WRAPPERS.splice(index, 1)
    }
  }
}

const OFFSET = 8
const GAP = 4

// A child with a header (a Card) keeps its own actions, e.g. the collapse
// chevron, in the top right corner: the overlay sits beside them, centered on
// the header row, rather than over them.
function headerAnchor(root, childEl) {
  const header = childEl?.shadowRoot?.querySelector(".MuiCardHeader-root")
  if (!root || !header) {
    return null
  }
  const box = root.getBoundingClientRect()
  const head = header.getBoundingClientRect()
  if (head.height === 0) {
    return null
  }
  const action = header.querySelector(".MuiCardHeader-action")
  const actionBox = action?.getBoundingClientRect()
  const right = actionBox?.width ? box.right - actionBox.left + GAP : box.right - head.right + OFFSET
  return {center: Math.round(head.top + head.height / 2 - box.top), right: Math.round(right)}
}

function placementSx(placement, anchor) {
  const [vertical, horizontal] = placement.split("-")
  if (anchor && placement === "top-right") {
    return {top: `${anchor.center}px`, right: `${anchor.right}px`, transform: "translateY(-50%)"}
  }
  return {[vertical]: `${OFFSET}px`, [horizontal]: `${OFFSET}px`}
}

export function render({model, view}) {
  const [active] = model.useState("active")
  const [disabled] = model.useState("disabled")
  const [hide_delay] = model.useState("hide_delay")
  const [inert] = model.useState("inert")
  const [label] = model.useState("label")
  const [placement] = model.useState("placement")
  const [show_button] = model.useState("show_button")
  const [sx] = model.useState("sx")
  const object = model.get_child("object")
  const toolbar = model.get_child("toolbar")
  const theme = useTheme()

  // Whether the toolbar shows in full screen: after activity, until the pointer and keys rest.
  const [shown, setShown] = React.useState(true)
  const timer = React.useRef(null)
  const overlayRef = React.useRef(null)
  const delayRef = React.useRef(hide_delay)
  delayRef.current = hide_delay

  const rest = React.useCallback(() => {
    const box = overlayRef.current
    if (box && (box.matches(":hover") || box.querySelector(":focus-visible"))) {
      timer.current = setTimeout(rest, delayRef.current)
      return
    }
    setShown(false)
  }, [])
  const activity = React.useCallback(() => {
    clearTimeout(timer.current)
    setShown(true)
    if (model.active && delayRef.current != null) {
      timer.current = setTimeout(rest, delayRef.current)
    }
  }, [])

  const controller = React.useMemo(() => new Controller(model, view, activity), [])

  React.useEffect(() => {
    controller.connect()
    const onMove = () => model.active && activity()
    document.addEventListener("pointermove", onMove)
    document.addEventListener("pointerdown", onMove, true)
    document.addEventListener("keydown", onMove, true)
    return () => {
      clearTimeout(timer.current)
      document.removeEventListener("pointermove", onMove)
      document.removeEventListener("pointerdown", onMove, true)
      document.removeEventListener("keydown", onMove, true)
      controller.disconnect()
    }
  }, [])

  const mounted = React.useRef(false)
  React.useEffect(() => {
    controller.apply(active, !mounted.current)
    mounted.current = true
    activity()
  }, [active])

  React.useEffect(() => {
    if (model.active) {
      controller.cover()
    }
  }, [inert])

  React.useEffect(() => {
    view.el.style.setProperty("--pmui-fullscreen-background", theme.palette.background.default)
    view.el.style.setProperty("--pmui-fullscreen-color", theme.palette.text.primary)
    view.el.style.setProperty("--pmui-fullscreen-scheme", theme.palette.mode)
  }, [theme.palette.background.default, theme.palette.text.primary, theme.palette.mode])

  const rootRef = React.useRef(null)
  const [anchor, setAnchor] = React.useState(null)
  React.useEffect(() => {
    const root = rootRef.current
    if (root == null) {
      return
    }
    const childEl = () => (model.object ? view.get_child_view(model.object)?.el : null)
    const measure = () => {
      const next = headerAnchor(root, childEl())
      setAnchor((prev) => (
        prev?.center === next?.center && prev?.right === next?.right ? prev : next
      ))
    }
    const resize = new ResizeObserver(measure)
    resize.observe(root)
    const el = childEl()
    if (el) {
      resize.observe(el)
    }
    // The child renders its header after the wrapper mounts.
    const mutation = new MutationObserver(measure)
    if (el?.shadowRoot) {
      mutation.observe(el.shadowRoot, {childList: true, subtree: true})
    }
    measure()
    const frame = requestAnimationFrame(measure)
    return () => {
      cancelAnimationFrame(frame)
      resize.disconnect()
      mutation.disconnect()
    }
  }, [object, active])

  const hidden = active && !shown && hide_delay != null
  React.useEffect(() => {
    view.el.style.cursor = hidden ? "none" : ""
  }, [hidden])

  const hasOverlay = show_button || (active && toolbar.length > 0)
  // In the page the button always shows, so keyboard and touch users find it.
  const overlayVisible = active ? !hidden : true

  // Beside a Card's header actions the overlay comes first in the DOM, so
  // the tab order follows the visual order: toggle, then the card's own actions.
  const overlayFirst = anchor != null && placement === "top-right"
  const overlay = hasOverlay ? (
    <Box
      ref={overlayRef}
      className="pmui-fullscreen-overlay"
      role="region"
      aria-label={label}
      sx={{
        position: "absolute",
        zIndex: 2,
        display: "flex",
        alignItems: "center",
        gap: 0.5,
        p: active && toolbar.length ? 0.5 : 0,
        borderRadius: "20px",
        bgcolor: active && toolbar.length ? "background.paper" : "transparent",
        border: active && toolbar.length ? 1 : 0,
        borderColor: "divider",
        boxShadow: active && toolbar.length ? 3 : 0,
        transition: "opacity 0.2s",
        opacity: overlayVisible ? 1 : 0,
        // Hidden in full screen it takes no clicks.
        pointerEvents: overlayVisible ? "auto" : "none",
        "@media (prefers-reduced-motion: reduce)": {transition: "none"},
        ...placementSx(placement, anchor),
      }}
    >
      {active && toolbar}
      {show_button && (
        <IconButton
          aria-label={active ? "Exit full screen" : "Enter full screen"}
          disabled={disabled && !active}
          onClick={() => controller.toggle()}
          size="small"
          // Low emphasis at rest; a raised button over the child in full screen.
          sx={active ? (toolbar.length ? {} : {
            bgcolor: "background.paper",
            boxShadow: 1,
            "&:hover": {bgcolor: "background.paper"},
          }) : {color: "text.secondary"}}
        >
          {active ? <FullscreenExitIcon /> : <FullscreenIcon />}
        </IconButton>
      )}
    </Box>
  ) : null

  return (
    <Box
      ref={rootRef}
      className="pmui-fullscreen"
      tabIndex={-1}
      sx={{
        outline: "none",
        position: "relative",
        width: "100%",
        height: "100%",
        "& .pmui-fullscreen-overlay:has(:focus-visible)": {opacity: 1, pointerEvents: "auto"},
        ...sx,
      }}
    >
      {overlayFirst && overlay}
      {object}
      {!overlayFirst && overlay}
    </Box>
  )
}
