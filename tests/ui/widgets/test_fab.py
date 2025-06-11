import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Fab
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_fab_basic_functionality(page):
    widget = Fab(icon='add')
    serve_component(page, widget)

    # Initial state
    expect(page.locator('.MuiFab-root')).to_have_count(1)
    expect(page.locator('.material-icons')).to_have_text('add')

def test_fab_extended_variant(page):
    label = 'Add Item'
    widget = Fab(icon='add', label=label, variant='extended')
    serve_component(page, widget)

    # Verify extended variant
    expect(page.locator('.MuiFab-root')).to_have_text(f"add{label}")
    expect(page.locator('.material-icons')).to_have_text('add')

@pytest.mark.parametrize('size', ['small', 'medium', 'large'])
def test_fab_sizes(page, size):
    widget = Fab(icon='add', size=size)
    serve_component(page, widget)

    expect(page.locator('.MuiFab-root')).to_have_count(1)
    expect(page.locator(f'.MuiFab-size{size.capitalize()}')).to_have_count(1)

@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_fab_colors(page, color):
    widget = Fab(icon='add', color=color)
    serve_component(page, widget)

    expect(page.locator('.MuiFab-root')).to_have_count(1)
    if color == 'error':
        css_class = 'Mui-error'
    else:
        css_class = f'MuiFab-{color}'
    expect(page.locator(f'.{css_class}')).to_have_count(1)

def test_fab_disabled_state(page):
    widget = Fab(icon='add', disabled=True)
    serve_component(page, widget)

    # Verify disabled state
    expect(page.locator('.MuiFab-root')).to_have_count(1)
    expect(page.locator('.MuiFab-root.Mui-disabled')).to_have_count(1)

def test_fab_click_handling(page):
    widget = Fab(icon='add')
    serve_component(page, widget)

    # Initial state
    assert widget.clicks == 0

    # Click the button
    page.locator('.MuiFab-root').click()
    wait_until(lambda: widget.clicks == 1, page)

def test_fab_click_callback(page):
    events = []
    def cb(event):
        events.append(event)

    widget = Fab(icon='add', on_click=cb)
    serve_component(page, widget)

    # Click the button
    page.locator('.MuiFab-root').click()
    wait_until(lambda: len(events) == 1, page)

def test_fab_custom_icon(page):
    # Test with a custom SVG icon
    svg_icon = '<svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>'
    widget = Fab(icon=svg_icon)
    serve_component(page, widget)

    # Verify custom icon is displayed
    expect(page.locator('.MuiFab-root')).to_have_count(1)
    expect(page.locator('.MuiFab-root span')).to_have_css('mask-image', 'url("data:image/svg+xml;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQgMjQiPjxwYXRoIGQ9Ik0xOSAxM2gtNnY2aC0ydi02SDV2LTJoNlY1aDJ2Nmg2djJ6Ii8+PC9zdmc+")')

def test_fab_href(page):
    widget = Fab(icon='add', href='https://example.com', target='_blank')
    serve_component(page, widget)

    # Verify href and target attributes
    expect(page.locator('.MuiFab-root')).to_have_attribute('href', 'https://example.com')
    expect(page.locator('.MuiFab-root')).to_have_attribute('target', '_blank')

def test_fab_icon_size(page):
    widget = Fab(icon='add', icon_size='2em')
    serve_component(page, widget)

    # Verify icon size
    expect(page.locator('.MuiFab-root')).to_have_count(1)
    expect(page.locator('.material-icons')).to_have_css('font-size', '28px')
