import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Paper
from panel_material_ui.wrappers import Badge
from panel_material_ui.widgets import IconButton
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def _page_width(page):
    return page.evaluate("() => document.body.clientWidth")


def _width(locator):
    box = locator.bounding_box()
    return box["width"] if box else 0


def test_badge_basic(page):
    widget = Badge(IconButton(icon="mail"), content=4, color="primary")
    serve_component(page, widget)

    expect(page.locator('.MuiBadge-root')).to_have_count(1)
    expect(page.locator('.MuiBadge-badge')).to_contain_text('4')


def test_badge_color(page):
    widget = Badge(IconButton(icon="mail"), content=4, color="secondary")
    serve_component(page, widget)

    badge = page.locator('.MuiBadge-colorSecondary')
    expect(badge).to_have_count(1)


def test_badge_dot_variant(page):
    widget = Badge(IconButton(icon="mail"), variant="dot", color="primary")
    serve_component(page, widget)

    expect(page.locator('.MuiBadge-dot')).to_have_count(1)


def test_badge_max(page):
    widget = Badge(IconButton(icon="mail"), content=100, max=99)
    serve_component(page, widget)

    expect(page.locator('.MuiBadge-badge')).to_contain_text('99+')


def test_badge_show_zero(page):
    widget = Badge(IconButton(icon="mail"), content=0, show_zero=True)
    serve_component(page, widget)

    expect(page.locator('.MuiBadge-badge')).to_contain_text('0')


def test_badge_zero_hidden_by_default(page):
    widget = Badge(IconButton(icon="mail"), content=0)
    serve_component(page, widget)

    badge = page.locator('.MuiBadge-invisible')
    expect(badge).to_have_count(1)


def test_badge_overlap_circular(page):
    widget = Badge(IconButton(icon="mail"), content=4, overlap="circular")
    serve_component(page, widget)

    expect(page.locator('.MuiBadge-overlapCircular')).to_have_count(1)


def test_badge_dynamic_update(page):
    widget = Badge(IconButton(icon="mail"), content=1)
    serve_component(page, widget)

    expect(page.locator('.MuiBadge-badge')).to_contain_text('1')
    widget.content = 5
    expect(page.locator('.MuiBadge-badge')).to_contain_text('5')


def test_badge_empty(page):
    widget = Badge(content=4)
    serve_component(page, widget)

    expect(page.locator('.MuiBadge-root')).to_have_count(1)


def test_badge_fills_responsive_child(page):
    widget = Badge(
        Paper(sizing_mode="stretch_width", height=60),
        content=3, color="primary", sizing_mode="stretch_width",
    )
    serve_component(page, widget)

    paper = page.locator('.MuiPaper-root')
    expect(paper).to_have_count(1)
    wait_until(lambda: _width(paper) > _page_width(page) * 0.8, page)


def test_badge_hugs_fixed_child(page):
    widget = Badge(IconButton(icon="mail"), content=3, color="primary")
    serve_component(page, widget)

    badge = page.locator('.MuiBadge-root')
    expect(badge).to_have_count(1)
    wait_until(lambda: 0 < _width(badge) < _page_width(page) * 0.5, page)
