import re

import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets.menus import NestedBreadcrumbs
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


ACTIVE_CLASS = re.compile(r".*\bMuiIcon-colorPrimary\b.*")

def _items_basic():
    # Multiple children under a single root for depth-1 switching.
    # A has two children (A1, A2); B has one child (B1).
    return [{
        "label": "Projects",
        "icon": "folder",
        "items": [
            {
                "label": "A",
                "icon": "category",
                "items": [
                    {"label": "A1", "icon": "grain"},
                    {"label": "A2", "icon": "grain"},
                ],
            },
            {
                "label": "B",
                "icon": "category",
                "items": [
                    {"label": "B1", "icon": "grain"},
                ],
            },
        ],
    }]

def test_nested_breadcrumbs_render_and_truncate(page):
    # Start on A: active=(0,) means root index is 0, child index at depth-1 is 0 (A) via tail.
    widget = NestedBreadcrumbs(items=_items_basic())
    serve_component(page, widget)

    # Renders full path: Projects > A > A1 (icon text appears in DOM)
    crumbs = page.locator(".MuiBreadcrumbs-ol .MuiBreadcrumbs-li")
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(0)).to_have_text("folderProjects")
    expect(crumbs.nth(1)).to_have_text("categoryA")
    expect(crumbs.nth(2)).to_have_text("grainA1")
    expect(crumbs.nth(0).locator('span.material-icons')).not_to_have_class(ACTIVE_CLASS)

    # Clicking the root (depth=0) should keep explicit selection at (0,)
    crumbs.nth(0).click()
    wait_until(lambda: widget.active == (0,), page)
    # And still render full path via tail
    wait_until(lambda: widget.path == (0, 0, 0), page)
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(2)).to_have_text("grainA1")
    expect(crumbs.nth(0).locator('span.material-icons')).to_have_class(ACTIVE_CLASS)

    # Clicking the middle segment (depth=1, "A") should expand explicit selection:
    # base = resolvedActive[: 1+1] -> (0, 0)
    crumbs.nth(1).click()
    wait_until(lambda: widget.active == (0, 0), page)
    # Full path now explicitly includes the same leaf via tail (still A1)
    wait_until(lambda: widget.path == (0, 0, 0), page)
    # The UI still shows Projects > A > A1
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(2)).to_have_text("grainA1")
    expect(crumbs.nth(1).locator('span.material-icons')).to_have_class(ACTIVE_CLASS)

    # Clicking the leaf (depth=2, "A1") grows explicit selection to include the leaf
    crumbs.nth(2).click()
    wait_until(lambda: widget.active == (0, 0, 0), page)
    # Path remains resolved to same chain
    expect(crumbs.nth(2)).to_have_text("grainA1")
    expect(crumbs.nth(2).locator('span.material-icons')).to_have_class(ACTIVE_CLASS)


def test_nested_breadcrumbs_menu_select_sibling_with_tail(page):
    widget = NestedBreadcrumbs(items=_items_basic(), active=(0,))
    serve_component(page, widget)

    # Open chevron menu at depth 1 (sibling switch for A/B)
    chevrons = page.locator('button[aria-label="Change selection"]')
    expect(chevrons).to_have_count(2)
    chevrons.nth(0).click()

    menu = page.locator(".MuiMenu-paper")
    expect(menu.nth(0)).to_be_visible()
    items = menu.nth(0).locator(".MuiMenuItem-root")
    expect(items).to_have_count(2)
    expect(items.nth(0)).to_contain_text("A")
    expect(items.nth(1)).to_contain_text("B")

    # Select "B" (idx=1) at depth=1 → active becomes (0, 1)
    # Rendered path auto-descends to B1 → path == (0, 1, 0)
    items.nth(1).click()
    wait_until(lambda: widget.active == (0, 1), page)
    wait_until(lambda: widget.path == (0, 1, 0), page)

    # Breadcrumbs now show Projects > B > B1
    crumbs = page.locator(".MuiBreadcrumbs-ol .MuiBreadcrumbs-li")
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(0)).to_have_text("folderProjects")
    expect(crumbs.nth(1)).to_have_text("categoryB")
    expect(crumbs.nth(2)).to_have_text("grainB1")


def test_nested_breadcrumbs_menu_non_selectable_item(page):
    items = [{
        "label": "Root",
        "items": [
            {"label": "Alpha"},
            {"label": "Beta", "selectable": False},   # not selectable
            {"label": "Gamma"},
        ],
    }]
    # start with explicit root only; rendered path will descend to first child (Alpha)
    widget = NestedBreadcrumbs(items=items, active=(0,))
    serve_component(page, widget)

    # Open chevron at depth 1
    page.locator('button[aria-label="Change selection"]').click()
    menu = page.locator(".MuiMenu-paper")
    expect(menu).to_be_visible()

    menu_items = menu.locator(".MuiMenuItem-root")
    expect(menu_items).to_have_count(3)
    expect(menu_items.nth(1)).to_contain_text("Beta")
    expect(menu_items.nth(1)).to_have_attribute("aria-disabled", "true")

    # Clicking disabled does nothing
    menu_items.nth(1).click(force=True)
    wait_until(lambda: widget.active == (0,), page)

    # Clicking Gamma updates active to (0, 2); rendered path ends at Gamma (no children)
    menu_items.nth(2).click()
    wait_until(lambda: widget.active == (0, 2), page)
    # No children → path equals explicit
    wait_until(lambda: widget.path == (0, 2), page)

    crumbs = page.locator(".MuiBreadcrumbs-ol .MuiBreadcrumbs-li")
    expect(crumbs).to_have_count(2)
    expect(crumbs.nth(0)).to_have_text("Root")
    expect(crumbs.nth(1)).to_have_text("Gamma")


def test_nested_breadcrumbs_menu_selected_marker(page):
    widget = NestedBreadcrumbs(items=_items_basic(), active=(0,))
    serve_component(page, widget)

    # At depth 1, A is currently selected (active[1] is implicit 0 via tail)
    page.locator('button[aria-label="Change selection"]').nth(0).click()
    menu = page.locator(".MuiMenu-paper")
    expect(menu.nth(0)).to_be_visible()

    # The first menu item (A) should be marked selected by MUI
    first_item = menu.locator(".MuiMenuItem-root").nth(0)
    expect(first_item).to_have_class(re.compile(r".*\bMui-selected\b.*"))


def test_nested_breadcrumbs_no_auto_descend_placeholder_flow(page):
    """
    With auto_descend=False:
    - Initial render shows: Projects > Select…
      (no implicit descent to A / A1)
    - Clicking the placeholder chevron opens a menu with A and B.
    - Selecting A sets active to (0, 0) and still shows a placeholder for A's children.
    - Selecting A2 sets active to (0, 0, 1) with no further placeholder (leaf).
    """
    widget = NestedBreadcrumbs(items=_items_basic(), active=(0,), auto_descend=False)
    serve_component(page, widget)

    crumbs = page.locator(".MuiBreadcrumbs-ol .MuiBreadcrumbs-li")
    # Only root + placeholder
    expect(crumbs).to_have_count(2)
    expect(crumbs.nth(0)).to_have_text("folderProjects")
    expect(crumbs.nth(1)).to_contain_text("Select…")

    # Placeholder chevron (depth == chain.length) opens children of root (A, B)
    placeholder_chevron = page.locator('button[aria-label="Choose item"]')
    expect(placeholder_chevron).to_have_count(1)
    placeholder_chevron.click()

    menu = page.locator(".MuiMenu-paper")
    expect(menu).to_be_visible()
    menu_items = menu.locator(".MuiMenuItem-root")
    expect(menu_items).to_have_count(2)
    expect(menu_items.nth(0)).to_contain_text("A")
    expect(menu_items.nth(1)).to_contain_text("B")

    # Select "A" (idx=0) -> active becomes (0, 0); still no auto tail
    menu_items.nth(0).click()
    wait_until(lambda: widget.active == (0, 0), page)
    # With no auto-descend, path equals explicit
    wait_until(lambda: widget.path == (0, 0), page)

    # Now we should see: Projects > A > Select…
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(0)).to_have_text("folderProjects")
    expect(crumbs.nth(1)).to_have_text("categoryA")
    expect(crumbs.nth(2)).to_contain_text("Select…")

    # Open placeholder again (children of A: A1, A2)
    page.locator('button[aria-label="Choose item"]').click()
    expect(menu.nth(1)).to_be_visible()
    menu_items = menu.nth(1).locator(".MuiMenuItem-root")
    expect(menu_items).to_have_count(2)
    expect(menu_items.nth(0)).to_contain_text("A1")
    expect(menu_items.nth(1)).to_contain_text("A2")

    # Choose A2 -> active becomes (0, 0, 1); leaf, so no placeholder
    menu_items.nth(1).click()
    wait_until(lambda: widget.active == (0, 0, 1), page)
    wait_until(lambda: widget.path == (0, 0, 1), page)

    # Breadcrumbs now: Projects > A > A2
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(2)).to_have_text("grainA2")


def test_nested_breadcrumbs_no_auto_descend_truncate(page):
    """
    With auto_descend=False:
    - Clicking a segment truncates the explicit active to that depth only.
    - No first-child tail is appended; path == active.
    - Placeholder shows up when the last explicit node has children.
    """
    widget = NestedBreadcrumbs(items=_items_basic(), active=(0, 0, 1), auto_descend=False)
    serve_component(page, widget)

    crumbs = page.locator(".MuiBreadcrumbs-ol .MuiBreadcrumbs-li")
    # We explicitly start at Projects > A > A2
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(0)).to_have_text("folderProjects")
    expect(crumbs.nth(1)).to_have_text("categoryA")
    expect(crumbs.nth(2)).to_have_text("grainA2")

    # Click middle segment "A" (depth=1) -> active becomes (0, 0) and no tail
    crumbs.nth(1).click()
    wait_until(lambda: widget.active == (0, 0), page)
    wait_until(lambda: widget.path == (0, 0), page)

    # Since A has children and auto_descend=False, we now see a placeholder
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(2)).to_contain_text("Select…")

    # Click root "Projects" (depth=0) -> active becomes (0,)
    crumbs.nth(0).click()
    wait_until(lambda: widget.active == (0,), page)
    wait_until(lambda: widget.path == (0,), page)

    # Root has children; placeholder is at depth 1
    expect(crumbs).to_have_count(2)
    expect(crumbs.nth(1)).to_contain_text("Select…")


def test_nested_breadcrumbs_restore_path_from_python(page):
    widget = NestedBreadcrumbs(items=_items_basic(), active=(0,), auto_descend=True)
    serve_component(page, widget)

    # Initially: Projects > A > A1 via tail
    crumbs = page.locator(".MuiBreadcrumbs-ol .MuiBreadcrumbs-li")
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(1)).to_have_text("categoryA")
    expect(crumbs.nth(2)).to_have_text("grainA1")
    expect(crumbs.nth(0).locator('span.material-icons')).to_have_class(ACTIVE_CLASS)

    # Now restore full path to Projects > B > B1
    widget.path = (0, 1, 0)

    wait_until(lambda: widget.active == (0,), page)
    wait_until(lambda: widget.path == (0, 1, 0), page)

    expect(crumbs.nth(1)).to_have_text("categoryB")
    expect(crumbs.nth(2)).to_have_text("grainB1")


def test_nested_breadcrumbs_restore_non_active_path_from_python(page):
    widget = NestedBreadcrumbs(items=_items_basic(), active=(0, 1, 0), auto_descend=True)
    serve_component(page, widget)

    # Initially: Projects > A > A1 via tail
    crumbs = page.locator(".MuiBreadcrumbs-ol .MuiBreadcrumbs-li")
    expect(crumbs).to_have_count(3)
    expect(crumbs.nth(1)).to_have_text("categoryB")
    expect(crumbs.nth(2)).to_have_text("grainB1")
    expect(crumbs.nth(2).locator('span.material-icons')).to_have_class(ACTIVE_CLASS)

    # Now restore full path to Projects > B > B1
    widget.path = (0, 0, 0)

    wait_until(lambda: widget.active == (0,), page)
    wait_until(lambda: widget.path == (0, 0, 0), page)

    expect(crumbs.nth(1)).to_have_text("categoryA")
    expect(crumbs.nth(2)).to_have_text("grainA1")
