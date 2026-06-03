import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Button
from panel_material_ui.layout import Tabs
from panel_material_ui.pane import Typography
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_tabs(page):
    layout = Tabs(("Tab 1", "Tab 1 objects"), ("Tab 2", "Card 2 objects"))
    serve_component(page, layout)

    expect(page.locator('.tabs')).to_have_count(1)
    expect(page.locator('.MuiTab-root')).to_have_count(2)

def test_tabs_basic(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1),
        ("Tab 2", content2)
    )
    serve_component(page, widget)

    # Check tabs structure
    tabs = page.locator('.MuiTab-root')
    expect(tabs).to_have_count(2)
    expect(tabs.nth(0)).to_contain_text('Tab 1')
    expect(tabs.nth(1)).to_contain_text('Tab 2')

def test_tabs_component_title(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        (Typography("Tab 1"), content1),
        (Typography("Tab 2"), content2)
    )
    serve_component(page, widget)

    # Check tabs structure
    tabs = page.locator('.MuiTab-root')
    expect(tabs).to_have_count(2)
    expect(tabs.nth(0)).to_contain_text('Tab 1')
    expect(tabs.nth(1)).to_contain_text('Tab 2')

def test_tabs_selection(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1),
        ("Tab 2", content2)
    )
    serve_component(page, widget)

    # Click second tab
    tabs = page.locator('.MuiTab-root')
    tabs.nth(1).click()

    # Check active state
    expect(page.locator('.Mui-selected')).to_contain_text('Tab 2')
    expect(page.locator('.MuiTabsPanel')).to_contain_text('Content 2')
    wait_until(lambda: widget.active == 1, page)

def test_tabs_disabled(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1),
        ("Tab 2", content2),
        disabled=[1]  # Disable second tab
    )
    serve_component(page, widget)

    # Check disabled state
    disabled_tab = page.locator('.Mui-disabled')
    expect(disabled_tab).to_contain_text('Tab 2')

    # Try clicking disabled tab (should not change)
    disabled_tab.click(force=True)
    expect(page.locator('.MuiTabsPanel')).to_contain_text('Content 1')
    wait_until(lambda: widget.active == 0, page)

def test_tabs_nested_components(page):
    button = Button(label="Click Me")
    widget = Tabs(
        ("Tab 1", button)
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.locator('.MuiButton-root').click()
    wait_until(lambda: button.clicks == 1, page)

def test_tabs_dynamic_update(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1)
    )
    serve_component(page, widget)

    # Initially one tab
    expect(page.locator('.MuiTab-root')).to_have_count(1)

    # Add another tab
    widget.objects = [('Tab 1', content1), ('Tab 2', content2)]
    expect(page.locator('.MuiTab-root')).to_have_count(2)

def test_tabs_color(page):
    content1 = Column("Content 1")
    widget = Tabs(
        ("Tab 1", content1),
        color='primary'
    )
    serve_component(page, widget)

    expect(page.locator('.MuiTab-textColorPrimary')).to_have_count(1)

def test_tabs_wrapped_text(page):
    content1 = Column("Content 1")
    widget = Tabs(
        ("Very Long Tab Name That Should Wrap", content1),
        wrapped=True
    )
    serve_component(page, widget)

    expect(page.locator('.MuiTab-wrapped')).to_have_count(1)

def test_tabs_initial_active(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1),
        ("Tab 2", content2),
        active=1  # Start with second tab active
    )
    serve_component(page, widget)

    # Check initial active state
    expect(page.locator('.MuiTabsPanel')).to_contain_text('Content 2')

def test_tabs_vertical(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1),
        ("Tab 2", content2),
        tabs_location='right'
    )
    serve_component(page, widget)

    # Check vertical orientation
    tabs_list = page.locator('.MuiTabs-root.MuiTabs-vertical')
    expect(tabs_list).to_have_count(1)


def test_tabs_closable_active_last(page):
    widget = Tabs(
        ("Tab 1", "Content 1"),
        ("Tab 2", "Content 2"),
        ("Tab 3", "Content 3"),
        closable=True,
        active=2
    )
    serve_component(page, widget)

    expect(page.locator('.MuiTab-root')).to_have_count(3)

    # Close the active (last) tab
    close_buttons = page.locator('.MuiTab-root >> nth=2 >> span:has-text("✕")')
    close_buttons.click()

    # Tab should be removed and previous tab becomes active
    expect(page.locator('.MuiTab-root')).to_have_count(2)
    wait_until(lambda: len(widget.objects) == 2, page)
    wait_until(lambda: widget.active == 1, page)
    expect(page.locator('.MuiTabsPanel')).to_contain_text('Content 2')


def test_tabs_closable_middle(page):
    widget = Tabs(
        ("Tab 1", "Content 1"),
        ("Tab 2", "Content 2"),
        ("Tab 3", "Content 3"),
        closable=True,
        active=2
    )
    serve_component(page, widget)

    # Close a tab before the active one
    close_buttons = page.locator('.MuiTab-root >> nth=0 >> span:has-text("✕")')
    close_buttons.click()

    # Active index should shift down to keep the same content visible
    expect(page.locator('.MuiTab-root')).to_have_count(2)
    wait_until(lambda: len(widget.objects) == 2, page)
    wait_until(lambda: widget.active == 1, page)
    expect(page.locator('.MuiTabsPanel')).to_contain_text('Content 3')


def test_tabs_closable_inactive(page):
    widget = Tabs(
        ("Tab 1", "Content 1"),
        ("Tab 2", "Content 2"),
        ("Tab 3", "Content 3"),
        closable=True,
        active=0
    )
    serve_component(page, widget)

    # Close a tab after the active one
    close_buttons = page.locator('.MuiTab-root >> nth=2 >> span:has-text("✕")')
    close_buttons.click()

    # Active index should remain unchanged
    expect(page.locator('.MuiTab-root')).to_have_count(2)
    wait_until(lambda: len(widget.objects) == 2, page)
    wait_until(lambda: widget.active == 0, page)
    expect(page.locator('.MuiTabsPanel')).to_contain_text('Content 1')
