import pytest
import re

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import MenuToggle
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_menutoggle_basic(page):
    items = [
        {'label': 'Favorite', 'icon': 'favorite_border', 'active_icon': 'favorite'},
        {'label': 'Bookmark', 'icon': 'bookmark_border', 'active_icon': 'bookmark'},
        {'label': 'Star', 'icon': 'star_border', 'active_icon': 'star'}
    ]
    widget = MenuToggle(items=items, label='Actions')
    serve_component(page, widget)

    # Check button exists
    button = page.locator('.MuiButton-root')
    expect(button).to_have_text('Actions')

    # Initial state should be closed
    assert widget.active is None


def test_menutoggle_open_close(page):
    items = [{'label': 'Item 1'}, {'label': 'Item 2'}]
    widget = MenuToggle(items=items, label='Menu')
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()

    expect(page.locator('.MuiMenu-root')).to_be_visible()

    # Close menu
    page.locator('body').click()
    expect(page.locator('.MuiMenu-root')).not_to_be_visible()


def test_menutoggle_item_toggle(page):
    items = [
        {'label': 'Favorite', 'icon': 'favorite_border', 'active_icon': 'favorite', 'toggled': False},
        {'label': 'Bookmark', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'toggled': True},
        {'label': 'Star', 'icon': 'star_border', 'active_icon': 'star', 'toggled': False}
    ]
    widget = MenuToggle(items=items, label='Actions')
    serve_component(page, widget)

    # Initial toggled should reflect the toggled states
    assert widget.toggled == [1]  # Bookmark is toggled

    # Open menu
    page.locator('.MuiButton-root').click()

    # Toggle first item (Favorite)
    page.locator('.MuiMenuItem-root').first.click()
    wait_until(lambda: 0 in widget.toggled, page)
    assert widget.toggled == [1, 0]  # Both Bookmark and Favorite

    # Menu should stay open by default (persistent=True)
    expect(page.locator('.MuiMenu-root')).to_be_visible()

    # Toggle second item (Bookmark) to turn it off
    page.locator('.MuiMenuItem-root').nth(1).click()
    wait_until(lambda: 1 not in widget.toggled, page)
    assert widget.toggled == [0]  # Only Favorite


def test_menutoggle_icon_switching(page):
    items = [
        {'label': 'Favorite', 'icon': 'favorite_border', 'active_icon': 'favorite'},
        {'label': 'Bookmark', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'toggled': True}
    ]
    widget = MenuToggle(items=items, label='Actions')
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()

    # Check initial icons
    icons = page.locator('.MuiMenuItem-root .material-icons').all()
    expect(icons[0]).to_have_text('favorite_border')  # Not toggled
    expect(icons[1]).to_have_text('bookmark')  # Toggled

    # Toggle first item
    page.locator('.MuiMenuItem-root').first.click()
    wait_until(lambda: 0 in widget.toggled, page)

    # Icon should change
    icons = page.locator('.MuiMenuItem-root .material-icons').all()
    expect(icons[0]).to_have_text('favorite')  # Now toggled


def test_menutoggle_non_persistent_mode(page):
    items = [
        {'label': 'Item 1', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'},
        {'label': 'Item 2', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'}
    ]
    widget = MenuToggle(items=items, label='Options', persistent=False)
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()

    # Toggle item
    page.locator('.MuiMenuItem-root').first.click()

    # Menu should close in non-persistent mode
    expect(page.locator('.MuiMenu-root')).not_to_be_visible()

    # But item should still be toggled
    assert 0 in widget.toggled


def test_menutoggle_selected_state(page):
    items = [
        {'label': 'Item 1', 'toggled': False},
        {'label': 'Item 2', 'toggled': True}
    ]
    widget = MenuToggle(items=items, label='Menu')
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()

    # Second item should have selected class
    expect(page.locator('.MuiMenuItem-root').nth(1)).to_have_class(re.compile('Mui-selected'))
    expect(page.locator('.MuiMenuItem-root').first).not_to_have_class(re.compile('Mui-selected'))


def test_menutoggle_with_colors(page):
    items = [
        {'label': 'Red', 'icon': 'circle', 'color': 'red', 'active_color': 'darkred'},
        {'label': 'Blue', 'icon': 'circle', 'color': 'blue', 'active_color': 'darkblue', 'toggled': True}
    ]
    widget = MenuToggle(items=items, label='Colors')
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()

    # Check colors are applied
    expect(page.locator('.MuiMenuItem-root').first).to_have_css('color', 'rgb(255, 0, 0)')
    expect(page.locator('.MuiMenuItem-root').nth(1)).to_have_css('color', 'rgb(0, 0, 139)')  # darkblue


def test_menutoggle_menu_button_icon(page):
    widget = MenuToggle(
        label='Menu',
        icon='menu',
        toggle_icon='close',
        items=[{'label': 'Item 1'}]
    )
    serve_component(page, widget)

    # Check initial icon
    expect(page.locator('.MuiButton-root .material-icons').first).to_have_text('menu')

    # Open menu and check icon changes
    page.locator('.MuiButton-root').click()
    expect(page.locator('.MuiButton-root .material-icons').first).to_have_text('close')


def test_menutoggle_with_dividers(page):
    widget = MenuToggle(
        label='Menu',
        items=[
            {'label': 'Item 1', 'icon': 'star_border', 'active_icon': 'star'},
            {'label': '---'},  # Divider
            {'label': 'Item 2', 'icon': 'star_border', 'active_icon': 'star'}
        ]
    )
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()

    # Verify divider
    expect(page.locator('.MuiDivider-root')).to_have_count(1)
    expect(page.locator('.MuiMenuItem-root')).to_have_count(2)


def test_menutoggle_programmatic_toggle_items(page):
    items = [
        {'label': 'Item 1', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'},
        {'label': 'Item 2', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'}
    ]
    widget = MenuToggle(items=items, label='Menu')
    serve_component(page, widget)

    # Programmatically toggle items
    widget.toggled = [0, 1]

    # Open menu to verify
    page.locator('.MuiButton-root').click()
    expect(page.locator('.MuiMenu-root')).to_be_visible()

    # Both items should be selected
    expect(page.locator('.MuiMenuItem-root.Mui-selected')).to_have_count(2)


def test_menutoggle_click_callback(page):
    events = []
    def cb(event):
        events.append(event)

    items = [
        {'label': 'Item 1', 'icon': 'favorite_border', 'active_icon': 'favorite'},
        {'label': 'Item 2', 'icon': 'star_border', 'active_icon': 'star'}
    ]
    widget = MenuToggle(
        label='Menu',
        items=items,
        on_click=cb
    )
    serve_component(page, widget)

    # Open menu and toggle item
    page.locator('.MuiButton-root').click()
    page.locator('.MuiMenuItem-root').first.click()
    wait_until(lambda: len(events) == 1, page)

    # Event should have the item data
    assert events[0]['label'] == 'Item 1'


@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_menutoggle_button_colors(page, color):
    widget = MenuToggle(
        label='Menu',
        color=color,
        items=[{'label': 'Item 1'}]
    )
    serve_component(page, widget)

    css_class = f'MuiButton-color{color.capitalize()}'
    expect(page.locator(f'.{css_class}')).to_have_count(1)


def test_menutoggle_disabled_state(page):
    widget = MenuToggle(
        label='Menu',
        disabled=True,
        items=[{'label': 'Item 1'}]
    )
    serve_component(page, widget)

    # Verify disabled state
    expect(page.locator('.MuiButton-root.Mui-disabled')).to_have_count(1)


def test_menutoggle_multiple_toggles(page):
    items = [
        {'label': 'Option A', 'icon': 'radio_button_unchecked', 'active_icon': 'radio_button_checked'},
        {'label': 'Option B', 'icon': 'radio_button_unchecked', 'active_icon': 'radio_button_checked'},
        {'label': 'Option C', 'icon': 'radio_button_unchecked', 'active_icon': 'radio_button_checked'}
    ]
    widget = MenuToggle(items=items, label='Multi Select')
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()

    # Toggle multiple items
    page.locator('.MuiMenuItem-root').nth(0).click()
    page.locator('.MuiMenuItem-root').nth(2).click()

    wait_until(lambda: len(widget.toggled) == 2, page)
    assert 0 in widget.toggled
    assert 2 in widget.toggled
    assert 1 not in widget.toggled

    # Icons should reflect state
    icons = page.locator('.MuiMenuItem-root .material-icons').all()
    expect(icons[0]).to_have_text('radio_button_checked')
    expect(icons[1]).to_have_text('radio_button_unchecked')
    expect(icons[2]).to_have_text('radio_button_checked')
