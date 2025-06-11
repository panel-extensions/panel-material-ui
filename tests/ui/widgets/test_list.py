import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import List
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

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

def test_list_basic_functionality(page):
    widget = List(items=["Item 1", "Item 2", "Item 3"])
    serve_component(page, widget)

    # Verify basic rendering
    expect(page.locator('.MuiList-root')).to_have_count(1)
    expect(page.locator('.MuiListItemButton-root')).to_have_count(3)
    expect(page.locator('.MuiListItemButton-root').nth(0)).to_have_text('IItem 1')
    expect(page.locator('.MuiListItemButton-root').nth(1)).to_have_text('IItem 2')
    expect(page.locator('.MuiListItemButton-root').nth(2)).to_have_text('IItem 3')

def test_list_item_selection(page):
    widget = List(items=["Item 1", "Item 2", "Item 3"])
    serve_component(page, widget)

    # Select first item
    page.locator('.MuiListItemButton-root').first.click()
    wait_until(lambda: widget.active == 0, page)
    expect(page.locator('.MuiListItemButton-root.Mui-selected')).to_have_text('IItem 1')

    # Select second item
    page.locator('.MuiListItemButton-root').nth(1).click()
    wait_until(lambda: widget.active == 1, page)
    expect(page.locator('.MuiListItemButton-root.Mui-selected')).to_have_text('IItem 2')

def test_list_nested_items(page):
    widget = List(items=[
        "Item 1",
        {
            "label": "Nested",
            "items": ["Nested 1", "Nested 2"]
        }
    ])
    serve_component(page, widget)

    # Verify initial state
    expect(page.locator('.MuiListItemButton-root')).to_have_count(4)  # Main items
    expect(page.locator('.MuiCollapse-root')).to_have_count(1)  # Nested container

    # Expand nested items
    page.locator('.MuiListItemButton-root').nth(1).locator('button').click()
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root')).to_have_count(0)
    page.locator('.MuiListItemButton-root').nth(1).locator('button').click()
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root')).to_have_count(2)
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root').nth(0)).to_have_text('NNested 1')
    expect(page.locator('.MuiCollapse-root .MuiListItemButton-root').nth(1)).to_have_text('NNested 2')

    # Select nested item
    page.locator('.MuiCollapse-root .MuiListItemButton-root').first.click()
    wait_until(lambda: widget.active == (1, 0), page)

def test_list_with_icons(page):
    widget = List(items=[
        {"label": "Item 1", "icon": "home"},
        {"label": "Item 2", "icon": "settings"}
    ])
    serve_component(page, widget)

    # Verify icons
    icons = page.locator('.MuiListItemIcon-root .material-icons')
    expect(icons.nth(0)).to_have_text('home')
    expect(icons.nth(1)).to_have_text('settings')

def test_list_with_avatars(page):
    widget = List(items=[
        {"label": "Item 1", "avatar": "A"},
        {"label": "Item 2"}  # Should use first letter of label
    ])
    serve_component(page, widget)

    # Verify avatars
    avatars = page.locator('.MuiAvatar-root')
    expect(avatars.nth(0)).to_have_text('A')
    expect(avatars.nth(1)).to_have_text('I')  # First letter of "Item 2"

def test_list_with_secondary_text(page):
    widget = List(items=[
        {"label": "Item 1", "secondary": "Description 1"},
        {"label": "Item 2", "secondary": "Description 2"}
    ])
    serve_component(page, widget)

    # Verify secondary text
    expect(page.locator('.MuiListItemText-secondary').nth(0)).to_have_text('Description 1')
    expect(page.locator('.MuiListItemText-secondary').nth(1)).to_have_text('Description 2')

def test_list_with_actions(page):
    widget = List(items=[{
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

def test_list_with_dividers(page):
    widget = List(items=[
        "Item 1",
        None,  # Divider
        "Item 2"
    ])
    serve_component(page, widget)

    # Verify divider
    expect(page.locator('.MuiDivider-root')).to_have_count(1)
    expect(page.locator('.MuiListItemButton-root')).to_have_count(2)

def test_list_dense_mode(page):
    widget = List(items=["Item 1", "Item 2"], dense=True)
    serve_component(page, widget)

    # Verify dense mode
    expect(page.locator('.MuiListItemButton-dense')).to_have_count(2)

def test_list_highlight_behavior(page):
    widget = List(items=["Item 1", "Item 2"], highlight=False)
    serve_component(page, widget)

    # Select item and verify no highlight
    page.locator('.MuiListItemButton-root').first.click()
    expect(page.locator('.MuiListItemButton-root').first).not_to_have_class('Mui-selected')

def test_list_with_href(page):
    widget = List(items=[
        {"label": "Link 1", "href": "https://example.com"},
        {"label": "Link 2", "href": "https://example.org", "target": "_blank"}
    ])
    serve_component(page, widget)

    # Verify href attributes
    expect(page.locator('.MuiListItemButton-root').nth(0)).to_have_attribute('href', 'https://example.com')
    expect(page.locator('.MuiListItemButton-root').nth(1)).to_have_attribute('href', 'https://example.org')
    expect(page.locator('.MuiListItemButton-root').nth(1)).to_have_attribute('target', '_blank')

def test_list_with_label(page):
    label = "List Label"
    widget = List(items=["Item 1", "Item 2"], label=label)
    serve_component(page, widget)

    # Verify label
    expect(page.locator('.MuiListSubheader-root')).to_have_text(label)

def test_list_action_callback(page):
    events = []
    def cb(event):
        events.append(event)

    widget = List(items=[{
        "label": "Item 1",
        "actions": [{"label": "Action", "icon": "edit"}]
    }])
    widget.on_action("Action", cb)
    serve_component(page, widget)

    # Trigger action
    page.locator('.MuiListItemButton-root button').click()
    page.locator('.MuiMenu-root .MuiMenuItem-root').click()
    wait_until(lambda: len(events) == 1, page)

def test_list_non_selectable_items(page):
    widget = List(items=[
        {"label": "Selectable", "selectable": True},
        {"label": "Non-selectable", "selectable": False}
    ])
    serve_component(page, widget)

    # Click non-selectable item
    page.locator('.MuiListItemButton-root').nth(1).click()
    expect(page.locator('.MuiListItemButton-root').nth(1)).not_to_have_class('Mui-selected')
    assert widget.active is None
