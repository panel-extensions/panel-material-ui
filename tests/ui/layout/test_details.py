import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.widgets import Button
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Details
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

def test_details_default(page):
    """Test that Details defaults to collapsed state."""
    layout = Details(1, 2, 3, title="Details 1")
    serve_component(page, layout)

    # Content should be collapsed by default
    content = page.locator('.MuiCollapse-root')
    expect(content).not_to_be_visible()

def test_details_basic(page):
    """Test basic Details structure."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content]
    )
    serve_component(page, widget)

    # Check that Details container exists
    container = page.locator('.details').first
    expect(container).to_be_visible()

    # Check header
    header = page.locator('.details-header').first
    expect(header).to_contain_text("Test Details")

def test_details_hide_header(page):
    """Test Details with hidden header."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        hide_header=True
    )
    serve_component(page, widget)

    # Header should not exist
    header = page.locator('.details-header')
    expect(header).to_have_count(0)

def test_details_collapse_expand(page):
    """Test Details collapse and expand functionality."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        collapsed=True
    )
    serve_component(page, widget)

    # Initially collapsed
    content_area = page.locator('.MuiCollapse-root')
    expect(content_area).not_to_be_visible()

    # Click on header to expand (header is clickable, not a button)
    header = page.locator('.details-header').first
    expect(header).to_be_visible()
    header.click()

    # Content should now be visible
    expect(content_area).to_be_visible()
    wait_until(lambda: not widget.collapsed, page)

    # Click header to collapse again
    header.click()
    expect(content_area).not_to_be_visible()
    wait_until(lambda: widget.collapsed, page)

def test_details_three_states(page):
    """Test Details three expansion states: collapsed, expanded (scrollable), fully expanded."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        collapsed=True
    )
    serve_component(page, widget)

    # State 1: Collapsed
    content_area = page.locator('.MuiCollapse-root')
    expect(content_area).not_to_be_visible()

    # Expand to state 2: Expanded with scrollable area
    header = page.locator('.details-header').first
    header.click()
    wait_until(lambda: not widget.collapsed, page)
    expect(content_area).to_be_visible()

    # Check for expand full button
    expand_full_button = page.locator('button[aria-label="expand fully"]')
    expect(expand_full_button).to_have_count(1)

    # Expand to state 3: Fully expanded
    expand_full_button.click()
    wait_until(lambda: widget.fully_expanded, page)

    # Check for collapse to scrollable button
    collapse_button = page.locator('button[aria-label="collapse to scrollable"]')
    expect(collapse_button).to_have_count(1)

    # Collapse back to scrollable
    collapse_button.click()
    wait_until(lambda: not widget.fully_expanded, page)

def test_details_custom_header(page):
    """Test Details with custom header component."""
    header = Button(name="Custom Header")
    content = Column("Details Content")
    widget = Details(
        header=header,
        objects=[content]
    )
    serve_component(page, widget)

    # Check custom header is rendered
    header_content = page.locator('.details-header').first
    expect(header_content).to_contain_text("Custom Header")

def test_details_nested_components(page):
    """Test Details with nested interactive components."""
    button = Button(name="Click Me")
    widget = Details(
        title="Test Details",
        objects=[button],
        collapsed=False
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.locator('.bk-btn').click()
    wait_until(lambda: button.clicks == 1, page)

def test_details_square(page):
    """Test Details with square variant."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        square=True
    )
    serve_component(page, widget)

    # Check if square removes border-radius (Details uses Box, not Paper)
    container = page.locator('.details').first
    expect(container).to_have_css('border-radius', '0px')

def test_details_elevation(page):
    """Test Details with custom elevation."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        elevation=5
    )
    serve_component(page, widget)

    # Details uses Box, not Paper, so elevation prop may not be visually applied
    # Just verify the component renders without error
    container = page.locator('.details').first
    expect(container).to_be_visible()

def test_details_header_styling(page):
    """Test Details header styling."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        header_background="#0000ff",
        header_color="#ffffff"
    )
    serve_component(page, widget)

    header = page.locator('.details-header').first
    expect(header).to_have_css('background-color', 'rgb(0, 0, 255)')
    expect(header).to_have_css('color', 'rgb(255, 255, 255)')

def test_details_multiple_objects(page):
    """Test Details with multiple objects."""
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Details(
        title="Test Details",
        objects=[content1, content2],
        collapsed=False
    )
    serve_component(page, widget)

    content = page.locator('.MuiCollapse-root')
    expect(content).to_contain_text("Content 1")
    expect(content).to_contain_text("Content 2")

def test_details_scrollable_height(page):
    """Test Details with custom scrollable_height."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        collapsed=False,
        fully_expanded=False,
        scrollable_height=42
    )
    serve_component(page, widget)

    # Check that max-height is applied to content area
    content_area = page.locator('.details-content').first
    expect(content_area).to_have_css('max-height', '42px')

def test_details_collapse_resets_fully_expanded(page):
    """Test that collapsing Details resets fully_expanded state."""
    content = Column("Details Content")
    widget = Details(
        title="Test Details",
        objects=[content],
        collapsed=False,
        fully_expanded=True
    )
    serve_component(page, widget)

    # Verify fully expanded
    wait_until(lambda: widget.fully_expanded, page)

    # Collapse
    header = page.locator('.details-header').first
    header.click()
    wait_until(lambda: widget.collapsed, page)

    # fully_expanded should be reset
    wait_until(lambda: not widget.fully_expanded, page)
