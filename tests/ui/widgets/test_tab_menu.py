import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets.menus import TabMenu
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_tab_menu(page):
    widget = TabMenu(name='TabMenu test', items=['Home', 'Dashboard', 'Profile'])
    serve_component(page, widget)

    expect(page.locator(".MuiTabs-root")).to_have_count(1)
    expect(page.locator(".MuiTab-root")).to_have_count(3)
    expect(page.locator(".MuiTab-root").nth(0)).to_have_text("Home")
    expect(page.locator(".MuiTab-root").nth(1)).to_have_text("Dashboard")
    expect(page.locator(".MuiTab-root").nth(2)).to_have_text("Profile")

    for i in range(3):
        page.locator(".MuiTab-root").nth(i).click()
        wait_until(lambda: widget.value == widget.items[i], page)

def test_tab_menu_basic(page):
    items = ['Home', 'Library', 'Data']
    widget = TabMenu(items=items)
    serve_component(page, widget)

    tabs = page.locator('.MuiTab-root')
    expect(tabs).to_have_count(3)
    expect(tabs.nth(2)).to_have_text('Data')


def test_tab_menu_click(page):
    events = []
    def cb(event):
        events.append(event)

    items = ['Home', 'Library', 'Data']
    widget = TabMenu(items=items, on_click=cb)
    serve_component(page, widget)

    tabs = page.locator('.MuiTab-root').nth(1)
    tabs.click()
    wait_until(lambda: len(events) == 1, page)
    assert events[0] == 'Library'

def test_tab_menu_with_icons(page):
    widget = TabMenu(items=[
        {"label": "Home", "icon": "home"},
        {"label": "Settings", "icon": "settings"}
    ])
    serve_component(page, widget)

    # Verify icons
    icons = page.locator('.MuiTab-root .material-icons')
    expect(icons.nth(0)).to_have_text('home')
    expect(icons.nth(1)).to_have_text('settings')

def test_tab_menu_with_avatars(page):
    widget = TabMenu(items=[
        {"label": "Item 1", "avatar": "A"},
        {"label": "Item 2", "avatar": "B"}
    ])
    serve_component(page, widget)

    # Verify avatars
    avatars = page.locator('.MuiTab-root .MuiAvatar-root')
    expect(avatars.nth(0)).to_have_text('A')
    expect(avatars.nth(1)).to_have_text('B')

def test_tab_menu_selection(page):
    items = [
        {'label': 'Item 1'},
        {'label': 'Item 2'},
        {'label': 'Item 3'}
    ]
    widget = TabMenu(items=items)
    serve_component(page, widget)

    tabs = page.locator('.MuiTab-root')
    tabs.nth(1).click()

    assert widget.active == 1
    assert widget.value == items[1]

def test_tab_menu_active_setting(page):
    items = ['Home', 'Library', 'Data']
    widget = TabMenu(items=items, active=2)
    serve_component(page, widget)

    # Verify the third tab is selected
    expect(page.locator('.MuiTab-root').nth(2)).to_have_attribute("aria-selected", "true")
    assert widget.value == 'Data'

def test_tab_menu_color(page):
    widget = TabMenu(items=[{'label': 'Home'}, {'label': 'Settings'}], color='secondary', active=1)
    serve_component(page, widget)

    # Verify color - MUI applies color to indicator and selected tab for secondary
    selected_tab = page.locator('.MuiTab-root[aria-selected="true"]')
    assert selected_tab.count() == 1
    # Should have 'Mui-selected' class and 'colorSecondary' in classes for secondary
    # Check class for 'Mui-selected'
    assert "Mui-selected" in selected_tab.first.get_attribute("class")
    # The indicator color for "secondary" uses the theme, check style or class presence
    indicator = page.locator('.MuiTabs-indicator')
    expect(indicator).to_have_count(1)
    expect(indicator).to_have_css('background-color', 'rgb(156, 39, 176)')

def test_tab_menu_variant(page):
    widget = TabMenu(items=[{'label': 'Home'}, {'label': 'Settings'}], variant='scrollable')
    serve_component(page, widget)

    # For "scrollable", scroll buttons are shown if not all tabs fit - not always visible with 2 tabs
    # But the variant results in 'MuiTabs-scrollable' class
    expect(page.locator('.MuiTabs-root > .MuiTabs-scroller')).to_have_count(1)

def test_tab_menu_centered(page):
    widget = TabMenu(items=[{'label': 'Home'}, {'label': 'Settings'}], centered=True)
    serve_component(page, widget)

    tabs = page.locator('.MuiTabs-root .MuiTabs-scroller > .MuiTabs-list')
    expect(tabs).to_have_count(1)
    # Check that the centered class is present
    tabs_class = tabs.first.get_attribute("class")
    assert "MuiTabs-centered" in tabs_class

def test_tab_menu_with_href(page):
    widget = TabMenu(items=[
        {"label": "Link 1", "href": "https://example.com"},
        {"label": "Link 2", "href": "https://example.org", "target": "_blank"}
    ])
    serve_component(page, widget)

    # Verify href attributes
    expect(page.locator('.MuiTab-root').nth(0)).to_have_attribute('href', 'https://example.com')
    expect(page.locator('.MuiTab-root').nth(1)).to_have_attribute('href', 'https://example.org')
    expect(page.locator('.MuiTab-root').nth(1)).to_have_attribute('target', '_blank')

def test_tab_menu_update_item(page):
    """Test updating a tab menu item and verifying it renders in the frontend"""
    items = [
        {'label': 'Home'},
        {'label': 'Dashboard'},
        {'label': 'Profile'}
    ]
    widget = TabMenu(items=items)
    serve_component(page, widget)

    # Verify initial state
    tabs = page.locator('.MuiTab-root')
    expect(tabs.nth(1)).to_have_text('Dashboard')

    # Update the item
    item_to_update = items[1]
    widget.update_item(item_to_update, label='Settings')

    assert widget.items[1]['label'] == 'Settings'
    expect(tabs.nth(1)).to_have_text('Settings')
    expect(tabs.nth(0)).to_have_text('Home')  # Other items unchanged
    expect(tabs.nth(2)).to_have_text('Profile')

def test_tab_menu_update_item_with_icon(page):
    """Test updating a tab item to add an icon"""
    items = [
        {'label': 'Home'},
        {'label': 'Dashboard'}
    ]
    widget = TabMenu(items=items)
    serve_component(page, widget)

    # Update item to add icon
    item_to_update = items[0]
    widget.update_item(item_to_update, icon='home', avatar='H')
    assert 'icon' in widget.items[0] and widget.items[0]['icon'] == 'home'

    # Verify icon is rendered
    expect(page.locator('.MuiTab-root').nth(0).locator('.material-icons')).to_have_text('home')
    expect(page.locator('.MuiTab-root').nth(0).locator('.MuiAvatar-root')).to_have_text('H')
