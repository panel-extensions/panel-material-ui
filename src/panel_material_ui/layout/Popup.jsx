import Popover from "@mui/material/Popover"
import {apply_flex, child_model, overlay_container} from "./utils"

const TRIGGER = "button, [role=button], a[href]"
const FOCUSABLE = "a[href], button, input, select, textarea, [tabindex], [contenteditable=true]"

function deep_find(root, selector) {
  if (root == null) { return null }
  const found = root.querySelector(selector)
  if (found) { return found }
  for (const el of root.querySelectorAll("*")) {
    if (el.shadowRoot) {
      const inner = deep_find(el.shadowRoot, selector)
      if (inner) { return inner }
    }
  }
  return null
}

function within(node, ancestor) {
  for (; node; node = node.parentNode || node.host) {
    if (node === ancestor) { return true }
  }
  return false
}

// Focusable elements in document order, looking into shadow roots.
function tabbables(root) {
  const found = []
  const walk = (node) => {
    for (const el of node.children) {
      if (el.matches(FOCUSABLE) && !el.disabled && el.tabIndex >= 0 && el.getClientRects().length) {
        found.push(el)
      }
      if (el.shadowRoot) { walk(el.shadowRoot) }
      walk(el)
    }
  }
  walk(root)
  return found
}

function closest_deep(node, selector) {
  for (; node; node = node.parentNode || node.host) {
    if (node.matches?.(selector)) { return node }
  }
  return null
}

function deep_active() {
  let el = document.activeElement
  while (el && el.shadowRoot && el.shadowRoot.activeElement) {
    el = el.shadowRoot.activeElement
  }
  return el
}

function accessible_name(el) {
  if (el == null) { return null }
  const name = el.getAttribute("aria-label") || el.getAttribute("title") || el.textContent?.trim()
  return name || null
}

export function render({model, view}, ref) {
  const [anchor_origin] = model.useState("anchor_origin")
  const [anchor_position] = model.useState("anchor_position")
  const [close_on_click] = model.useState("close_on_click")
  const [elevation] = model.useState("elevation")
  const [enforce_focus] = model.useState("enforce_focus")
  const [hide_backdrop] = model.useState("hide_backdrop")
  const [label] = model.useState("label")
  const [modal] = model.useState("modal")
  const [open, setOpen] = model.useState("open")
  const [sx] = model.useState("sx")
  const [transform_origin] = model.useState("transform_origin")
  const objects = model.get_child("objects")

  const anchorEl = view.parent?.child_views.includes(view) ? view.parent.el : null

  const paperRef = React.useRef(null)
  const triggerRef = React.useRef(null)
  // Whether closing should return the focus to the trigger.
  const restoreRef = React.useRef(false)
  // Set while the focus may still have to come back once the popup unmounts.
  const pendingRef = React.useRef(false)
  const [name, setName] = React.useState(null)
  const nonModal = modal === false

  React.useEffect(() => {
    const handler = () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(child_model(model.objects, object, index)), "column")
      })
    }
    model.on("lifecycle:update_layout", handler)
    return () => model.off("lifecycle:update_layout", handler)
  }, [])

  // The trigger of a non-modal popup is the sibling that has the focus when
  // it opens, else the first button among the views it shares a parent with.
  const siblings = () => (view.parent?.child_views ?? []).filter((v) => v !== view)
  const find_trigger = () => {
    const active = deep_active()
    if (active && active !== document.body && siblings().some((v) => within(active, v.el))) {
      return active.closest(TRIGGER) ?? active
    }
    if (triggerRef.current?.isConnected) { return triggerRef.current }
    for (const sibling of siblings()) {
      const button = deep_find(sibling.el.shadowRoot ?? sibling.el, TRIGGER)
      if (button) { return button }
    }
    return null
  }

  const close = () => setOpen(false)

  const restore_focus = () => {
    const trigger = triggerRef.current
    if (!restoreRef.current || trigger == null || !trigger.isConnected) { return }
    const paper = paperRef.current
    const root = paper?.closest(".MuiPopover-root") ?? paper
    const active = deep_active()
    // Only take the focus back from the popup itself, never from an element
    // the user moved it to.
    if (active == null || active === document.body || !active.isConnected || (root && within(active, root))) {
      trigger.focus()
      pendingRef.current = true
    }
  }

  const onExited = () => {
    const trigger = triggerRef.current
    const active = deep_active()
    if (pendingRef.current && trigger?.isConnected && (active == null || active === document.body || !active.isConnected)) {
      trigger.focus()
    }
    pendingRef.current = false
  }

  React.useEffect(() => {
    if (!nonModal) { return }
    let frame = null
    let attempt = 0
    const sync = () => {
      const trigger = find_trigger()
      if (trigger == null) {
        if (attempt++ < 40) { frame = requestAnimationFrame(sync) }
        return
      }
      triggerRef.current = trigger
      trigger.setAttribute("aria-haspopup", "dialog")
      trigger.setAttribute("aria-expanded", String(open))
      setName(accessible_name(trigger))
    }
    sync()
    if (!open) {
      restore_focus()
      restoreRef.current = false
    }
    return () => cancelAnimationFrame(frame)
  }, [open, nonModal])

  React.useEffect(() => {
    if (!nonModal || !open) { return }
    const onPointerDown = (event) => {
      const paper = paperRef.current
      if (paper == null) { return }
      const path = event.composedPath()
      const trigger = triggerRef.current
      // A press on the trigger toggles the popup through its own click.
      if (path.includes(paper) || (trigger && path.includes(trigger))) { return }
      if (close_on_click) {
        restoreRef.current = false
        close()
      }
    }
    // The popup lives in an overlay layer at the end of the document, so Tab
    // on the trigger moves into the popup rather than past it.
    const onTriggerKeyDown = (event) => {
      if (event.key === "Tab" && !event.shiftKey && paperRef.current) {
        event.preventDefault()
        paperRef.current.focus()
      } else if (event.key === "Escape") {
        event.preventDefault()
        event.stopPropagation()
        close()
      }
    }
    const trigger = triggerRef.current
    document.addEventListener("pointerdown", onPointerDown, true)
    trigger?.addEventListener("keydown", onTriggerKeyDown)
    return () => {
      document.removeEventListener("pointerdown", onPointerDown, true)
      trigger?.removeEventListener("keydown", onTriggerKeyDown)
    }
  }, [open, nonModal, close_on_click])

  const onEnter = () => {
    const paper = paperRef.current
    const active = deep_active()
    const trigger = triggerRef.current
    // Leave the focus alone if it moved elsewhere while the popup opened.
    if (paper && (active == null || active === document.body || (trigger && within(active, trigger)))) {
      paper.focus()
    }
  }

  const onKeyDown = (event) => {
    if (event.key === "Escape") {
      event.preventDefault()
      event.stopPropagation()
      restoreRef.current = true
      close()
    } else if (event.key === "Tab") {
      const paper = paperRef.current
      const trigger = triggerRef.current
      const items = tabbables(paper)
      const active = deep_active()
      if (event.shiftKey && (active === paper || active === items[0])) {
        // Back to the trigger, leaving the popup open.
        if (trigger) {
          event.preventDefault()
          trigger.focus()
        }
      } else if (!event.shiftKey && (items.length === 0 || active === items[items.length - 1])) {
        event.preventDefault()
        restoreRef.current = true
        close()
      }
    }
  }

  const watchedRef = React.useRef(null)

  const watch_nested_modal = (el) => {
    const paper = paperRef.current
    const modal_root = el ? closest_deep(el, ".MuiModal-root") : null
    if (modal_root && paper && modal_root !== closest_deep(paper, ".MuiModal-root") && watchedRef.current !== modal_root) {
      watchedRef.current = modal_root
      watch_modal(modal_root)
    }
  }

  const onFocus = () => {
    restoreRef.current = true
    // The focus target is retargeted, so look it up once it has the focus.
    setTimeout(() => watch_nested_modal(deep_active()))
  }
  const onFocusRef = React.useRef(onFocus)
  onFocusRef.current = onFocus

  // MUI's focus trap replaces an onFocus prop on the paper, so listen natively.
  const focusListener = React.useRef((event) => onFocusRef.current(event)).current
  const setPaper = React.useCallback((el) => {
    paperRef.current?.removeEventListener("focusin", focusListener)
    paperRef.current = el
    el?.addEventListener("focusin", focusListener)
  }, [])

  // A modal opened from inside the popup, e.g. a Dialog, keeps it open.
  // Once the modal closes, the focus comes back to the popup, or to the
  // trigger if the popup closed meanwhile, unless the user moved it elsewhere.
  const watch_modal = (modal_root) => {
    const parent = modal_root.parentNode
    const closed = () => !modal_root.isConnected || modal_root.getClientRects().length === 0 ||
      getComputedStyle(modal_root).visibility === "hidden"
    const check = () => {
      if (!closed()) { return }
      observer.disconnect()
      watchedRef.current = null
      const active = deep_active()
      if (active && active !== document.body && active.isConnected && !within(active, modal_root)) { return }
      const paper = paperRef.current
      const target = paper?.isConnected ? paper : triggerRef.current
      target?.focus()
    }
    const observer = new MutationObserver(check)
    observer.observe(modal_root, {attributes: true, childList: true, subtree: true})
    if (parent) { observer.observe(parent, {childList: true}) }
  }

  const onBlur = () => {
    // The focus target is retargeted to this shadow tree, so the element
    // that took the focus is only known once it has it.
    setTimeout(() => {
      const paper = paperRef.current
      const next = deep_active()
      const trigger = triggerRef.current
      // Focus leaving the window keeps the popup open, and so does focus on
      // the trigger, whose click toggles it.
      if (paper == null || next == null || next === document.body || within(next, paper)) { return }
      if (trigger && within(next, trigger)) { return }
      const own_root = closest_deep(paper, ".MuiModal-root")
      const modal_root = closest_deep(next, ".MuiModal-root")
      if (modal_root && modal_root !== own_root) {
        watch_nested_modal(next)
        return
      }
      close()
    })
  }

  const paperProps = {}
  if (nonModal || label) {
    paperProps.role = "dialog"
    paperProps["aria-label"] = (label || name) ?? undefined
  }
  if (nonModal) {
    Object.assign(paperProps, {
      "aria-modal": "false",
      onBlur,
      onKeyDown,
      style: {pointerEvents: "auto"},
      tabIndex: -1,
    })
  }

  return (
    <Popover
      anchorEl={anchorEl}
      anchorOrigin={anchor_origin}
      anchorPosition={anchor_position ? {left: anchor_position[1], top: anchor_position[0]} : undefined}
      anchorReference={anchor_position == null ? "anchorEl" : "anchorPosition"}
      container={overlay_container(view.container)}
      disableAutoFocus={nonModal}
      disableEnforceFocus={nonModal || !enforce_focus}
      disableRestoreFocus={nonModal}
      disableScrollLock={nonModal}
      elevation={elevation}
      marginThreshold={0}
      hideBackdrop={nonModal || hide_backdrop}
      onClose={() => close_on_click && setOpen(false)}
      open={open}
      slotProps={{
        paper: {ref: setPaper, ...paperProps},
        root: nonModal ? {style: {pointerEvents: "none"}} : undefined,
        transition: nonModal ? {onEnter, onExited} : undefined,
      }}
      sx={sx}
      transformOrigin={transform_origin ?? undefined}
    >
      {objects}
    </Popover>
  )
}
