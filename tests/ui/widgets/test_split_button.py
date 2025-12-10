import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import SplitButton
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_split_button_split_mode(page):
    items = [{'label': 'Option 1'}, {'label': 'Option 2'}, {'label': 'Option 3'}]
    widget = SplitButton(items=items, label='Menu')
    events = []
    widget.on_click(events.append)

    serve_component(page, widget)

    # Check button exists
    button = page.locator('.MuiButtonBase-root')

    expect(button.nth(0)).to_have_text('Menu')

    button.nth(0).click()
    wait_until(lambda: len(events) == 1, page)
    assert events[0] == 'Menu'

    button.nth(1).click()
    menu_items = page.locator('.MuiMenuItem-root')
    expect(menu_items).to_have_count(3)

    menu_items.nth(1).click()
    wait_until(lambda: len(events) == 2, page)
    assert events[1] == items[1]


def test_split_button_select_mode(page):
    items = [{'label': 'Option 1'}, {'label': 'Option 2'}, {'label': 'Option 3'}]
    widget = SplitButton(items=items, label='Menu', mode='select')
    events = []
    widget.on_click(events.append)

    serve_component(page, widget)

    # Check button exists
    button = page.locator('.MuiButtonBase-root')

    expect(button.nth(0)).to_have_text('Option 1')

    widget.active = 1
    expect(button.nth(0)).to_have_text('Option 2')

    button.nth(0).click()
    wait_until(lambda: len(events) == 1, page)
    assert events[0] == items[1]

    button.nth(1).click()
    menu_items = page.locator('.MuiMenuItem-root')
    expect(menu_items).to_have_count(3)

    menu_items.nth(2).click()
    wait_until(lambda: len(events) == 1, page)
    expect(button.nth(0)).to_have_text('Option 3')

    button.nth(0).click()
    wait_until(lambda: len(events) == 2, page)
    assert events[1] == items[2]

def test_split_button_focus(page):
    items = [{'label': 'Option 1'}, {'label': 'Option 2'}]
    widget = SplitButton(items=items, label='Menu')
    serve_component(page, widget)
    button = page.locator('.MuiButtonBase-root').nth(0)
    expect(button).to_have_count(1)
    widget.focus()
    expect(button).to_be_focused()

def test_split_button_update_item(page):
    """Test updating a split button item and verifying it renders in the frontend"""
    items = [
        {'label': 'Open'},
        {'label': 'Save'}
    ]
    widget = SplitButton(items=items, label='File')
    serve_component(page, widget)

    # Open menu to see items
    page.locator('.MuiButtonBase-root').nth(1).click()
    menu_items = page.locator('.MuiMenuItem-root')
    expect(menu_items.nth(0)).to_have_text('Open')

    # Update the item
    item_to_update = items[0]
    widget.update_item(item_to_update, label='Open File', icon='folder_open')

    assert widget.items[0]['label'] == 'Open File'

    # Reopen menu to verify update
    page.locator('.MuiButtonBase-root').nth(1).click(force=True)
    expect(menu_items.nth(0)).to_have_text('folder_openOpen File')
    expect(menu_items.nth(0).locator('.material-icons')).to_have_text('folder_open')
    expect(menu_items.nth(1)).to_have_text('Save')  # Other item unchanged

def test_split_button_update_item_with_href(page):
    """Test updating a split button item with href"""
    items = [
        {'label': 'Option 1'},
        {'label': 'Option 2'}
    ]
    widget = SplitButton(items=items, label='Menu')
    serve_component(page, widget)

    # Open menu
    page.locator('.MuiButtonBase-root').nth(1).click(force=True)

    # Update item to add href
    item_to_update = items[1]
    widget.update_item(item_to_update, href='/option2', target='_blank')

    assert 'href' in widget.items[1] and widget.items[1]['href'] == '/option2'

    # Reopen menu to verify
    page.locator('.MuiButtonBase-root').nth(1).click(force=True)
    expect(page.locator('.MuiMenuItem-root').nth(1)).to_have_attribute('href', '/option2')
    expect(page.locator('.MuiMenuItem-root').nth(1)).to_have_attribute('target', '_blank')
