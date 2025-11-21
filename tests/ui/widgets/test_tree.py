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
            "id": "files",
            "label": "Files",
            "items": [
                {"id": "reports", "label": "Reports"},
                {"id": "logs", "label": "Logs"}
            ]
        },
        {"id": "settings", "label": "Settings"}
    ])


def test_tree_basic_render(page):
    widget = Tree(items=_tree_items(), expanded=["files"])
    serve_component(page, widget)

    tree = page.locator('[role="tree"]')
    expect(tree).to_have_count(1)

    # Parent + two children + second root item
    expect(page.locator('[role="treeitem"]')).to_have_count(4)


def test_tree_item_selection_updates_param(page):
    widget = Tree(items=_tree_items(), expanded=["files"])
    serve_component(page, widget)

    page.get_by_role("treeitem", name="Logs").click()
    wait_until(lambda: widget.selected == "logs", page)

    page.get_by_role("treeitem", name="Settings").click()
    wait_until(lambda: widget.selected == "settings", page)


def test_tree_honors_selectable_flag(page):
    items = [
        {"id": "allowed", "label": "Allowed"},
        {"id": "blocked", "label": "Blocked", "selectable": False},
    ]
    widget = Tree(items=items)
    serve_component(page, widget)

    page.get_by_role("treeitem", name="Allowed").click()
    wait_until(lambda: widget.selected == "allowed", page)

    page.get_by_role("treeitem", name="Blocked").click()
    # Non-selectable item should not change the selected value
    wait_until(lambda: widget.selected == "allowed", page)


def test_tree_secondary_and_buttons_render(page):
    items = [{
        "id": "doc",
        "label": "Document",
        "secondary": "Latest revision",
        "buttons": [{"label": "Open doc"}]
    }]
    widget = Tree(items=items)
    serve_component(page, widget)

    expect(page.get_by_text("Latest revision")).to_have_count(1)
    expect(page.get_by_role("button", name="Open doc")).to_have_count(1)
