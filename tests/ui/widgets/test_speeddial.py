import time

import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import SpeedDial
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


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

def test_speeddial_update_item(page):
    """Test updating a speed dial item and verifying it renders in the frontend"""
    items = [
        {'label': 'Camera', 'icon': 'camera'},
        {'label': 'Photos', 'icon': 'photo'}
    ]
    widget = SpeedDial(items=items)
    serve_component(page, widget)

    # Open speed dial
    page.locator('.MuiSpeedDial-fab').click()
    wait_until(lambda: page.locator('.MuiSpeedDial-actions').is_visible(), page)

    actions = page.locator('.MuiSpeedDialAction-fab')
    # Hover to see tooltip
    actions.nth(0).hover()
    tooltip = page.locator('#-action-0')
    expect(tooltip).to_have_text('Camera')

    # Update the item
    item_to_update = items[0]
    widget.update_item(item_to_update, label='Video Camera', icon='videocam', color='secondary')

    # Wait for frontend to update
    assert widget.items[0]['label'] == 'Video Camera'

    # Verify update (hover again to see updated tooltip)
    actions.nth(0).hover()
    wait_until(lambda: tooltip.text_content() == 'Video Camera', page)
    expect(tooltip).to_have_text('Video Camera')

def test_speeddial_update_item_with_avatar(page):
    """Test updating a speed dial item with avatar"""
    items = [
        {'label': 'Action 1', 'icon': 'add'}
    ]
    widget = SpeedDial(items=items)
    serve_component(page, widget)

    # Open speed dial
    page.locator('.MuiSpeedDial-fab').click()
    wait_until(lambda: page.locator('.MuiSpeedDial-actions').is_visible(), page)

    # Update item to add avatar
    item_to_update = items[0]
    widget.update_item(item_to_update, avatar='A', icon=None, color='primary')

    assert 'avatar' in widget.items[0] and widget.items[0]['avatar'] == 'A'

    # Verify avatar is rendered (speed dial shows avatar when provided)
    actions = page.locator('.MuiSpeedDialAction-fab')
    expect(actions.nth(0).locator('.MuiAvatar-root')).to_have_text('A')
