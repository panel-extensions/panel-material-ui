import pytest

pytest.importorskip("playwright")

from panel.layout.spacer import Spacer
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Feed
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

    wait_until(lambda: feed_el.evaluate("(el) => el.scrollTop") > 0, page)
    wait_until(lambda: int(feed_el.locator("pre").last.inner_text() or 0) > 0.9 * ITEMS, page)


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
    feed.scroll_to_latest(scroll_limit=1000)

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
    wait_until(lambda: feed_el.evaluate("(el) => el.scrollTop") > 0, page)
    wait_until(lambda: int(feed_el.locator("pre").last.inner_text() or 0) > 50, page)


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
