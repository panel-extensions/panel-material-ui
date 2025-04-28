import time

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets.menus import Breadcrumbs, List, MenuButton, Pagination, SpeedDial
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
        wait_until(lambda: widget.value == widget.items[i], page)

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

def test_list_basic(page):
    items = [
        {'label': 'Item 1'},
        {'label': 'Item 2'},
        {'label': 'Item 3'}
    ]
    widget = List(items=items)
    serve_component(page, widget)

    list_items = page.locator('.MuiListItemButton-root')
    expect(list_items).to_have_count(3)

def test_list_nested(page):
    items = [
        {
            'label': 'Item 1',
            'items': [
                {'label': 'Subitem 1'},
                {'label': 'Subitem 2'}
            ]
        }
    ]
    widget = List(items=items)
    serve_component(page, widget)

    # Click to expand
    page.locator('.MuiListItemButton-root').first.click()

    # Check subitems are visible
    subitems = page.locator('.MuiCollapse-root .MuiListItemButton-root')
    expect(subitems).to_have_count(2)

def test_list_selection(page):
    items = [
        {'label': 'Item 1'},
        {'label': 'Item 2'},
        {'label': 'Item 3'}
    ]
    widget = List(items=items)
    serve_component(page, widget)

    list_items = page.locator('.MuiListItemButton-root')
    list_items.nth(1).click()

    assert widget.active == 1
    assert widget.value == items[1]

def test_menubutton_basic(page):
    items = ['Option 1', 'Option 2', 'Option 3']
    widget = MenuButton(items=items, label='Menu')
    serve_component(page, widget)

    # Check button exists
    button = page.locator('.MuiButtonBase-root')
    expect(button).to_have_text('Menu')

    # Click to open menu
    button.click()

    # Check menu items
    menu_items = page.locator('.MuiMenuItem-root')
    expect(menu_items).to_have_count(3)

def test_menubutton_selection(page):
    items = ['Option 1', 'Option 2', 'Option 3']
    widget = MenuButton(items=items, label='Menu')
    serve_component(page, widget)

    # Open menu and select item
    page.locator('.MuiButton-root').click()
    page.locator('.MuiMenuItem-root').nth(1).click()

    assert widget.active == 1
    assert widget.value == 'Option 2'

def test_pagination_basic(page):
    widget = Pagination(count=5)
    serve_component(page, widget)

    pagination = page.locator('.MuiPagination-root')
    expect(pagination).to_have_count(1)

    # Check number of page buttons (including prev/next)
    page_buttons = page.locator('.MuiPaginationItem-root')
    expect(page_buttons).to_have_count(7)  # 5 pages + prev/next buttons

def test_pagination_navigation(page):
    widget = Pagination(count=5)
    serve_component(page, widget)

    # Click second page
    page.locator('.MuiPaginationItem-root').nth(2).click()
    wait_until(lambda: widget.value == 1, page)

def test_speeddial_basic(page):
    items = [
        {'label': 'Copy', 'icon': 'content_copy'},
        {'label': 'Save', 'icon': 'save'},
        {'label': 'Print', 'icon': 'print'}
    ]
    widget = SpeedDial(items=items)
    serve_component(page, widget)

    # Check SpeedDial exists
    speeddial = page.locator('.MuiSpeedDial-root')
    expect(speeddial).to_have_count(1)

    # Click to open
    page.locator('.MuiSpeedDial-fab').click()

    # Check actions are visible
    actions = page.locator('.MuiSpeedDialAction-fab')
    expect(actions).to_have_count(3)

def test_speeddial_selection(page):
    events = []
    def cb(event):
        events.append(event)

    items = [
        {'label': 'Copy', 'icon': 'content_copy'},
        {'label': 'Save', 'icon': 'save'},
        {'label': 'Print', 'icon': 'print'}
    ]
    widget = SpeedDial(items=items, on_click=cb)
    serve_component(page, widget)

    # Open and click an action
    page.locator('.MuiSpeedDial-fab').click()
    page.locator('.MuiSpeedDialAction-fab').nth(1).click()

    wait_until(lambda: len(events) == 1, page)
    assert widget.value == items[1]
