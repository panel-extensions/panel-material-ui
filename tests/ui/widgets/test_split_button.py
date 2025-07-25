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
