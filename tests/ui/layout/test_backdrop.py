import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Backdrop, Column
from panel_material_ui.widgets import Button, LoadingSpinner
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

def test_backdrop_basic(page):
    content = LoadingSpinner()
    widget = Backdrop(
        objects=[content],
        open=True
    )
    serve_component(page, widget)

    # Check backdrop exists and is visible
    backdrop = page.locator('.MuiBackdrop-root')
    expect(backdrop).to_have_count(1)
    expect(backdrop).to_be_visible()

def test_backdrop_visibility(page):
    content = LoadingSpinner()
    widget = Backdrop(
        objects=[content],
        open=False
    )
    serve_component(page, widget)

    # Initially not visible
    backdrop = page.locator('.MuiBackdrop-root')
    expect(backdrop).not_to_be_visible()

    # Show backdrop
    widget.open = True
    expect(backdrop).to_be_visible()

    # Hide backdrop
    widget.open = False
    expect(backdrop).not_to_be_visible()

def test_backdrop_nested_components(page):
    button = Button(name="Click Me")
    widget = Backdrop(
        objects=[button],
        open=True
    )
    serve_component(page, widget)

    # Check if button is interactive while backdrop is shown
    page.locator('button').click()
    wait_until(lambda: button.clicks == 1, page)

def test_backdrop_multiple_objects(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Backdrop(
        objects=[content1, content2],
        open=True
    )
    serve_component(page, widget)

    backdrop = page.locator('.MuiBackdrop-root')
    expect(backdrop).to_contain_text("Content 1")
    expect(backdrop).to_contain_text("Content 2")

def test_backdrop_custom_styling(page):
    content = LoadingSpinner()
    widget = Backdrop(
        objects=[content],
        open=True,
        sx={'backgroundColor': 'rgb(0, 0, 255)'}
    )
    serve_component(page, widget)

    backdrop = page.locator('.MuiBackdrop-root')
    expect(backdrop).to_have_css('background-color', 'rgb(0, 0, 255)')

def test_backdrop_z_index(page):
    content = LoadingSpinner()
    widget = Backdrop(
        objects=[content],
        open=True
    )
    serve_component(page, widget)

    backdrop = page.locator('.MuiBackdrop-root')
    # Check if z-index is higher than drawer (default behavior)
    z_index = backdrop.evaluate('el => window.getComputedStyle(el).zIndex')
    wait_until(lambda: int(z_index) > 1200, page)  # MUI drawer zIndex is typically 1200

def test_backdrop_loading_indicator(page):
    progress = LoadingSpinner(color='primary')
    widget = Backdrop(
        objects=[progress],
        open=True
    )
    serve_component(page, widget)

    # Check if CircularProgress is rendered
    progress_indicator = page.locator('.MuiCircularProgress-root')
    expect(progress_indicator).to_have_count(1)
    expect(progress_indicator).to_be_visible()

def test_backdrop_click_through(page):
    # Test that elements behind backdrop are not clickable
    background_button = Button(name="Background Button")
    backdrop_content = LoadingSpinner()

    column = Column(
        background_button,
        Backdrop(objects=[backdrop_content], open=True)
    )
    serve_component(page, column)

    # Try to click button behind backdrop
    background_button_el = page.locator('button:text("Background Button")')
    background_button_el.click(force=True)  # force click through backdrop

    # Button should not register click due to backdrop
    wait_until(lambda: background_button.clicks == 0, page)
