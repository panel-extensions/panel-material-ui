import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Paper
from panel_material_ui.widgets import Button
from panel_material_ui.wrappers import Clickable
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_clickable_basic(page):
    widget = Clickable(Paper(height=60, width=100))
    serve_component(page, widget)

    expect(page.locator('.MuiButtonBase-root')).to_have_count(1)


def test_clickable_click_increments(page):
    widget = Clickable(Paper(height=60, width=100))
    serve_component(page, widget)

    page.locator('.MuiButtonBase-root').click()
    wait_until(lambda: widget.clicks == 1, page)

    page.locator('.MuiButtonBase-root').click()
    wait_until(lambda: widget.clicks == 2, page)


def test_clickable_on_click_callback(page):
    events = []
    widget = Clickable(Paper(height=60, width=100), on_click=lambda e: events.append(e))
    serve_component(page, widget)

    page.locator('.MuiButtonBase-root').click()
    wait_until(lambda: len(events) == 1, page)


def test_clickable_disabled(page):
    widget = Clickable(Paper(height=60, width=100), disabled=True)
    serve_component(page, widget)

    button = page.locator('.MuiButtonBase-root')
    expect(button).to_be_disabled()

    button.click(force=True)
    page.wait_for_timeout(200)
    assert widget.clicks == 0


def test_clickable_disable_ripple(page):
    widget = Clickable(Paper(height=60, width=100), disable_ripple=True)
    serve_component(page, widget)

    expect(page.locator('.MuiButtonBase-root')).to_have_count(1)
    page.locator('.MuiButtonBase-root').click()
    wait_until(lambda: widget.clicks == 1, page)


def test_clickable_dynamic_child(page):
    paper = Paper(height=60, width=100)
    widget = Clickable(paper)
    serve_component(page, widget)

    expect(page.locator('.MuiPaper-root')).to_have_count(1)

    widget.object = Button(label="Hello")
    expect(page.locator('.MuiButton-root')).to_have_count(1)


def test_clickable_fills_responsive_child(page):
    widget = Clickable(
        Paper(sizing_mode="stretch_width", height=60),
        sizing_mode="stretch_width",
    )
    serve_component(page, widget)

    button_base = page.locator('.MuiButtonBase-root')
    expect(button_base).to_have_count(1)
    page_width = page.evaluate("() => document.body.clientWidth")
    wait_until(
        lambda: button_base.bounding_box()["width"] > page_width * 0.8, page
    )
