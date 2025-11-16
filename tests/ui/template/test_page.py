import pytest

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component
from playwright.sync_api import expect

from panel_material_ui.template import Page

pytestmark = pytest.mark.ui


def test_page_theme_config_header_color(page):
    pg = Page()

    serve_component(page, pg)

    header = page.locator(".MuiAppBar-root")
    expect(header).to_have_css("background-color", "rgb(0, 114, 181)")

    pg.theme_config = {
        "palette": {
            "primary": {
                "main": "#000000"
            }
        }
    }
    expect(header).to_have_css("background-color", "rgb(0, 0, 0)")


def test_page_sidebar_resizable_handle_present(page):
    """Test that the resize handle is present when sidebar has content."""
    pg = Page(sidebar=[pn.pane.Markdown("# Sidebar Content")])

    serve_component(page, pg)

    # Check that sidebar is present
    sidebar = page.locator(".sidebar")
    expect(sidebar).to_be_visible()

    # Check that resize handle is present
    resize_handle = page.locator('[aria-label="Resize sidebar"]')
    expect(resize_handle).to_be_visible()
    expect(resize_handle).to_have_attribute("title", "Drag to resize sidebar")


def test_page_sidebar_default_width(page):
    """Test that sidebar has the default width of 320px."""
    pg = Page(sidebar=[pn.pane.Markdown("# Sidebar Content")])

    serve_component(page, pg)

    sidebar_paper = page.locator(".MuiDrawer-paper.sidebar")
    expect(sidebar_paper).to_have_css("width", "320px")


def test_page_sidebar_custom_width(page):
    """Test that sidebar respects custom width setting."""
    pg = Page(
        sidebar=[pn.pane.Markdown("# Sidebar Content")],
        sidebar_width=400
    )

    serve_component(page, pg)

    sidebar_paper = page.locator(".MuiDrawer-paper.sidebar")
    expect(sidebar_paper).to_have_css("width", "400px")


def test_page_sidebar_resize_drag(page):
    """Test that dragging the resize handle changes sidebar width."""
    pg = Page(sidebar=[pn.pane.Markdown("# Sidebar Content")])

    serve_component(page, pg)

    # Get initial sidebar width
    sidebar_paper = page.locator(".MuiDrawer-paper.sidebar")
    expect(sidebar_paper).to_have_css("width", "320px")

    # Get resize handle
    resize_handle = page.locator('[aria-label="Resize sidebar"]')
    expect(resize_handle).to_be_visible()

    # Get the bounding box for drag calculation
    handle_box = resize_handle.bounding_box()
    assert handle_box is not None

    # Drag the handle to the right to increase width
    page.mouse.move(handle_box["x"] + handle_box["width"] / 2, handle_box["y"] + handle_box["height"] / 2)
    page.mouse.down()
    page.mouse.move(handle_box["x"] + 100, handle_box["y"] + handle_box["height"] / 2)
    page.mouse.up()

    # Wait for the change to be applied
    page.wait_for_timeout(100)

    # Check that the width has increased (should be around 420px)
    # Using a range check since exact pixel values can vary
    assert pg.sidebar_width > 380, f"Expected sidebar_width > 380, got {pg.sidebar_width}"
    assert pg.sidebar_width < 440, f"Expected sidebar_width < 440, got {pg.sidebar_width}"


def test_page_sidebar_collapse_on_small_drag(page):
    """Test that dragging sidebar to very small width collapses it."""
    pg = Page(
        sidebar=[pn.pane.Markdown("# Sidebar Content")],
        sidebar_width=200  # Start with smaller width for easier testing
    )

    serve_component(page, pg)

    # Verify sidebar is initially open
    assert pg.sidebar_open is True
    sidebar_paper = page.locator(".MuiDrawer-paper.sidebar")
    expect(sidebar_paper).to_be_visible()

    # Get resize handle
    resize_handle = page.locator('[aria-label="Resize sidebar"]')
    expect(resize_handle).to_be_visible()

    # Get the bounding box for drag calculation
    handle_box = resize_handle.bounding_box()
    assert handle_box is not None

    # Drag the handle far to the left to trigger collapse (more than 150px to get below 50px threshold)
    page.mouse.move(handle_box["x"] + handle_box["width"] / 2, handle_box["y"] + handle_box["height"] / 2)
    page.mouse.down()
    page.mouse.move(handle_box["x"] - 180, handle_box["y"] + handle_box["height"] / 2)
    page.mouse.up()

    # Wait for the change to be applied
    page.wait_for_timeout(200)

    # Check that sidebar is now collapsed
    assert pg.sidebar_open is False, "Sidebar should be collapsed when dragged to small width"


def test_page_sidebar_no_handle_when_empty(page):
    """Test that no resize handle is present when sidebar is empty."""
    pg = Page()  # No sidebar content

    serve_component(page, pg)

    # Check that resize handle is not present
    resize_handle = page.locator('[aria-label="Resize sidebar"]')
    expect(resize_handle).not_to_be_visible()


def test_page_sidebar_handle_styling(page):
    """Test that the resize handle has proper styling and hover effects."""
    pg = Page(sidebar=[pn.pane.Markdown("# Sidebar Content")])

    serve_component(page, pg)

    resize_handle = page.locator('[aria-label="Resize sidebar"]')
    expect(resize_handle).to_be_visible()

    # Check that handle has col-resize cursor
    expect(resize_handle).to_have_css("cursor", "col-resize")

    # Check that handle is positioned at the right edge
    expect(resize_handle).to_have_css("position", "absolute")
    expect(resize_handle).to_have_css("right", "0px")
    expect(resize_handle).to_have_css("top", "0px")


def test_page_sidebar_width_persistence(page):
    """Test that sidebar width changes are reflected in the model."""
    pg = Page(sidebar=[pn.pane.Markdown("# Sidebar Content")])

    serve_component(page, pg)

    # Get initial width from model
    initial_width = pg.sidebar_width
    assert initial_width == 320

    # Simulate a programmatic width change
    pg.sidebar_width = 450

    # Wait for change to be applied
    page.wait_for_timeout(100)

    # Check that the CSS reflects the new width
    sidebar_paper = page.locator(".MuiDrawer-paper.sidebar")
    expect(sidebar_paper).to_have_css("width", "450px")
