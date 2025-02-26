import time

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets.menus import Breadcrumbs, List, SpeedDial
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
        wait_until(lambda: widget.value == i, page)

def test_list(page):
    widget = List(name='List test', items=['Item 1', 'Item 2', 'Item 3'])
    serve_component(page, widget)

    expect(page.locator(".list")).to_have_count(1)
    expect(page.locator(".MuiList-root")).to_have_count(1)

    expect(page.locator(".MuiListItemText-root")).to_have_count(3)
    expect(page.locator(".MuiListItemText-root").nth(0)).to_have_text("Item 1")
    expect(page.locator(".MuiListItemText-root").nth(1)).to_have_text("Item 2")
    expect(page.locator(".MuiListItemText-root").nth(2)).to_have_text("Item 3")

    for i in range(3):
        page.locator(".MuiListItemButton-root").nth(i).click()
        wait_until(lambda: widget.value == i, page)

def test_speed_dial(page):
    widget = SpeedDial(name='SpeedDial test', items=[
        {'label': 'Item 1', 'icon': 'home'},
        {'label': 'Item 2', 'icon': 'dashboard'},
        {'label': 'Item 3', 'icon': 'profile'}
    ])
    serve_component(page, widget)

    expect(page.locator(".speed-dial")).to_have_count(1)
    expect(page.locator(".MuiSpeedDial-root")).to_have_count(1)
    expect(page.locator(".MuiSpeedDial-fab")).to_have_count(1)

    for _ in range(3):
        try:
            page.locator(".MuiSpeedDial-fab").hover(force=True)
        except Exception as e:
            time.sleep(0.1)
        else:
            break
    expect(page.locator(".MuiSpeedDial-actions")).to_be_visible()
    expect(page.locator(".MuiSpeedDial-actions button")).to_have_count(3)

    page.locator(".MuiSpeedDial-actions button").nth(0).hover()
    expect(page.locator("#SpeedDialtest-action-0")).to_be_visible()
    expect(page.locator("#SpeedDialtest-action-0")).to_have_text("Item 1")
    page.locator(".MuiSpeedDial-actions button").nth(1).hover()
    expect(page.locator("#SpeedDialtest-action-1")).to_be_visible()
    expect(page.locator("#SpeedDialtest-action-1")).to_have_text("Item 2")
    page.locator(".MuiSpeedDial-actions button").nth(2).hover()
    expect(page.locator("#SpeedDialtest-action-2")).to_be_visible()
    expect(page.locator("#SpeedDialtest-action-2")).to_have_text("Item 3")

    for i in range(3):
        page.locator(".MuiSpeedDial-actions button").nth(i).click()
        wait_until(lambda: widget.value == i, page)
