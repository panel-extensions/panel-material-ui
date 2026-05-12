import Box from "@mui/material/Box"
import {
  apply_flex, child_at_latest, scroll_to_child, scroll_to_latest,
  update_scroll_button, use_latest_scroll_settlement
} from "./utils"

const BOX_BASE_SX = {
  height: "100%",
  width: "100%",
  display: "flex",
  position: "relative",
}

export function render({model, view}) {
  const flexDirection = model.esm_constants.direction
  const isColumn = flexDirection === "column"

  const [sx] = model.useState("sx")
  let auto_scroll_limit = 0
  let scroll_button_threshold = 0
  let scroll_index = null
  let scroll_position = 0
  let view_latest = false
  let setScrollPosition = undefined
  if (isColumn) {
    const [auto_scroll_limit_state] = model.useState("auto_scroll_limit")
    const [scroll_button_threshold_state] = model.useState("scroll_button_threshold")
    const [scroll_index_state] = model.useState("scroll_index")
    const [scroll_position_state, setScrollPosition_state] = model.useState("scroll_position")
    const [view_latest_state] = model.useState("view_latest")
    auto_scroll_limit = auto_scroll_limit_state === undefined ? 0 : auto_scroll_limit_state
    scroll_button_threshold = scroll_button_threshold_state === undefined ? 0 : scroll_button_threshold_state
    scroll_index = scroll_index_state === undefined ? null : scroll_index_state
    scroll_position = scroll_position_state === undefined ? 0 : scroll_position_state
    view_latest = view_latest_state === undefined ? false : view_latest_state
    setScrollPosition = setScrollPosition_state
  }
  const objects = model.get_child("objects")
  const boxRef = React.useRef(null)
  const syncingScrollRef = React.useRef(false)
  const pendingScrollLatestRef = React.useRef(false)
  const layoutUpdatedRef = React.useRef(false)
  const prevObjectsLengthRef = React.useRef(objects.length)
  const [showScrollButton, setShowScrollButton] = React.useState(false)
  let scrollToLatest = () => false
  let startScrollLatestSettlement = () => {}
  let stopScrollLatestSettlement = () => {}

  const managedScroll = isColumn && (
    Boolean(view_latest) ||
    auto_scroll_limit > 0 ||
    scroll_button_threshold > 0 ||
    scroll_position > 0 ||
    scroll_index !== null
  )

  if (isColumn) {

    const updateScrollButton = React.useCallback((el) => {
      if (!isColumn || !managedScroll || scroll_button_threshold <= 0) {
        setShowScrollButton(false)
        return
      }
      update_scroll_button(el, scroll_button_threshold, setShowScrollButton)
    }, [managedScroll, scroll_button_threshold])

    const scrollToIndex = React.useCallback((index) => {
      const el = boxRef.current
      if (!el || index === null || index < 0) {
        return
      }
      const child = el.children.item(index)
      if (!child) {
        return
      }
      scroll_to_child(el, child, setScrollPosition)
    }, [setScrollPosition])

    scrollToLatest = React.useCallback((scrollLimit = null) => {
      return scroll_to_latest(boxRef.current, syncingScrollRef, setScrollPosition, updateScrollButton, scrollLimit)
    }, [setScrollPosition, updateScrollButton])

    const latestChildAtBottom = React.useCallback((el) => {
      return child_at_latest(el, el.children.item(objects.length - 1))
    }, [objects.length])

    const settlement = use_latest_scroll_settlement({
      boxRef,
      pendingScrollLatestRef,
      scrollToLatest,
      latestChildAtBottom,
      layoutUpdatedRef,
    })
    startScrollLatestSettlement = settlement.startScrollLatestSettlement
    stopScrollLatestSettlement = settlement.stopScrollLatestSettlement

    React.useEffect(() => {
      const el = boxRef.current
      if (!managedScroll || !el) {
        return
      }
      const onScroll = () => {
        if (syncingScrollRef.current) {
          return
        }
        setScrollPosition(Math.round(el.scrollTop))
        updateScrollButton(el)
      }
      el.addEventListener("scroll", onScroll)
      updateScrollButton(el)
      return () => {
        el.removeEventListener("scroll", onScroll)
      }
    }, [managedScroll, setScrollPosition, updateScrollButton])

    React.useEffect(() => {
      const el = boxRef.current
      if (!managedScroll || !el || syncingScrollRef.current) {
        return
      }
      if (Math.abs(el.scrollTop - scroll_position) <= 1) {
        return
      }
      syncingScrollRef.current = true
      el.scrollTo({top: scroll_position, behavior: "instant"})
      syncingScrollRef.current = false
      updateScrollButton(el)
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
        startScrollLatestSettlement(null, true)
      } else if (objects.length > prevObjectsLengthRef.current && auto_scroll_limit > 0) {
        scrollToLatest(auto_scroll_limit)
      }
      prevObjectsLengthRef.current = objects.length
    }, [managedScroll, objects.length, auto_scroll_limit, scrollToLatest, startScrollLatestSettlement, view_latest])
  }

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
      layoutUpdatedRef.current = true
      objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), flexDirection)
      })
      if (pendingScrollLatestRef.current) {
        scrollToLatest()
      }
    }
    model.on("lifecycle:update_layout", handler)
    return () => {
      stopScrollLatestSettlement?.()
      model.off("lifecycle:update_layout", handler)
    }
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
            startScrollLatestSettlement()
            model.send_event("click", {})
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault()
              startScrollLatestSettlement()
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
