import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets.menus import Breadcrumbs
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_breadcrumbs(page):
    widget = Breadcrumbs(name='Breadcrumbs test', items=['Home', 'Dashboard', 'Profile'])
    serve_component(page, widget)

    expect(page.locator(".breadcrumbs")).to_have_count(1)
    expect(page.locator(".MuiBreadcrumbs-ol")).to_have_count(1)
    expect(page.locator(".MuiBreadcrumbs-li")).to_have_count(3)
    expect(page.locator(".MuiBreadcrumbs-li").nth(0)).to_have_text("Home")
    expect(page.locator(".MuiBreadcrumbs-li").nth(1)).to_have_text("Dashboard")
    expect(page.locator(".MuiBreadcrumbs-li").nth(2)).to_have_text("Profile")

    for i in range(3):
        page.locator(".MuiBreadcrumbs-li").nth(i).click()
        wait_until(lambda: widget.value == widget.items[i], page)

def test_breadcrumbs_basic(page):
    items = ['Home', 'Library', 'Data']
    widget = Breadcrumbs(items=items)
    serve_component(page, widget)

    breadcrumbs = page.locator('.MuiBreadcrumbs-ol .MuiBreadcrumbs-li')
    expect(breadcrumbs).to_have_count(3)
    expect(breadcrumbs.nth(2)).to_have_text('Data')

def test_breadcrumbs_click(page):
    events = []
    def cb(event):
        events.append(event)

    items = ['Home', 'Library', 'Data']
    widget = Breadcrumbs(items=items, on_click=cb)
    serve_component(page, widget)

    breadcrumbs = page.locator('.MuiBreadcrumbs-ol .MuiBreadcrumbs-li').nth(1)
    breadcrumbs.click()
    wait_until(lambda: len(events) == 1, page)
    assert events[0] == 'Library'
