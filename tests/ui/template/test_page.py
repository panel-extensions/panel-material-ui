import time

import pytest

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component
from playwright.sync_api import expect
from panel_material_ui.template import Page
from panel_material_ui.widgets import Button

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


def test_page_main_width_default_unclamped(page):
    """By default the main content area is not clamped (no max-width)."""
    pg = Page(main=[pn.pane.Markdown("# Content")])

    serve_component(page, pg)

    main_content = page.locator(".main-content")
    expect(main_content).to_be_attached()
    expect(main_content).to_have_css("max-width", "none")


def test_page_main_width_custom(page):
    """main_width clamps and centers the main content area."""
    pg = Page(main=[pn.pane.Markdown("# Content")], main_width=800)

    serve_component(page, pg)

    main_content = page.locator(".main-content")
    expect(main_content).to_have_css("max-width", "800px")
    # Centered via alignSelf in the column flex parent (margin:auto would
    # compute to resolved pixels, so we assert on align-self instead).
    expect(main_content).to_have_css("align-self", "center")


def test_page_app_bar_width_default_unclamped(page):
    """By default the app bar toolbar is not clamped (no max-width)."""
    pg = Page(main=[pn.pane.Markdown("# Content")])

    serve_component(page, pg)

    toolbar = page.locator(".header .MuiToolbar-root")
    expect(toolbar).to_have_css("max-width", "none")


def test_page_app_bar_width_custom(page):
    """app_bar_width clamps and centers the app bar toolbar content."""
    pg = Page(main=[pn.pane.Markdown("# Content")], app_bar_width=900)

    serve_component(page, pg)

    toolbar = page.locator(".header .MuiToolbar-root")
    expect(toolbar).to_have_css("max-width", "900px")
    expect(toolbar).to_have_css("align-self", "center")


def test_page_main_width_css_string(page):
    """main_width accepts a CSS length string (resolved by the browser)."""
    # 60rem resolves to 960px at the default 16px root font size.
    pg = Page(main=[pn.pane.Markdown("# Content")], main_width="60rem")

    serve_component(page, pg)

    main_content = page.locator(".main-content")
    expect(main_content).to_have_css("max-width", "960px")
    expect(main_content).to_have_css("align-self", "center")


def test_page_main_width_breakpoint_dict(page):
    """main_width accepts a breakpoint dict, applying per-breakpoint clamps."""
    pg = Page(main=[pn.pane.Markdown("# Content")], main_width={"xs": "100%", "md": 800})

    serve_component(page, pg)

    main_content = page.locator(".main-content")
    # At/above the md breakpoint the 800px clamp applies.
    page.set_viewport_size({"width": 1200, "height": 800})
    expect(main_content).to_have_css("max-width", "800px")
    # Below md the clamp falls back to the xs entry (100%), i.e. not 800px.
    page.set_viewport_size({"width": 500, "height": 800})
    expect(main_content).not_to_have_css("max-width", "800px")


def test_page_app_bar_width_follows_main_width(page):
    """When app_bar_width is unset, the toolbar follows main_width so the
    header stays aligned with the clamped main content."""
    pg = Page(main=[pn.pane.Markdown("# Content")], main_width=800)

    serve_component(page, pg)

    toolbar = page.locator(".header .MuiToolbar-root")
    expect(toolbar).to_have_css("max-width", "800px")
    expect(toolbar).to_have_css("align-self", "center")


def test_page_app_bar_width_overrides_main_width(page):
    """An explicit app_bar_width takes precedence over main_width for the toolbar."""
    pg = Page(main=[pn.pane.Markdown("# Content")], main_width=800, app_bar_width=1200)

    serve_component(page, pg)

    toolbar = page.locator(".header .MuiToolbar-root")
    expect(toolbar).to_have_css("max-width", "1200px")
    main_content = page.locator(".main-content")
    expect(main_content).to_have_css("max-width", "800px")


def test_page_linear_progress_hidden_when_idle(page):
    """Test that linear progress bar is hidden (opacity: 0) when not busy."""
    pg = Page(
        busy_indicator='linear',
        main=[pn.pane.Markdown("# Content")]
    )

    serve_component(page, pg)

    # Wait for page to load
    page.wait_for_timeout(500)

    # Find the LinearProgress component
    progress = page.locator(".MuiLinearProgress-root")

    # Progress should exist in the DOM
    expect(progress).to_be_attached()

    # Progress should be hidden (opacity: 0) when idle
    expect(progress).to_have_css("opacity", "0")


def test_page_linear_progress_visible_when_busy(page):
    """Test that linear progress bar is visible (opacity: 1) when busy."""
    def slow_operation(event):
        time.sleep(2)

    button = Button(label='Trigger Busy', on_click=slow_operation)

    pg = Page(
        busy_indicator='linear',
        main=[button]
    )

    serve_component(page, pg)

    # Find the progress bar
    progress = page.locator(".MuiLinearProgress-root")

    # Initially should be hidden
    expect(progress).to_have_css("opacity", "0")

    # Click button to trigger busy state
    page.locator('.MuiButton-root').click()

    # Wait a bit for the busy state to activate (1 second debounce)
    page.wait_for_timeout(1100)

    # Progress bar should now be visible
    expect(progress).to_have_css("opacity", "1")
