import re

import pytest

pytest.importorskip('playwright')

from panel_material_ui.layout import FloatPanel, Paper
from panel_material_ui.widgets import Button

from playwright.sync_api import expect
from panel.tests.util import serve_component, wait_until

pytestmark = pytest.mark.ui

def test_paper(page):
    layout = Paper(name="Paper", objects=[1, 2, 3])
    serve_component(page, layout)
    expect(page.locator('.paper')).to_have_count(1)


def test_float_panel_drag_and_content(page):
    """Dragging the surface padding updates position without swallowing child clicks (#679)."""
    button = Button(label="Submit")
    panel = FloatPanel(button, position=(40, 50), elevation=4)
    serve_component(page, panel)

    surface = page.locator(".MuiPaper-root")
    expect(page.get_by_role("button", name="Drag floating panel")).to_have_count(0)
    expect(surface).to_have_css("position", "fixed")
    expect(surface).to_have_css("left", "40px")
    expect(surface).to_have_css("top", "50px")
    expect(surface).to_have_class(re.compile("MuiPaper-elevation4"))
    box = surface.bounding_box()
    assert box is not None
    page.mouse.move(box["x"] + 4, box["y"] + 4)
    page.mouse.down()
    page.mouse.move(box["x"] + 64, box["y"] + 34, steps=5)
    page.mouse.up()
    wait_until(lambda: panel.position == (100, 80), page)
    expect(surface).to_have_css("left", "100px")
    expect(surface).to_have_css("top", "80px")

    page.get_by_role("button", name="Submit").click()
    wait_until(lambda: button.clicks == 1, page)

    panel.position = (25, 35)
    expect(surface).to_have_css("left", "25px")
    expect(surface).to_have_css("top", "35px")


def test_float_panel_keyboard_and_children_update(page):
    """Arrow keys move the panel and list-like children can be replaced (#679)."""
    panel = FloatPanel("Initial", position=(20, 20))
    serve_component(page, panel)
    surface = page.get_by_role("group", name="Floating panel")
    surface.focus()
    surface.press("ArrowRight")
    wait_until(lambda: panel.position == (30, 20), page)
    surface.press("ArrowUp")
    wait_until(lambda: panel.position == (30, 10), page)
    panel.objects = [Button(label="Updated")]
    expect(page.get_by_role("button", name="Updated")).to_be_visible()
