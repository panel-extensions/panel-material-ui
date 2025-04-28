import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.widgets import Button
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Tabs
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

    # Check initial content
    content = page.locator('.MuiTabPanel-root')
    expect(content).to_contain_text('Content 1')

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
    expect(tabs.nth(1)).to_have_class('Mui-selected')
    expect(page.locator('.MuiTabPanel-root')).to_contain_text('Content 2')
    assert widget.active == 1

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
    tab = page.locator('.MuiTab-root').nth(1)
    expect(tab).to_have_class('Mui-disabled')

    # Try clicking disabled tab (should not change)
    tab.click()
    expect(page.locator('.MuiTabPanel-root')).to_contain_text('Content 1')
    assert widget.active == 0

def test_tabs_full_width(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1),
        ("Tab 2", content2),
        stretch=True
    )
    serve_component(page, widget)

    tabs = page.locator('.MuiTab-root')
    expect(tabs.nth(0)).to_have_class('MuiTab-fullWidth')
    expect(tabs.nth(1)).to_have_class('MuiTab-fullWidth')

def test_tabs_nested_components(page):
    button = Button(name="Click Me")
    widget = Tabs(
        ("Tab 1", button)
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.locator('button').click()
    assert button.clicks == 1

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

def test_tabs_text_color(page):
    content1 = Column("Content 1")
    widget = Tabs(
        ("Tab 1", content1),
        text_color='primary'
    )
    serve_component(page, widget)

    tab = page.locator('.MuiTab-root')
    expect(tab).to_have_class('MuiTab-textColorPrimary')

def test_tabs_wrapped_text(page):
    content1 = Column("Content 1")
    widget = Tabs(
        ("Very Long Tab Name That Should Wrap", content1),
        wrapped=True
    )
    serve_component(page, widget)

    tab = page.locator('.MuiTab-root')
    expect(tab).to_have_class('MuiTab-wrapped')

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
    tabs = page.locator('.MuiTab-root')
    expect(tabs.nth(1)).to_have_class('Mui-selected')
    expect(page.locator('.MuiTabPanel-root')).to_contain_text('Content 2')

def test_tabs_vertical(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Tabs(
        ("Tab 1", content1),
        ("Tab 2", content2),
        orientation='vertical'
    )
    serve_component(page, widget)

    # Check vertical orientation
    tabs_list = page.locator('.MuiTabs-vertical')
    expect(tabs_list).to_have_count(1)
