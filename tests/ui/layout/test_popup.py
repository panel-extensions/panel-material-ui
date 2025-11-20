import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.widgets import Button
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Popup
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

def test_popup_basic(page):
    content = Column("Popup Content")
    widget = Popup(
        objects=[content],
        open=True
    )
    serve_component(page, widget)

    # Check popup structure
    popup = page.locator('.MuiPopover-root')
    expect(popup).to_have_count(1)

    # Check content
    content = page.locator('.MuiPaper-root')
    expect(content).to_contain_text("Popup Content")

def test_popup_visibility(page):
    content = Column("Popup Content")
    widget = Popup(
        objects=[content],
        open=False
    )
    serve_component(page, widget)

    # Initially not visible
    popup = page.locator('.MuiPopover-root')
    expect(popup).to_have_count(0)

    # Show popup
    widget.open = True
    expect(popup).to_have_count(1)

def test_popup_nested_components(page):
    button = Button(name="Click Me")
    widget = Popup(
        objects=[button],
        open=True
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.locator('button').click()
    wait_until(lambda: button.clicks == 1, page)

def test_popup_multiple_objects(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Popup(
        objects=[content1, content2],
        open=True
    )
    serve_component(page, widget)

    content = page.locator('.MuiPaper-root')
    expect(content).to_contain_text("Content 1")
    expect(content).to_contain_text("Content 2")
