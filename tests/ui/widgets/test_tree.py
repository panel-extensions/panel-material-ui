import copy

import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Tree
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def _tree_items():
    return copy.deepcopy([
        {
            "label": "Files",
            "items": [
                {"label": "Reports"},
                {"label": "Logs"}
            ]
        },
        {"label": "Settings"}
    ])


def test_tree_basic_render(page):
    widget = Tree(items=_tree_items(), expanded=[(0,)])
    serve_component(page, widget)

    tree = page.locator('[role="tree"]')
    expect(tree).to_have_count(1)

    # Parent + two children + second root item
    expect(page.locator('[role="treeitem"]')).to_have_count(4)


def test_tree_item_selection_updates_param(page):
    widget = Tree(items=_tree_items(), expanded=[(0,)])
    serve_component(page, widget)

    page.get_by_role("treeitem", name="Logs").click()
    wait_until(lambda: widget.active == [(0, 1)], page)

    page.get_by_role("treeitem", name="Settings").click()
    wait_until(lambda: widget.active == [(1,)], page)


def test_tree_honors_selectable_flag(page):
    items = [
        {"label": "Allowed"},
        {"label": "Blocked", "selectable": False},
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    page.get_by_role("treeitem", name="Allowed").click()
    wait_until(lambda: widget.active == [(0,)], page)

    page.get_by_role("treeitem", name="Blocked").click()
    # Non-selectable item should not change the selected value
    wait_until(lambda: widget.active == [(0,)], page)


def test_tree_selection_without_ids(page):
    widget = Tree(items=[
        {"label": "Alpha"},
        {"label": "Beta", "items": [{"label": "Nested"}]}
    ], expanded=[(1,)])
    serve_component(page, widget)

    page.get_by_role("treeitem", name="Nested").click()
    wait_until(lambda: widget.active == [(1, 0)], page)


def test_tree_checkbox_selection(page):
    widget = Tree(items=_tree_items(), checkboxes=True, expanded=[(0,)])
    serve_component(page, widget)

    checkboxes = page.locator("input[type='checkbox']")

    # Select "Reports"
    checkboxes.nth(1).click(force=True)
    wait_until(lambda: widget.active == [(0, 0)], page)

    # Select "Logs" as well
    checkboxes.nth(2).click(force=True)
    wait_until(lambda: widget.active == [(0, 0), (0, 1)], page)


def test_tree_secondary_and_buttons_render(page):
    items = [{
        "label": "Document",
        "secondary": "Latest revision",
        "buttons": [{"label": "Open doc"}]
    }]
    widget = Tree(items=items)
    serve_component(page, widget)

    expect(page.get_by_text("Latest revision")).to_have_count(1)
    expect(page.get_by_role("button", name="Open doc")).to_have_count(1)


def test_tree_disabled_items_not_selectable(page):
    items = [
        {"label": "Enabled"},
        {"label": "Disabled", "disabled": True},
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    # Select enabled item
    page.get_by_role("treeitem", name="Enabled").click()
    wait_until(lambda: widget.active == [(0,)], page)

    # Try to select disabled item - should not change selection
    page.get_by_role("treeitem", name="Disabled").click(force=True)
    wait_until(lambda: widget.active == [(0,)], page)


def test_tree_disabled_items_have_disabled_styling(page):
    items = [
        {"label": "Enabled"},
        {"label": "Disabled", "disabled": True},
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    # Check that disabled item has disabled attribute
    disabled_item = page.get_by_role("treeitem", name="Disabled")
    expect(disabled_item.locator('[data-disabled="true"]')).to_have_count(1)


def test_tree_disabled_items_in_nested_structure(page):
    items = [
        {
            "label": "Parent",
            "items": [
                {"label": "Enabled Child"},
                {"label": "Disabled Child", "disabled": True},
            ]
        }
    ]
    widget = Tree(items=items, expanded=[(0,)])
    serve_component(page, widget)

    # Select enabled child
    page.get_by_role("treeitem", name="Enabled Child").click()
    wait_until(lambda: widget.active == [(0, 0)], page)

    # Try to select disabled child - should not change selection
    page.get_by_role("treeitem", name="Disabled Child").click(force=True)
    wait_until(lambda: widget.active == [(0, 0)], page)


def test_tree_disabled_items_can_still_expand(page):
    items = [
        {
            "label": "Disabled Parent",
            "disabled": True,
            "items": [
                {"label": "Child 1"},
                {"label": "Child 2"},
            ]
        }
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    # Initially collapsed
    expect(page.get_by_role("treeitem", name="Child 1")).not_to_be_visible()

    # Click expand icon - should expand even though parent is disabled
    parent = page.get_by_role("treeitem", name="Disabled Parent")
    # Find and click the expand icon (usually a button or icon within the treeitem)
    expand_button = parent.locator(".MuiSvgIcon-root").first
    expand_button.click(force=True)

    # Children should not be visible
    expect(page.get_by_role("treeitem", name="Child 1")).to_be_hidden()

def test_tree_disabled_items_with_checkboxes(page):
    items = [
        {"label": "Enabled", "id": "enabled"},
        {"label": "Disabled", "id": "disabled", "disabled": True},
    ]
    widget = Tree(items=items, checkboxes=True)
    serve_component(page, widget)

    checkboxes = page.locator("input[type='checkbox']")

    # Enabled checkbox should be clickable
    checkboxes.nth(0).click(force=True)
    wait_until(lambda: widget.active == [(0,)], page)

    # Disabled checkbox should not be clickable/checked
    disabled_checkbox = checkboxes.nth(1)
    expect(disabled_checkbox).to_be_disabled()

    # Try clicking disabled checkbox - selection should not change
    disabled_checkbox.click(force=True)
    wait_until(lambda: widget.active == [(0,)], page)


def test_tree_mixed_disabled_and_selectable(page):
    items = [
        {"label": "Selectable", "selectable": True},
        {"label": "Non-selectable", "selectable": False},
        {"label": "Disabled", "disabled": True},
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    # Select selectable item
    page.get_by_role("treeitem").nth(0).click(force=True)
    wait_until(lambda: widget.active == [(0,)], page)

    # Try non-selectable - should not change
    page.get_by_role("treeitem").nth(1).click(force=True)
    wait_until(lambda: widget.active == [(0,)], page)

    # Try disabled - should not change
    page.get_by_role("treeitem").nth(2).click(force=True)
    wait_until(lambda: widget.active == [(0,)], page)


def test_menu_list_with_toggle_actions(page):
    widget = Tree(items=[{
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
    expect(page.get_by_role("treeitem").locator('.MuiCheckbox-root .material-icons-outlined')).to_have_text('edit')
    page.get_by_role("treeitem").locator('.MuiCheckbox-root').click()
    expect(page.get_by_role("treeitem").locator('.MuiCheckbox-root .material-icons')).to_have_text('edit')
    wait_until(lambda: edit_actions == [True], page)

    widget.toggle_action(widget.items[0], "Edit", False)
    expect(page.get_by_role("treeitem").locator('.MuiCheckbox-root .material-icons-outlined')).to_have_text('edit')

def test_tree_update_item(page):
    """Test updating a tree item and verifying it renders in the frontend"""
    items = [
        {'id': '1', 'label': 'Node 1'},
        {'id': '2', 'label': 'Node 2'}
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    # Verify initial state
    tree_items = page.locator('[role="treeitem"]')
    expect(tree_items.nth(0)).to_have_text('Node 1')

    # Update the item
    item_to_update = items[0]
    widget.update_item(item_to_update, label='Updated Node 1', disabled=True)
    assert widget.items[0]['label'] == 'Updated Node 1'

    expect(tree_items.nth(0)).to_have_text('Updated Node 1')
    expect(tree_items.nth(0).locator('[data-disabled="true"]')).to_have_count(1)
    expect(tree_items.nth(1)).to_have_text('Node 2')  # Other item unchanged

def test_tree_update_item_nested(page):
    """Test updating a nested tree item"""
    items = [
        {
            'id': 'parent',
            'label': 'Parent',
            'items': [
                {'id': 'child1', 'label': 'Child 1'},
                {'id': 'child2', 'label': 'Child 2'}
            ]
        }
    ]
    widget = Tree(items=items, expanded=[(0,)])
    serve_component(page, widget)

    # Verify initial state
    child_items = page.locator('[role="treeitem"]')
    expect(child_items.nth(1)).to_have_text('Child 1')

    # Update the nested item
    child_to_update = items[0]['items'][0]
    widget.update_item(child_to_update, label='Updated Child', file_type='pdf')
    assert widget.items[0]['items'][0]['label'] == 'Updated Child'

    expect(child_items.nth(1)).to_have_text('Updated Child')
    expect(child_items.nth(2)).to_have_text('Child 2')  # Other child unchanged

def test_tree_update_item_with_secondary(page):
    """Test updating a tree item with secondary text"""
    items = [
        {'id': '1', 'label': 'Node 1'},
        {'id': '2', 'label': 'Node 2'}
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    # Update item to add secondary text
    item_to_update = items[1]
    widget.update_item(item_to_update, secondary='Secondary text', selectable=False)

    assert 'secondary' in widget.items[1] and widget.items[1]['secondary'] == 'Secondary text'
    expect(page.locator('[role="treeitem"]').nth(1)).to_contain_text('Secondary text')
