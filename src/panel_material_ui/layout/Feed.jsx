import Box from "@mui/material/Box"
import {
  apply_flex, child_at_latest, scroll_to_child, scroll_to_latest,
  update_scroll_button, use_latest_scroll_settlement
} from "./utils"

const FEED_BASE_SX = {
  minHeight: "100%",
  display: "flex",
  position: "relative",
  alignSelf: "stretch",
  boxSizing: "border-box",
  minWidth: 0,
}

export function render({model, view, el}) {
  const [sx] = model.useState("sx")
  const [scroll_button_threshold] = model.useState("scroll_button_threshold")
  const [scroll_index] = model.useState("scroll_index")
  const [scroll_position, setScrollPosition] = model.useState("scroll_position")
  const [view_latest] = model.useState("view_latest")
  const [visibleChildren, setVisibleChildren] = model.useState("visible_children")
  const objects = model.get_child("objects")
  const flexDirection = model.esm_constants.direction
  const boxRef = React.useRef(null)
  const syncingScrollRef = React.useRef(false)
  const [scrollbarWidth, setScrollbarWidth] = React.useState(0)
  const [showScrollButton, setShowScrollButton] = React.useState(false)
  const wrappersRef = React.useRef(new Map())
  const visibleSetRef = React.useRef(new Set(visibleChildren || []))
  const initialLatestDoneRef = React.useRef(!view_latest)
  const topAnchorRef = React.useRef(null)
  const pendingScrollLatestRef = React.useRef(false)
  const layoutUpdatedRef = React.useRef(false)
  const observerRef = React.useRef(null)
  const observedNodesRef = React.useRef(new Map())

  el.style.width = "100%"

  const updateScrollButton = React.useCallback((el) => {
    update_scroll_button(el, view.model.data.scroll_button_threshold, setShowScrollButton)
  }, [])

  const scrollToLatest = React.useCallback((scrollLimit = null) => {
    return scroll_to_latest(boxRef.current, syncingScrollRef, setScrollPosition, updateScrollButton, scrollLimit)
  }, [])

  const latestChildAtBottom = React.useCallback((el) => {
    const latest = model.objects[model.objects.length - 1]
    const node = latest ? wrappersRef.current.get(latest.id) : null
    return child_at_latest(el, node)
  }, [])

  const syncLatestVisibleChild = React.useCallback(() => {
    const latest = model.objects[model.objects.length - 1]
    const ordered = latest ? [latest.id] : []
    visibleSetRef.current = new Set(ordered)
    setVisibleChildren(ordered)
  }, [])

  const updateScrollbarWidth = React.useCallback((el = boxRef.current) => {
    if (!el) {
      return
    }
    const width = Math.max(el.offsetWidth - el.clientWidth, 0)
    setScrollbarWidth((current) => current === width ? current : width)
  }, [])

  const setBoxRef = React.useCallback((node) => {
    if (!node) {
      boxRef.current = null
      return
    }
    const root = node.getRootNode()
    const host = root instanceof ShadowRoot ? root.host : null
    boxRef.current = (
      node.closest(".scroll-vertical, .scrollable-vertical, .scrollable") ??
      host?.closest(".scroll-vertical, .scrollable-vertical, .scrollable") ??
      host ??
      node
    )
    updateScrollbarWidth(boxRef.current)
  }, [])

  const {startScrollLatestSettlement, stopScrollLatestSettlement, scrollSettledCallbackRef} = use_latest_scroll_settlement({
    boxRef,
    pendingScrollLatestRef,
    topAnchorRef,
    scrollToLatest,
    latestChildAtBottom,
    onDefaultSettled: syncLatestVisibleChild,
    layoutUpdatedRef,
  })

  const armScrollLatestAfterRender = React.useCallback(() => {
    pendingScrollLatestRef.current = true
    topAnchorRef.current = null
  }, [])

  const scrollToIndex = React.useCallback((index) => {
    const el = boxRef.current
    if (!el || index === null || index < 0) {
      return
    }
    const child = wrappersRef.current.get(model.objects[index]?.id)
    if (!child) {
      return
    }
    scroll_to_child(el, child, setScrollPosition)
  }, [])

  const captureTopAnchor = React.useCallback((el) => {
    const scrollTop = el.scrollTop
    for (const childModel of model.objects) {
      const node = wrappersRef.current.get(childModel.id)
      if (!node) {
        continue
      }
      const top = node.offsetTop - el.offsetTop
      const bottom = top + node.offsetHeight
      if (bottom > scrollTop + 1) {
        topAnchorRef.current = {id: childModel.id, viewportOffset: top - scrollTop}
        return
      }
    }
    topAnchorRef.current = null
  }, [])

  React.useEffect(() => {
    const el = boxRef.current
    if (!el) {
      return
    }
    const onScroll = () => {
      if (syncingScrollRef.current) {
        return
      }
      setScrollPosition(Math.round(el.scrollTop))
      updateScrollButton(el)
      captureTopAnchor(el)
    }
    el.addEventListener("scroll", onScroll)
    updateScrollButton(el)
    updateScrollbarWidth(el)
    captureTopAnchor(el)
    return () => el.removeEventListener("scroll", onScroll)
  }, [])

  React.useEffect(() => {
    const el = boxRef.current
    if (!el || syncingScrollRef.current) {
      return
    }
    if (Math.abs(el.scrollTop - scroll_position) <= 1) {
      return
    }
    syncingScrollRef.current = true
    el.scrollTo({top: scroll_position, behavior: "instant"})
    syncingScrollRef.current = false
    updateScrollButton(el)
  }, [])

  React.useEffect(() => {
    scrollToIndex(scroll_index)
  }, [scroll_index])

  React.useEffect(() => {
    const handler = (msg) => {
      if (msg?.type === "scroll_to") {
        scrollToIndex(msg.index)
      } else if (msg?.type === "scroll_latest") {
        if (scrollToLatest(msg.scroll_limit ?? null)) {
          startScrollLatestSettlement()
        }
      }
    }
    model.on("msg:custom", handler)
    return () => model.off("msg:custom", handler)
  }, [])

  React.useEffect(() => {
    if (!view_latest) {
      initialLatestDoneRef.current = true
      return
    }
    if (initialLatestDoneRef.current) {
      return
    }
    const settleInitialLatest = () => {
      initialLatestDoneRef.current = true
      syncLatestVisibleChild()
    }
    const frameId = requestAnimationFrame(() => {
      startScrollLatestSettlement(settleInitialLatest)
    })
    return () => cancelAnimationFrame(frameId)
  }, [view_latest])

  React.useEffect(() => {
    const handler = () => {
      layoutUpdatedRef.current = true
      updateScrollbarWidth()
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), flexDirection)
      })
      if (view_latest && !initialLatestDoneRef.current) {
        startScrollLatestSettlement(() => {
          initialLatestDoneRef.current = true
          syncLatestVisibleChild()
        })
      } else if (pendingScrollLatestRef.current) {
        scrollToLatest()
      }
    }
    model.on("lifecycle:update_layout", handler)
    return () => model.off("lifecycle:update_layout", handler)
  }, [])

  React.useEffect(() => {
    const root = boxRef.current
    if (!root) {
      return
    }
    const observer = new IntersectionObserver((entries) => {
      if (pendingScrollLatestRef.current) {
        return
      }
      let changed = false
      const next = new Set(visibleSetRef.current)
      for (const entry of entries) {
        const id = entry.target.getAttribute("data-feed-child-id")
        if (!id) {
          continue
        }
        if (entry.isIntersecting) {
          if (!next.has(id)) {
            next.add(id)
            changed = true
          }
        } else if (next.has(id)) {
          next.delete(id)
          changed = true
        }
      }
      if (!changed) {
        return
      }
      visibleSetRef.current = next
      if (!initialLatestDoneRef.current) {
        return
      }
      const ordered = model.objects.map((m) => m.id).filter((id) => next.has(id))
      setVisibleChildren(ordered)
    }, {root, threshold: 0.01})
    observerRef.current = observer

    return () => {
      stopScrollLatestSettlement()
      for (const node of observedNodesRef.current.values()) {
        observer.unobserve(node)
      }
      observedNodesRef.current.clear()
      observer.disconnect()
      observerRef.current = null
    }
  }, [])

  React.useEffect(() => {
    const observer = observerRef.current
    if (!observer) {
      return
    }

    const currentNodes = wrappersRef.current
    let changedVisible = false
    const nextVisible = new Set(visibleSetRef.current)

    // Unobserve nodes that are no longer active in the current window.
    for (const [id, node] of observedNodesRef.current) {
      const currentNode = currentNodes.get(id)
      if (!currentNode || currentNode !== node) {
        observer.unobserve(node)
        observedNodesRef.current.delete(id)
        if (nextVisible.delete(id)) {
          changedVisible = true
        }
      }
    }

    // Observe any newly mounted nodes.
    for (const [id, node] of currentNodes) {
      if (observedNodesRef.current.get(id) !== node) {
        observer.observe(node)
        observedNodesRef.current.set(id, node)
      }
    }
  }, [objects])

  React.useLayoutEffect(() => {
    const el = boxRef.current
    if (!el) {
      return
    }
    updateScrollbarWidth(el)
    updateScrollButton(el)
    if (pendingScrollLatestRef.current) {
      startScrollLatestSettlement(scrollSettledCallbackRef.current)
      return
    }
    const anchor = topAnchorRef.current
    if (!anchor) {
      return
    }
    const node = wrappersRef.current.get(anchor.id)
    if (!node) {
      return
    }
    const top = node.offsetTop - el.offsetTop
    const desired = Math.round(top - anchor.viewportOffset)
    if (Math.abs(el.scrollTop - desired) <= 1) {
      return
    }
    syncingScrollRef.current = true
    el.scrollTo({top: desired, behavior: "instant"})
    setScrollPosition(Math.round(el.scrollTop))
    syncingScrollRef.current = false
    updateScrollButton(el)
  }, [objects])

  const boxSx = React.useMemo(
    () => [
      FEED_BASE_SX,
      {flexDirection, width: scrollbarWidth ? `calc(100% - ${scrollbarWidth}px)` : "100%"},
      {"& > div": {flex: "0 0 auto", maxHeight: "unset"}},
      sx || {},
    ],
    [flexDirection, scrollbarWidth, sx]
  )

  return (
    <Box ref={setBoxRef} sx={boxSx}>
      {objects.map((object, index) => {
        const childModel = model.objects[index]
        const childId = childModel?.id ?? `${index}`
        apply_flex(view.get_child_view(childModel), flexDirection)
        return (
          <div
            key={childId}
            data-feed-child-id={childId}
            ref={(node) => {
              if (node) {
                wrappersRef.current.set(childId, node)
              } else {
                wrappersRef.current.delete(childId)
              }
            }}
          >
            {object}
          </div>
        )
      })}
      {scroll_button_threshold > 0 && (
        <div
          role="button"
          tabIndex={0}
          aria-label="Scroll to latest"
          className={`scroll-button${showScrollButton ? " visible" : ""}`}
          onClick={() => {
            armScrollLatestAfterRender()
            scrollToLatest()
            model.send_event("click", {})
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault()
              armScrollLatestAfterRender()
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
