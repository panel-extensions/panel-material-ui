import Box from "@mui/material/Box"
import {apply_flex} from "./utils"

const BOX_BASE_SX = {
  height: "100%",
  width: "100%",
  display: "flex",
  position: "relative",
}

export function render({model, view}) {
  const [sx] = model.useState("sx")
  const [auto_scroll_limit] = model.useState("auto_scroll_limit")
  const [scroll_button_threshold] = model.useState("scroll_button_threshold")
  const [scroll_index] = model.useState("scroll_index")
  const [scroll_position, setScrollPosition] = model.useState("scroll_position")
  const [view_latest] = model.useState("view_latest")
  const objects = model.get_child("objects")
  const flexDirection = model.esm_constants.direction
  const boxRef = React.useRef(null)
  const updatingRef = React.useRef(false)
  const userScrollingRef = React.useRef(false)
  const userScrollFramesRef = React.useRef(0)
  const userScrollRafRef = React.useRef(null)
  const prevObjectsLengthRef = React.useRef(objects.length)
  const [showScrollButton, setShowScrollButton] = React.useState(false)

  const isColumn = flexDirection === "column"
  const managedScroll = isColumn && (
    Boolean(view_latest) ||
    auto_scroll_limit > 0 ||
    scroll_button_threshold > 0 ||
    scroll_position > 0 ||
    scroll_index !== null
  )

  const distanceFromLatest = React.useCallback((el) => {
    return el.scrollHeight - el.scrollTop - el.clientHeight
  }, [])

  const updateScrollButton = React.useCallback((el) => {
    if (!managedScroll || scroll_button_threshold <= 0) {
      setShowScrollButton(false)
      return
    }
    setShowScrollButton(distanceFromLatest(el) >= scroll_button_threshold)
  }, [managedScroll, scroll_button_threshold, distanceFromLatest])

  const scrollToIndex = React.useCallback((index) => {
    const el = boxRef.current
    if (!el || index === null || index < 0) {
      return
    }
    const child = el.children.item(index)
    if (!child) {
      return
    }
    const relativeTop = child.offsetTop - el.offsetTop + el.scrollTop
    updatingRef.current = true
    setScrollPosition(Math.round(relativeTop))
    updatingRef.current = false
  }, [setScrollPosition])

  const scrollToLatest = React.useCallback((scrollLimit = null) => {
    const el = boxRef.current
    if (!el) {
      return
    }
    if (scrollLimit !== null && distanceFromLatest(el) > scrollLimit) {
      return
    }
    requestAnimationFrame(() => {
      updatingRef.current = true
      el.scrollTo({top: el.scrollHeight, behavior: "instant"})
      setScrollPosition(Math.round(el.scrollTop))
      updatingRef.current = false
      updateScrollButton(el)
    })
  }, [distanceFromLatest, setScrollPosition, updateScrollButton])

  React.useEffect(() => {
    const el = boxRef.current
    if (!managedScroll || !el) {
      return
    }
    const onScroll = () => {
      if (updatingRef.current) {
        return
      }
      userScrollingRef.current = true
      // Keep user-scrolling lock for a couple of animation frames
      // to avoid bouncing when synced scroll_position updates round-trip.
      userScrollFramesRef.current = 2
      if (userScrollRafRef.current === null) {
        const tick = () => {
          if (userScrollFramesRef.current > 0) {
            userScrollFramesRef.current -= 1
            userScrollRafRef.current = requestAnimationFrame(tick)
          } else {
            userScrollingRef.current = false
            userScrollRafRef.current = null
          }
        }
        userScrollRafRef.current = requestAnimationFrame(tick)
      }
      setScrollPosition(Math.round(el.scrollTop))
      updateScrollButton(el)
    }
    el.addEventListener("scroll", onScroll)
    updateScrollButton(el)
    return () => {
      el.removeEventListener("scroll", onScroll)
      if (userScrollRafRef.current !== null) {
        cancelAnimationFrame(userScrollRafRef.current)
        userScrollRafRef.current = null
      }
      userScrollFramesRef.current = 0
      userScrollingRef.current = false
    }
  }, [managedScroll, setScrollPosition, updateScrollButton])

  React.useEffect(() => {
    const el = boxRef.current
    if (!managedScroll || !el || updatingRef.current || userScrollingRef.current) {
      return
    }
    if (Math.abs(el.scrollTop - scroll_position) <= 1) {
      return
    }
    requestAnimationFrame(() => {
      updatingRef.current = true
      el.scrollTo({top: scroll_position, behavior: "instant"})
      updatingRef.current = false
      updateScrollButton(el)
    })
  }, [managedScroll, scroll_position, updateScrollButton])

  React.useEffect(() => {
    if (!managedScroll) {
      return
    }
    scrollToIndex(scroll_index)
  }, [managedScroll, scroll_index, scrollToIndex])

  React.useEffect(() => {
    const handler = (msg) => {
      if (msg?.type === "scroll_to") {
        scrollToIndex(msg.index)
      }
    }
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [model, scrollToIndex])

  React.useEffect(() => {
    const el = boxRef.current
    if (!managedScroll || !el) {
      prevObjectsLengthRef.current = objects.length
      return
    }
    if (view_latest && prevObjectsLengthRef.current === objects.length) {
      scrollToLatest()
    } else if (objects.length > prevObjectsLengthRef.current && auto_scroll_limit > 0) {
      scrollToLatest(auto_scroll_limit)
    }
    prevObjectsLengthRef.current = objects.length
  }, [managedScroll, objects.length, auto_scroll_limit, scrollToLatest, view_latest])

  let props = {}
  if (flexDirection === "flex") {
    const [alignItems] = model.useState("align_items")
    const [justifyContent] = model.useState("justify_content")
    const [gap] = model.useState("gap")
    const [flexWrap] = model.useState("flex_wrap")
    const [flex_direction] = model.useState("flex_direction")
    props = {
      alignItems,
      justifyContent,
      gap,
      flexWrap,
      flexDirection: flex_direction,
    }
  }

  React.useEffect(() => {
    const handler = () => {
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), flexDirection)
      })
    }
    model.on("lifecycle:update_layout", handler)
    return () => model.off("lifecycle:update_layout", handler)
  }, [])

  const boxSx = React.useMemo(
    () => [BOX_BASE_SX, {flexDirection}, managedScroll ? {overflowY: "auto"} : {}, props, sx || {}],
    [flexDirection, managedScroll, props, sx]
  )

  return (
    <Box
      ref={boxRef}
      sx={boxSx}
    >
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), flexDirection)
        return object
      })}
      {managedScroll && scroll_button_threshold > 0 && (
        <div
          role="button"
          tabIndex={0}
          aria-label="Scroll to latest"
          className={`scroll-button${showScrollButton ? " visible" : ""}`}
          onClick={() => {
            scrollToLatest()
            model.send_event("click", {})
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault()
              scrollToLatest()
              model.send_event("click", {})
            }
          }}
          style={{
            position: "sticky",
            top: "auto",
            bottom: "0.8rem",
            alignSelf: "flex-end",
            marginRight: "0.8rem",
            zIndex: 1,
            cursor: "pointer",
            display: showScrollButton ? "inline-flex" : "none",
          }}
        />
      )}
    </Box>
  )
}
