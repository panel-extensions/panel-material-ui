import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Chip
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_chip_basic(page):
    widget = Chip(label="Hello")
    serve_component(page, widget)
    expect(page.locator('.MuiChip-root')).to_have_count(1)
    expect(page.locator('.MuiChip-label')).to_have_text("Hello")


@pytest.mark.parametrize('variant', ['filled', 'outlined'])
def test_chip_variant(page, variant):
    widget = Chip(label="Test", variant=variant)
    serve_component(page, widget)
    expect(page.locator(f'.MuiChip-{variant}')).to_have_count(1)


@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'success', 'warning', 'info'])
def test_chip_color(page, color):
    widget = Chip(label="Test", color=color)
    serve_component(page, widget)
    expect(page.locator(f'.MuiChip-color{color.capitalize()}')).to_have_count(1)


@pytest.mark.parametrize('size', ['small', 'medium'])
def test_chip_size(page, size):
    widget = Chip(label="Test", size=size)
    serve_component(page, widget)
    expect(page.locator(f'.MuiChip-size{size.capitalize()}')).to_have_count(1)


def test_chip_disabled(page):
    widget = Chip(label="Disabled", disabled=True)
    serve_component(page, widget)
    expect(page.locator('.MuiChip-root.Mui-disabled')).to_have_count(1)


def test_chip_on_click(page):
    events = []
    def cb(event):
        events.append(event)

    widget = Chip(label="Click me", on_click=cb)
    serve_component(page, widget)
    page.locator('.MuiChip-root').click()
    wait_until(lambda: len(events) == 1, page)


def test_chip_clicks(page):
    widget = Chip(label="Click me")
    serve_component(page, widget)
    page.locator('.MuiChip-root').click()
    wait_until(lambda: widget.clicks == 1, page)


def test_chip_label_update(page):
    widget = Chip(label="Before")
    serve_component(page, widget)
    expect(page.locator('.MuiChip-label')).to_have_text("Before")
    widget.label = "After"
    expect(page.locator('.MuiChip-label')).to_have_text("After")


def test_chip_icon(page):
    widget = Chip(label="Star", icon="star")
    serve_component(page, widget)
    expect(page.locator('.MuiChip-icon')).to_have_count(1)
