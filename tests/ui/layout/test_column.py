import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Column
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_column_scroll_features_render(page):
    col = Column(
        *list(range(60)),
        height=240,
        scroll=True,
        auto_scroll_limit=100,
        scroll_button_threshold=20,
        scroll_position=10,
        view_latest=True,
        css_classes=["test-col-render"],
    )
    serve_component(page, col)

    col_el = page.locator(".test-col-render").first
    expect(col_el).to_be_visible()
    expect(col_el.locator(".scroll-button")).to_have_count(1)
    assert col.auto_scroll_limit == 100
    assert col.scroll_button_threshold == 20
    assert col.scroll_position >= 0
    assert col.view_latest is True

def test_column_scroll_button_click_event(page):
    col = Column(
        *list(range(60)),
        height=240,
        scroll=True,
        scroll_button_threshold=20,
        css_classes=["test-col-click"],
    )
    events = []
    col.param.watch(events.append, "scroll_button_click", onlychanged=False)
    serve_component(page, col)

    col_el = page.locator(".test-col-click").first
    button = col_el.locator(".scroll-button")

    expect(button).to_have_count(1)
    button.click(force=True)
    wait_until(lambda: len(events) == 1, page)
