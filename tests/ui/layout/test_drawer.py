import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Column, Drawer, Row
from panel_material_ui.widgets import Button

pytestmark = pytest.mark.ui


def test_drawer_basic(page):
    content = Column("Drawer Content")
    widget = Drawer(objects=[content])
    serve_component(page, widget)

    # Initially drawer should not be visible (default open=False)
    drawer = page.locator('.MuiDrawer-root')
    expect(drawer).to_have_count(0)

    # Open drawer
    widget.open = True
    drawer = page.locator('.MuiDrawer-root')
    expect(drawer).to_have_count(1)
    expect(drawer).to_contain_text("Drawer Content")

def test_drawer_close(page):
    content = Column("Drawer Content")
    widget = Drawer(objects=[content], open=True)
    serve_component(page, widget)

    # Click backdrop to close
    page.locator('.MuiBackdrop-root').click()

    # Drawer should be closed
    drawer = page.locator('.MuiDrawer-root')
    expect(drawer).to_have_count(0)
    assert widget.open == False  # noqa

@pytest.mark.parametrize('anchor', ['left', 'right', 'top', 'bottom'])
def test_drawer_anchor(page, anchor):
    content = Column("Drawer Content")
    widget = Drawer(objects=[content], open=True, anchor=anchor)
    serve_component(page, widget)

    expect(page.locator(f'.MuiDrawer-anchor{anchor.capitalize()}')).to_have_count(1)

def test_drawer_size(page):
    content = Column("Drawer Content")
    widget = Drawer(objects=[content], open=True, size=300)
    serve_component(page, widget)

    drawer_paper = page.locator('.MuiDrawer-paper')
    # Left drawer (default) should have width set to size
    expect(drawer_paper).to_have_css('width', '300px')

def test_drawer_vertical_size(page):
    content = Column("Drawer Content")
    widget = Drawer(objects=[content], open=True, size=300, anchor='top')
    serve_component(page, widget)

    drawer_paper = page.locator('.MuiDrawer-paper')
    # Top drawer should have height set to size
    expect(drawer_paper).to_have_css('height', '300px')

def test_drawer_with_button_interaction(page):
    button = Button(label="Click Me")
    widget = Drawer(objects=[button], open=True)
    serve_component(page, widget)

    # Button should be clickable inside drawer
    drawer_button = page.locator('.MuiDrawer-paper button')
    drawer_button.click()
    wait_until(lambda: button.clicks == 1, page)

def test_drawer_multiple_objects(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Drawer(objects=[content1, content2], open=True)
    serve_component(page, widget)

    drawer = page.locator('.MuiDrawer-paper')
    expect(drawer).to_contain_text("Content 1")
    expect(drawer).to_contain_text("Content 2")


def test_drawer_transition_callback_and_resize(page):
    events = []
    widget = Drawer("Content", variant="persistent", inline=True)
    widget.on_transition(events.append)
    serve_component(page, Row(widget, Column("Main")))
    page.evaluate("window.__resizes = 0; window.addEventListener('resize', () => window.__resizes++)")

    widget.open = True
    wait_until(lambda: events == [True], page)
    assert page.evaluate("window.__resizes") >= 1

    widget.open = False
    wait_until(lambda: events == [True, False], page)


def test_drawer_resize_on_toggle_disabled(page):
    events = []
    widget = Drawer("Content", variant="persistent", inline=True, resize_on_toggle=False)
    widget.on_transition(events.append)
    serve_component(page, Row(widget, Column("Main")))
    page.evaluate("window.__resizes = 0; window.addEventListener('resize', () => window.__resizes++)")

    widget.open = True
    wait_until(lambda: events == [True], page)
    assert page.evaluate("window.__resizes") == 0
