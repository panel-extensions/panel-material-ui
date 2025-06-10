import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import MenuButton
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


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

def test_menu_button_basic_functionality(page):
    widget = MenuButton(
        label='Menu Button',
        items=[
            {'label': 'Item 1'},
            {'label': 'Item 2'},
            {'label': 'Item 3'}
        ]
    )
    serve_component(page, widget)

    expect(page.locator('.MuiButton-root')).to_have_count(1)
    expect(page.locator('.MuiButton-root')).to_have_text('Menu Button')

def test_menu_button_open_close(page):
    widget = MenuButton(
        label='Menu Button',
        items=[
            {'label': 'Item 1'},
            {'label': 'Item 2'}
        ]
    )
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()
    expect(page.locator('.MuiMenu-root')).to_be_visible()
    expect(page.locator('.MuiMenuItem-root')).to_have_count(2)

    # Close menu by clicking outside
    page.mouse.click(0, 0)
    expect(page.locator('.MuiMenu-root')).not_to_be_visible()

def test_menu_button_item_selection(page):
    widget = MenuButton(
        label='Menu Button',
        items=[
            {'label': 'Item 1'},
            {'label': 'Item 2'}
        ]
    )
    serve_component(page, widget)

    # Open menu and select item
    page.locator('.MuiButton-root').click()
    page.locator('.MuiMenuItem-root').first.click()

    # Verify menu is closed and value is updated
    expect(page.locator('.MuiMenu-root')).not_to_be_visible()
    wait_until(lambda: widget.value == {'label': 'Item 1'}, page)

def test_menu_button_with_icons(page):
    widget = MenuButton(
        label='Menu Button',
        icon='menu',
        items=[
            {'label': 'Item 1', 'icon': 'home'},
            {'label': 'Item 2', 'icon': 'settings'}
        ]
    )
    serve_component(page, widget)

    # Verify button icon
    expect(page.locator('.MuiButton-root .material-icons')).to_have_text('menu')

    # Open menu and verify item icons
    page.locator('.MuiButton-root').click()
    icons = page.locator('.MuiMenuItem-root .material-icons').all()
    expect(icons[0]).to_have_text('home')
    expect(icons[1]).to_have_text('settings')

@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_menu_button_colors(page, color):
    widget = MenuButton(
        label='Menu Button',
        color=color,
        items=[{'label': 'Item 1'}]
    )
    serve_component(page, widget)

    css_class = f'MuiButton-color{color.capitalize()}'
    expect(page.locator(f'.{css_class}')).to_have_count(1)

def test_menu_button_disabled_state(page):
    widget = MenuButton(
        label='Menu Button',
        disabled=True,
        items=[{'label': 'Item 1'}]
    )
    serve_component(page, widget)

    # Verify disabled state
    expect(page.locator('.MuiButton-root.Mui-disabled')).to_have_count(1)

def test_menu_button_click_callback(page):
    events = []
    def cb(event):
        events.append(event)

    widget = MenuButton(
        label='Menu Button',
        items=[{'label': 'Item 1'}],
        on_click=cb
    )
    serve_component(page, widget)

    # Open menu and click item
    page.locator('.MuiButton-root').click()
    page.locator('.MuiMenuItem-root').click()
    wait_until(lambda: len(events) == 1, page)

def test_menu_button_with_dividers(page):
    widget = MenuButton(
        label='Menu Button',
        items=[
            {'label': 'Item 1'},
            {'label': '---'},  # Divider
            {'label': 'Item 2'}
        ]
    )
    serve_component(page, widget)

    # Open menu and verify divider
    page.locator('.MuiButton-root').click()
    expect(page.locator('.MuiDivider-root')).to_have_count(1)
    expect(page.locator('.MuiMenuItem-root')).to_have_count(2)

def test_menu_button_custom_icon(page):
    # Test with a custom SVG icon
    svg_icon = '<svg viewBox="0 0 24 24"><path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>'
    widget = MenuButton(
        label='Menu Button',
        icon=svg_icon,
        items=[{'label': 'Item 1'}]
    )
    serve_component(page, widget)

    # Verify custom icon is displayed
    expect(page.locator('.MuiButton-icon span')).to_have_css('mask-image', 'url("data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQgMjQiPjxwYXRoIGQ9Ik0zIDE4aDE4di0ySDN2MnptMC01aDE4di0ySDN2MnptMC03djJoMThWNkgzeiIvPjwvc3ZnPg==")')

def test_menu_button_menu_position(page):
    widget = MenuButton(
        label='Menu Button',
        items=[{'label': 'Item 1'}]
    )
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButton-root').click()
    menu = page.locator('.MuiMenu-paper')

    # Verify menu is positioned correctly
    expect(menu).to_be_visible()
    menu_box = menu.bounding_box()
    button_box = page.locator('.MuiButton-root').bounding_box()

    # Menu should be below the button
    assert menu_box['y'] > button_box['y']
    # Menu should be aligned with the right side of the button
    assert abs(menu_box['x'] + menu_box['width'] - (button_box['x'] + button_box['width'])) < 1
