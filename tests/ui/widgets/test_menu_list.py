import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import MenuList
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

def test_menu_list(page):
    widget = MenuList(name='List test', items=['Item 1', 'Item 2', 'Item 3'])
    serve_component(page, widget)

    expect(page.locator(".menu-list")).to_have_count(1)
    expect(page.locator(".MuiList-root")).to_have_count(1)

    expect(page.locator(".MuiListItemText-root")).to_have_count(3)
    expect(page.locator(".MuiListItemText-root").nth(0)).to_have_text("Item 1")
    expect(page.locator(".MuiListItemText-root").nth(1)).to_have_text("Item 2")
    expect(page.locator(".MuiListItemText-root").nth(2)).to_have_text("Item 3")

    for i in range(3):
        page.locator(".MuiListItemButton-root").nth(i).click()
        wait_until(lambda: widget.value == widget.items[i], page)

def test_menu_list_basic(page):
    items = [
        {'label': 'Item 1'},
        {'label': 'Item 2'},
        {'label': 'Item 3'}
    ]
    widget = MenuList(items=items)
    serve_component(page, widget)

    list_items = page.locator('.MuiListItemButton-root')
    expect(list_items).to_have_count(3)

def test_menu_list_nested(page):
    items = [
        {
            'label': 'Item 1',
            'items': [
                {'label': 'Subitem 1'},
                {'label': 'Subitem 2'}
            ]
        }
    ]
    widget = MenuList(items=items)
    serve_component(page, widget)

    # Click to expand
    page.locator('.MuiListItemButton-root > .MuiIconButton-root').first.click()

    # Check subitems are visible
    subitems = page.locator('.MuiCollapse-root .MuiListItemButton-root')
    expect(subitems).to_have_count(2)

def test_menu_list_selection(page):
    items = [
        {'label': 'Item 1'},
        {'label': 'Item 2'},
        {'label': 'Item 3'}
    ]
    widget = MenuList(items=items)
    serve_component(page, widget)

    list_items = page.locator('.MuiListItemButton-root')
    list_items.nth(1).click()

    assert widget.active == (1,)
    assert widget.value == items[1]

def test_menu_list_basic_functionality(page):
    widget = MenuList(items=["Item 1", "Item 2", "Item 3"])
    serve_component(page, widget)

    # Verify basic rendering
    expect(page.locator('.MuiList-root')).to_have_count(1)
    expect(page.locator('.MuiListItemButton-root')).to_have_count(3)
    expect(page.locator('.MuiListItemButton-root').nth(0)).to_have_text('IItem 1')
    expect(page.locator('.MuiListItemButton-root').nth(1)).to_have_text('IItem 2')
    expect(page.locator('.MuiListItemButton-root').nth(2)).to_have_text('IItem 3')

def test_menu_list_item_selection(page):
    widget = MenuList(items=["Item 1", "Item 2", "Item 3"])
    serve_component(page, widget)

    # Select first item
    page.locator('.MuiListItemButton-root').first.click()
    wait_until(lambda: widget.active == (0,), page)
    expect(page.locator('.MuiListItemButton-root.Mui-selected')).to_have_text('IItem 1')

    # Select second item
    page.locator('.MuiListItemButton-root').nth(1).click()
    wait_until(lambda: widget.active == (1,), page)
    expect(page.locator('.MuiListItemButton-root.Mui-selected')).to_have_text('IItem 2')

def test_menu_list_nested_items(page):
    widget = MenuList(items=[
        "Item 1",
        {
            "label": "Nested",
            "items": ["Nested 1", "Nested 2"]
        }
    ])
    serve_component(page, widget)

    # Verify initial state
    expect(page.locator('.MuiListItemButton-root')).to_have_count(2)  # Main items

    # Expand nested items
    page.locator('.MuiListItemButton-root').nth(1).locator('.MuiIconButton-root').click()
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root')).to_have_count(2)
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root').nth(0)).to_have_text('NNested 1')
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root').nth(1)).to_have_text('NNested 2')

    page.locator('.MuiCollapse-root .MuiListItemButton-root').first.click()
    wait_until(lambda: widget.active == (1, 0), page)

    page.locator('.MuiListItemButton-root').nth(1).locator('.MuiIconButton-root').click() # Collapse nested items
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root')).to_have_count(0)


def test_menu_list_with_icons(page):
    widget = MenuList(items=[
        {"label": "Item 1", "icon": "home"},
        {"label": "Item 2", "icon": "settings"}
    ])
    serve_component(page, widget)

    # Verify icons
    icons = page.locator('.MuiListItemIcon-root .material-icons')
    expect(icons.nth(0)).to_have_text('home')
    expect(icons.nth(1)).to_have_text('settings')

def test_menu_list_with_avatars(page):
    widget = MenuList(items=[
        {"label": "Item 1", "avatar": "A"},
        {"label": "Item 2"}  # Should use first letter of label
    ])
    serve_component(page, widget)

    # Verify avatars
    avatars = page.locator('.MuiAvatar-root')
    expect(avatars.nth(0)).to_have_text('A')
    expect(avatars.nth(1)).to_have_text('I')  # First letter of "Item 2"

def test_menu_list_with_secondary_text(page):
    widget = MenuList(items=[
        {"label": "Item 1", "secondary": "Description 1"},
        {"label": "Item 2", "secondary": "Description 2"}
    ])
    serve_component(page, widget)

    # Verify secondary text
    expect(page.locator('.MuiListItemText-secondary').nth(0)).to_have_text('Description 1')
    expect(page.locator('.MuiListItemText-secondary').nth(1)).to_have_text('Description 2')

def test_menu_list_with_actions(page):
    widget = MenuList(items=[{
        "label": "Item 1",
        "actions": [
            {"label": "Edit", "icon": "edit", "inline": True},
            {"label": "Delete", "icon": "delete", "inline": False}
        ]
    }])
    serve_component(page, widget)

    # Verify inline action
    expect(page.locator('.MuiListItemButton-root button .material-icons')).to_have_text('edit')

    # Open menu and verify menu action
    page.locator('.MuiListItemButton-root button').nth(1).click()
    expect(page.locator('.MuiMenu-root .MuiMenuItem-root')).to_have_text('deleteDelete')
    expect(page.locator('.MuiMenu-root .material-icons')).to_have_text('delete')

def test_menu_list_with_toggle_actions(page):
    widget = MenuList(items=[{
        "label": "Item 1",
        "actions": [
            {"label": "Edit", "icon": "edit", "inline": True, "toggle": True},
            {"label": "Delete", "icon": "delete", "inline": False, "toggle": True}
        ]
    }])

    edit_actions, delete_actions = [], []
    widget.on_action("Edit", lambda item: edit_actions.append(item['actions'][0]['value']))
    widget.on_action("Delete", lambda item: edit_actions.append(item['actions'][1]['value']))
    serve_component(page, widget)

    # Verify inline action
    expect(page.locator('.MuiListItemButton-root .MuiCheckbox-root .material-icons-outlined')).to_have_text('edit')
    page.locator('.MuiListItemButton-root .MuiCheckbox-root').click()
    expect(page.locator('.MuiListItemButton-root .MuiCheckbox-root .material-icons')).to_have_text('edit')
    wait_until(lambda: edit_actions == [True], page)

    widget.toggle_action(widget.items[0], "Edit", False)
    expect(page.locator('.MuiListItemButton-root .MuiCheckbox-root .material-icons-outlined')).to_have_text('edit')

def test_menu_list_with_dividers(page):
    widget = MenuList(items=[
        "Item 1",
        None,  # Divider
        "Item 2"
    ])
    serve_component(page, widget)

    # Verify divider
    expect(page.locator('.MuiDivider-root')).to_have_count(1)
    expect(page.locator('.MuiListItemButton-root')).to_have_count(2)

def test_menu_list_dense_mode(page):
    widget = MenuList(items=["Item 1", "Item 2"], dense=True)
    serve_component(page, widget)

    # Verify dense mode
    expect(page.locator('.MuiListItemButton-dense')).to_have_count(2)

def test_menu_list_highlight_behavior(page):
    widget = MenuList(items=["Item 1", "Item 2"], highlight=False)
    serve_component(page, widget)

    # Select item and verify no highlight
    page.locator('.MuiListItemButton-root').first.click()
    expect(page.locator('.MuiListItemButton-root').first).not_to_have_class('Mui-selected')

def test_menu_list_with_href(page):
    widget = MenuList(items=[
        {"label": "Link 1", "href": "https://example.com"},
        {"label": "Link 2", "href": "https://example.org", "target": "_blank"}
    ])
    serve_component(page, widget)

    # Verify href attributes
    expect(page.locator('.MuiListItemButton-root').nth(0)).to_have_attribute('href', 'https://example.com')
    expect(page.locator('.MuiListItemButton-root').nth(1)).to_have_attribute('href', 'https://example.org')
    expect(page.locator('.MuiListItemButton-root').nth(1)).to_have_attribute('target', '_blank')

def test_menu_list_with_label(page):
    label = "List Label"
    widget = MenuList(items=["Item 1", "Item 2"], label=label)
    serve_component(page, widget)

    # Verify label
    expect(page.locator('.MuiListSubheader-root')).to_have_text(label)

def test_menu_list_action_callback(page):
    events = []
    def cb(event):
        events.append(event)

    widget = MenuList(items=[{
        "label": "Item 1",
        "actions": [{"label": "Action", "icon": "edit"}]
    }])
    widget.on_action("Action", cb)
    serve_component(page, widget)

    # Trigger action
    page.locator('.MuiListItemButton-root button').click()
    page.locator('.MuiMenu-root .MuiMenuItem-root').click()
    wait_until(lambda: len(events) == 1, page)

def test_menu_list_non_selectable_items(page):
    widget = MenuList(items=[
        {"label": "Selectable", "selectable": True},
        {"label": "Non-selectable", "selectable": False}
    ])
    serve_component(page, widget)

    # Click non-selectable item
    page.locator('.MuiListItemButton-root').nth(1).click()
    expect(page.locator('.MuiListItemButton-root').nth(1)).not_to_have_class('Mui-selected')
    assert widget.active is None

def test_menu_list_collapsed(page):
    widget = MenuList(items=[
        {"label": "Item 1", "icon": "home"},
        {"label": "Item 2", "icon": "settings"},
        {"label": "Item 3"}  # No icon, should show avatar
    ], collapsed=True)
    serve_component(page, widget)

    # Verify ListItemText is not rendered when collapsed
    expect(page.locator('.MuiListItemText-root')).to_have_count(0)

    # Verify icons are still rendered
    icons = page.locator('.MuiListItemIcon-root .material-icons')
    expect(icons).to_have_count(2)
    expect(icons.nth(0)).to_have_text('home')
    expect(icons.nth(1)).to_have_text('settings')

    # Verify avatar is rendered for item without icon
    avatars = page.locator('.MuiAvatar-root')
    expect(avatars).to_have_count(1)
    expect(avatars.nth(0)).to_have_text('I')  # First letter of "Item 3"

    # Verify collapsed class is applied
    expect(page.locator('.MuiListItemButton-root.collapsed')).to_have_count(3)

    # Verify tooltips display labels on hover
    # Hover over first item with icon
    tooltip = page.locator('.MuiTooltip-popper')
    page.locator('.MuiListItemButton-root').nth(0).hover()
    expect(tooltip).to_have_count(1)
    expect(tooltip).to_be_visible()
    expect(tooltip).to_have_text('Item 1')

    # Hover over second item with icon
    page.locator('.MuiListItemButton-root').nth(1).hover()
    expect(tooltip).to_have_count(1)
    expect(tooltip).to_be_visible()
    expect(tooltip).to_have_text('Item 2')

    # Hover over third item with avatar
    page.locator('.MuiListItemButton-root').nth(2).hover()
    expect(tooltip).to_have_count(1)
    expect(tooltip).to_be_visible()
    expect(tooltip).to_have_text('Item 3')

def test_menu_list_update_item(page):
    """Test updating a menu list item and verifying it renders in the frontend"""
    items = [
        {'label': 'Home'},
        {'label': 'Dashboard'},
        {'label': 'Profile'}
    ]
    widget = MenuList(items=items)
    serve_component(page, widget)

    # Verify initial state
    list_items = page.locator('.MuiListItemButton-root')
    expect(list_items.nth(1)).to_have_text('DDashboard')

    # Update the item
    item_to_update = items[1]
    widget.update_item(item_to_update, label='Settings', secondary='Settings page')

    # Wait for frontend to update
    assert widget.items[1]['label'] == 'Settings'
    expect(list_items.nth(1).locator('.MuiListItemText-primary')).to_have_text('Settings')
    expect(list_items.nth(1).locator('.MuiListItemText-secondary')).to_have_text('Settings page')
    expect(list_items.nth(0).locator('.MuiListItemText-primary')).to_have_text('Home')  # Other items unchanged

def test_menu_list_update_item_nested(page):
    """Test updating a nested menu list item"""
    items = [
        {
            'label': 'Parent',
            'items': [
                {'label': 'Child 1'},
                {'label': 'Child 2'}
            ]
        }
    ]
    widget = MenuList(items=items)
    serve_component(page, widget)

    # Expand parent to show children
    page.locator('.MuiListItemButton-root').first.locator('.MuiIconButton-root').click()
    wait_until(lambda: page.locator('.MuiCollapse-root .MuiListItemButton-root').count() == 2, page)

    # Verify initial state
    child_items = page.locator('.MuiCollapse-root .MuiListItemButton-root')
    expect(child_items.nth(0).locator('.MuiListItemText-primary')).to_have_text('Child 1')

    # Update the nested item
    child_to_update = items[0]['items'][0]
    widget.update_item(child_to_update, label='Updated Child', icon='star')

    assert widget.items[0]['items'][0]['label'] == 'Updated Child'
    expect(child_items.nth(0).locator('.MuiListItemText-primary')).to_have_text('Updated Child')
    expect(child_items.nth(0).locator('.material-icons')).to_have_text('star')
    expect(child_items.nth(1).locator('.MuiListItemText-primary')).to_have_text('Child 2')  # Other child unchanged


def test_menu_list_update_item_with_icon(page):
    """Test updating a menu list item to add an icon"""
    items = [
        {'label': 'Home'},
        {'label': 'Dashboard'}
    ]
    widget = MenuList(items=items)
    serve_component(page, widget)

    # Update item to add icon
    item_to_update = items[0]
    widget.update_item(item_to_update, icon='home')

    assert 'icon' in widget.items[0] and widget.items[0]['icon'] == 'home'

    # Verify icon is rendered
    expect(page.locator('.MuiListItemButton-root').nth(0).locator('.material-icons')).to_have_text('home')
