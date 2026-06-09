import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Paper
from panel_material_ui.wrappers import Tooltip
from panel_material_ui.widgets import Button
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def _page_width(page):
    return page.evaluate("() => document.body.clientWidth")


def _width(locator):
    box = locator.bounding_box()
    return box["width"] if box else 0


def test_tooltip_basic(page):
    button = Button(label="Hover me")
    widget = Tooltip(button, title="Help text")
    serve_component(page, widget)

    expect(page.locator('.MuiButton-root')).to_have_count(1)


def test_tooltip_shows_on_hover(page):
    button = Button(label="Hover me")
    widget = Tooltip(button, title="Help text", enter_delay=0)
    serve_component(page, widget)

    page.locator('.MuiButton-root').hover()
    expect(page.locator('.MuiTooltip-tooltip')).to_be_visible()
    expect(page.locator('.MuiTooltip-tooltip')).to_contain_text('Help text')


def test_tooltip_arrow(page):
    button = Button(label="Hover me")
    widget = Tooltip(button, title="With arrow", arrow=True, enter_delay=0)
    serve_component(page, widget)

    page.locator('.MuiButton-root').hover()
    expect(page.locator('.MuiTooltip-arrow')).to_be_visible()


def test_tooltip_placement_top(page):
    button = Button(label="Hover me")
    widget = Tooltip(button, title="Top tooltip", placement="top", enter_delay=0, margin=(200, 0, 0, 0))
    serve_component(page, widget)

    page.locator('.MuiButton-root').hover()
    tooltip = page.locator('.MuiTooltip-popper')
    expect(tooltip).to_be_visible()
    expect(tooltip).to_have_attribute('data-popper-placement', 'top')


def test_tooltip_controlled_open(page):
    button = Button(label="Hover me")
    widget = Tooltip(button, title="Always open", open=True)
    serve_component(page, widget)

    expect(page.locator('.MuiTooltip-tooltip')).to_be_visible()


def test_tooltip_controlled_closed(page):
    button = Button(label="Hover me")
    widget = Tooltip(button, title="Always closed", open=False)
    serve_component(page, widget)

    page.locator('.MuiButton-root').hover()
    expect(page.locator('.MuiTooltip-tooltip')).not_to_be_visible()


def test_tooltip_title_update(page):
    button = Button(label="Hover me")
    widget = Tooltip(button, title="Original", enter_delay=0)
    serve_component(page, widget)

    page.locator('.MuiButton-root').hover()
    expect(page.locator('.MuiTooltip-tooltip')).to_contain_text('Original')

    page.mouse.move(0, 0)
    widget.title = "Updated"
    page.locator('.MuiButton-root').hover()
    expect(page.locator('.MuiTooltip-tooltip')).to_contain_text('Updated')


def test_tooltip_empty(page):
    widget = Tooltip(title="Empty tooltip")
    serve_component(page, widget)

    expect(page.locator('.MuiTooltip-tooltip')).not_to_be_visible()


def test_tooltip_fills_responsive_child(page):
    widget = Tooltip(
        Paper(sizing_mode="stretch_width", height=60),
        title="Help", sizing_mode="stretch_width",
    )
    serve_component(page, widget)

    paper = page.locator('.MuiPaper-root')
    expect(paper).to_have_count(1)
    wait_until(lambda: _width(paper) > _page_width(page) * 0.8, page)


def test_tooltip_hugs_fixed_child(page):
    widget = Tooltip(Button(label="Hi"), title="Help")
    serve_component(page, widget)

    button = page.locator('.MuiButton-root')
    expect(button).to_have_count(1)
    wait_until(lambda: 0 < _width(button) < _page_width(page) * 0.5, page)
