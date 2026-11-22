import {useTheme} from "@mui/material/styles"

// Panel's components live in nested shadow roots, which querySelector does not reach.
function collect(root, cls, found) {
  for (const el of root.querySelectorAll("*")) {
    if (el.classList.contains(cls)) {
      found.push(el)
    }
    if (el.shadowRoot) {
      collect(el.shadowRoot, cls, found)
    }
  }
  return found
}

function reducedMotion() {
  return window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ?? false
}

// The styles each outlined element had before it was first outlined, and its
// pending timer, so a repeated outline restores the original styles.
const OUTLINED = new WeakMap()

function outline(el, color, duration, reduce) {
  let state = OUTLINED.get(el)
  if (state === undefined) {
    state = {styles: [el.style.outline, el.style.outlineOffset, el.style.transition], timer: null}
    OUTLINED.set(el, state)
  }
  clearTimeout(state.timer)
  const restore = () => {
    [el.style.outline, el.style.outlineOffset, el.style.transition] = state.styles
    OUTLINED.delete(el)
  }
  el.style.transition = reduce ? "none" : "outline-color 0.6s"
  el.style.outline = `3px solid ${color}`
  el.style.outlineOffset = "2px"
  state.timer = setTimeout(() => {
    if (reduce) {
      restore()
      return
    }
    el.style.outlineColor = "transparent"
    state.timer = setTimeout(restore, 700)
  }, duration)
}

export function render({model}) {
  const [color] = model.useState("color")
  const [duration] = model.useState("duration")
  const theme = useTheme()
  const outlineColor = (theme.palette[color] ?? theme.palette.primary).main

  const settings = React.useRef({})
  settings.current = {outlineColor, duration}

  React.useEffect(() => {
    const handler = (msg) => {
      let attempts = 0
      // The class may arrive in the same update as the request.
      const run = () => {
        const found = collect(document, msg.css_class, [])
        if (!found.length) {
          if (attempts++ < 20) {
            setTimeout(run, 50)
          }
          return
        }
        const reduce = reducedMotion()
        found.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top)
        const first = found[0]
        first.scrollIntoView({behavior: reduce ? "auto" : "smooth", block: msg.block ?? "center"})
        if (msg.focus) {
          if (!first.hasAttribute("tabindex")) {
            first.setAttribute("tabindex", "-1")
          }
          first.focus({preventScroll: true})
        }
        if (msg.highlight) {
          const {outlineColor, duration} = settings.current
          found.forEach((el) => outline(el, outlineColor, duration, reduce))
        }
      }
      run()
    }
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [])

  return <span style={{display: "none"}} />
}
