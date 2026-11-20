import pytest

pytest.importorskip("playwright")

from panel.io.state import state
from panel.layout.spacer import Spacer
from panel.tests.util import serve_component, wait_until
from panel_material_ui.chat import ChatFeed, ChatMessage
from panel_material_ui.layout import Column, Feed
from panel_material_ui.widgets import Button
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

ITEMS = 100


def _feed(page, css_class: str):
    return page.locator(f".{css_class}").first


def _rendered_count(feed_el):
    return feed_el.locator("pre").count()


def test_feed_load_entries(page):
    feed = Feed(*list(range(ITEMS)), height=250, css_classes=["test-feed-load"])
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-load")
    expect(feed_el).to_be_visible()
    assert feed_el.bounding_box()["height"] == 250

    children_count = _rendered_count(feed_el)
    assert 10 <= children_count <= 40

    feed_el.evaluate("(el) => el.scrollTo({top: 100})")
    wait_until(lambda: _rendered_count(feed_el) >= 10, page)
    assert 10 <= _rendered_count(feed_el) <= 40

    feed_el.evaluate("(el) => el.scrollTo({top: 0})")
    wait_until(lambda: _rendered_count(feed_el) >= 10, page)


def test_feed_view_latest(page):
    feed = Feed(*list(range(ITEMS)), height=250, view_latest=True, css_classes=["test-feed-latest"])
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-latest")
    expect(feed_el).to_be_attached()
    assert feed_el.bounding_box()["height"] == 250

    expect(page.locator(".bk-panel-models-markup-HTML").last).to_have_text("99")

    def assert_at_bottom():
        assert feed_el.evaluate("(el) => el.scrollHeight - el.scrollTop - el.clientHeight") <= 1

    wait_until(assert_at_bottom, page)


def test_feed_scroll_to_latest(page):
    feed = Feed(*list(range(ITEMS)), height=250, css_classes=["test-feed-scroll-latest"])
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-scroll-latest")
    expect(feed_el).to_be_attached()
    wait_until(lambda: feed_el.evaluate("(el) => el.scrollTop") == 0, page)

    feed.scroll_to_latest()
    wait_until(lambda: int(feed_el.locator("pre").last.inner_text() or 0) > 0.9 * ITEMS, page)


def test_feed_scroll_to_latest_disabled_when_limit_zero(page):
    feed = Feed(*list(range(ITEMS)), height=250, css_classes=["test-feed-limit-zero"])
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-limit-zero")
    expect(feed_el).to_be_attached()
    page.wait_for_timeout(200)
    initial_scroll = feed_el.evaluate("(el) => el.scrollTop")

    feed.scroll_to_latest(scroll_limit=0)
    page.wait_for_timeout(200)

    final_scroll = feed_el.evaluate("(el) => el.scrollTop")
    assert initial_scroll == final_scroll


def test_feed_scroll_to_latest_always_when_limit_null(page):
    feed = Feed(*list(range(ITEMS)), height=250, css_classes=["test-feed-limit-null"])
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-limit-null")
    wait_until(lambda: int(feed_el.locator("pre").last.inner_text() or 0) < 0.9 * ITEMS, page)
    feed.scroll_to_latest(scroll_limit=None)
    wait_until(lambda: int(feed_el.locator("pre").last.inner_text() or 0) > 0.9 * ITEMS, page)


def test_feed_scroll_to_latest_within_limit(page):
    feed = Feed(
        Spacer(styles=dict(background="red"), width=200, height=200),
        Spacer(styles=dict(background="green"), width=200, height=200),
        Spacer(styles=dict(background="blue"), width=200, height=200),
        auto_scroll_limit=0,
        height=420,
        css_classes=["test-feed-within-limit"],
    )
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-within-limit")
    expect(feed_el).to_have_js_property("scrollTop", 0)

    feed.scroll_to_latest(scroll_limit=100)
    page.wait_for_timeout(200)

    feed.append(Spacer(styles=dict(background="yellow"), width=200, height=200))
    page.wait_for_timeout(200)
    expect(feed_el).to_have_js_property("scrollTop", 0)

    feed_el.evaluate("(el) => el.scrollTo({top: 200})")
    expect(feed_el).to_have_js_property("scrollTop", 200)

    feed.append(Spacer(styles=dict(background="yellow"), width=200, height=200))
    page.wait_for_timeout(200)
    feed.scroll_to_latest()

    def assert_at_bottom():
        assert feed_el.evaluate("(el) => el.scrollHeight - el.scrollTop - el.clientHeight") == 0

    wait_until(assert_at_bottom, page)


def test_feed_view_scroll_button(page):
    feed = Feed(
        *list(range(ITEMS)),
        height=250,
        scroll_button_threshold=50,
        css_classes=["test-feed-scroll-button"],
    )
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-scroll-button")
    scroll_arrow = feed_el.locator(".scroll-button")

    expect(scroll_arrow).to_have_count(1)
    expect(scroll_arrow).to_have_class("scroll-button visible")
    expect(scroll_arrow).to_be_visible()

    scroll_arrow.click()
    wait_until(lambda: int(feed_el.locator("pre").last.inner_text() or 0) > 0.9 * ITEMS, page)

    def assert_at_bottom():
        assert feed_el.evaluate("(el) => el.scrollHeight - el.scrollTop - el.clientHeight") <= 1

    wait_until(assert_at_bottom, page)


def test_feed_dynamic_objects(page):
    feed = Feed(height=250, load_buffer=10, css_classes=["test-feed-dynamic"])
    serve_component(page, feed)

    feed.objects = list(range(ITEMS))
    feed_el = _feed(page, "test-feed-dynamic")

    wait_until(lambda: feed_el.locator("pre").first.inner_text() == "0", page)
    wait_until(lambda: feed_el.locator("pre").count() >= 10, page)


def test_feed_reset_visible_range(page):
    feed = Feed(
        *list(range(ITEMS)),
        load_buffer=20,
        height=50,
        view_latest=True,
        css_classes=["test-feed-reset-range"],
    )
    serve_component(page, feed)

    feed_el = _feed(page, "test-feed-reset-range")
    pre = feed_el.locator("pre")
    expect(pre.last).to_be_attached()
    page.wait_for_timeout(500)

    wait_until(lambda: pre.last.text_content() in ("98", "99"), page)

    feed.objects = feed.objects[:20]
    page.wait_for_timeout(500)
    expect(pre.last).to_have_text("19")


# Counts, every few milliseconds, the children in view that were rendered and are
# blank again while they stay in the feed, as a child that is mounted anew is until
# its button has rendered, and the times the feed's log went back to the top after
# it had scrolled down.
_WATCH_BLANKS = """
(feed) => {
  window.blanks = 0
  window.checked = 0
  window.top_jumps = []
  let scrolled = 0
  const seen = new Set()
  const find = (root, selector, found = []) => {
    found.push(...root.querySelectorAll(selector))
    for (const el of root.querySelectorAll("*")) {
      if (el.shadowRoot) {
        find(el.shadowRoot, selector, found)
      }
    }
    return found
  }
  window.blank_watch = setInterval(() => {
    const [log] = find(feed.shadowRoot ?? feed, ".chat-feed-log")
    if (log.scrollTop > log.clientHeight) {
      scrolled = Math.max(scrolled, log.scrollTop)
    } else if (scrolled && log.scrollTop < 200) {
      window.top_jumps.push([Math.round(scrolled), Math.round(log.scrollTop)])
      scrolled = 0
    }
    const view = feed.getBoundingClientRect()
    for (const wrapper of find(feed.shadowRoot ?? feed, "[data-feed-child-id]")) {
      const box = wrapper.getBoundingClientRect()
      if (box.bottom <= view.top || box.top >= view.bottom) {
        continue
      }
      const id = wrapper.getAttribute("data-feed-child-id")
      const [button] = find(wrapper, "button")
      const rendered = button != null && button.getBoundingClientRect().height > 0
      if (rendered) {
        seen.add(id)
        window.checked++
      } else if (seen.has(id)) {
        window.blanks++
      }
    }
  }, 10)
}
"""


def test_feed_window_shift_keeps_children_rendered(page):
    feeds = []

    def app():
        feed = ChatFeed(height=700, css_classes=["test-feed-shift"])
        feeds.append(feed)
        rounds = iter(range(60))

        def add():
            i = next(rounds, None)
            if i is None:
                callback.stop()
                return
            feed.objects = [
                *feed.objects,
                ChatMessage(f"question {i}", user="You"),
                ChatMessage(Button(label=f"item {i}"), user="Bot"),
                ChatMessage(f"answer {i}", user="Bot"),
            ]

        # Every round lands while the frontend is still settling the last one.
        callback = state.add_periodic_callback(add, period=200)
        return Column(feed, height=800, width=600)

    serve_component(page, app)
    feed_el = _feed(page, "test-feed-shift")
    expect(feed_el.get_by_role("button", name="item 0")).to_be_attached(timeout=20000)
    feed_el.evaluate(_WATCH_BLANKS)
    wait_until(lambda: len(feeds[0].objects) == 3 * 60, page, timeout=240000)
    page.wait_for_timeout(1000)
    page.evaluate("clearInterval(window.blank_watch)")

    # Past twice the load_buffer of 50 the window drops children at the top.
    assert feed_el.get_by_role("button", name="item 0").count() == 0
    assert page.evaluate("window.checked") > 0
    assert page.evaluate("window.blanks") == 0
    assert page.evaluate("window.top_jumps") == []
    expect(feed_el.get_by_role("button", name="item 59")).to_be_visible(timeout=20000)

    log = feed_el.locator(".chat-feed-log")

    def assert_at_bottom():
        assert log.evaluate("(el) => el.scrollHeight - el.scrollTop - el.clientHeight") <= 1

    wait_until(assert_at_bottom, page)
