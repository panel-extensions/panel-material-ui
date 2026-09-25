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
    """Dragging the surface moves it without swallowing child clicks (#679)."""
    button = Button(label="Submit")
    panel = FloatPanel(button, position="left-top", offsetx=40, offsety=50, elevation=4, contained=False)
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
    expect(surface).to_have_css("left", "100px")
    expect(surface).to_have_css("top", "80px")

    page.get_by_role("button", name="Submit").click()
    wait_until(lambda: button.clicks == 1, page)

    panel.param.update(offsetx=25, offsety=35)
    expect(surface).to_have_css("left", "25px")
    expect(surface).to_have_css("top", "35px")


def test_float_panel_keyboard_and_children_update(page):
    """Arrow keys move the panel and list-like children can be replaced (#679)."""
    panel = FloatPanel("Initial", position="left-top", offsetx=20, offsety=20, contained=False)
    serve_component(page, panel)
    surface = page.get_by_role("group", name="Floating panel")
    surface.focus()
    surface.press("ArrowRight")
    expect(surface).to_have_css("left", "30px")
    surface.press("ArrowUp")
    expect(surface).to_have_css("top", "10px")
    panel.objects = [Button(label="Updated")]
    expect(page.get_by_role("button", name="Updated")).to_be_visible()


def test_float_panel_window_controls(page):
    """Window controls update status and allow restoring a closed panel (#679)."""
    panel = FloatPanel(Button(label="Content"), name="Tools", contained=False, position="center")
    serve_component(page, panel)
    surface = page.get_by_role("group", name="Floating panel")
    expect(surface).to_be_visible()
    expect(surface).to_contain_text("Tools")
    page.get_by_role("button", name="Minimize floating panel").click()
    wait_until(lambda: panel.status == "minimized", page)
    expect(page.get_by_role("button", name="Content")).to_have_count(0)
    page.get_by_role("button", name="Restore floating panel").click()
    wait_until(lambda: panel.status == "normalized", page)
    expect(page.get_by_role("button", name="Content")).to_be_visible()
    page.get_by_role("button", name="Maximize floating panel").click()
    wait_until(lambda: panel.status == "maximized", page)
    expect(surface).to_have_css("width", f"{page.viewport_size['width']}px")
    page.get_by_role("button", name="Restore size").click()
    wait_until(lambda: panel.status == "normalized", page)
    page.get_by_role("button", name="Close floating panel").click()
    wait_until(lambda: panel.status == "closed", page)
    expect(surface).to_have_count(0)
    panel.status = "normalized"
    expect(surface).to_be_visible()


def test_float_panel_contained(page):
    """Contained panels use their parent as the positioning boundary (#679)."""
    from panel_material_ui.layout import Column

    panel = FloatPanel("Content", position="right-bottom", offsetx=12, offsety=15)
    serve_component(page, Column(panel, width=420, height=300))
    surface = page.get_by_role("group", name="Floating panel")
    expect(surface).to_have_css("position", "absolute")
    expect(surface).to_have_css("right", "12px")
    expect(surface).to_have_css("bottom", "15px")
    panel.position = "center"
    expect(surface).to_have_css("transform", re.compile(r"matrix\(1, 0, 0, 1, -"))


def test_float_panel_size_and_smallified(page):
    """Explicit dimensions, resize affordance, and smallified status remain usable (#679)."""
    panel = FloatPanel("Content", name="Tools", width=240, height=160,
                       position="left-top", contained=False)
    serve_component(page, panel)
    surface = page.get_by_role("group", name="Floating panel")
    handle = page.get_by_label("Resize floating panel")
    expect(handle).to_be_visible()
    before = surface.bounding_box()
    corner = handle.bounding_box()
    assert before is not None and corner is not None
    page.mouse.move(corner["x"] + corner["width"] / 2, corner["y"] + corner["height"] / 2)
    page.mouse.down()
    page.mouse.move(corner["x"] + corner["width"] / 2 + 80,
                    corner["y"] + corner["height"] / 2 + 60, steps=8)
    page.mouse.up()
    after = surface.bounding_box()
    assert after is not None
    assert after["width"] >= before["width"] + 60
    assert after["height"] >= before["height"] + 40
    panel.status = "smallified"
    expect(page.get_by_role("button", name="Content")).to_have_count(0)
    panel.status = "normalized"
    expect(surface).to_contain_text("Content")


def test_float_panel_resizes_without_explicit_dimensions(page):
    """A content-sized panel can be resized from the browser corner (#679)."""
    panel = FloatPanel("Content", position="left-top", contained=False)
    serve_component(page, panel)
    surface = page.get_by_role("group", name="Floating panel")
    before = surface.bounding_box()
    corner = page.get_by_label("Resize floating panel").bounding_box()
    assert before is not None and corner is not None
    page.mouse.move(corner["x"] + corner["width"] / 2, corner["y"] + corner["height"] / 2)
    page.mouse.down()
    page.mouse.move(corner["x"] + corner["width"] / 2 + 80,
                    corner["y"] + corner["height"] / 2 + 60, steps=8)
    page.mouse.up()
    after = surface.bounding_box()
    assert after is not None
    assert after["width"] >= before["width"] + 60
    assert after["height"] >= before["height"] + 40


def test_float_panel_resizes_from_right_bottom_anchor(page):
    """Resizing an anchored panel grows it without moving its top-left corner (#679)."""
    panel = FloatPanel("Content", position="right-bottom", offsetx=40, offsety=50,
                       contained=False)
    serve_component(page, panel)
    surface = page.get_by_role("group", name="Floating panel")
    before = surface.bounding_box()
    corner = page.get_by_label("Resize floating panel").bounding_box()
    assert before is not None and corner is not None
    page.mouse.move(corner["x"] + corner["width"] / 2, corner["y"] + corner["height"] / 2)
    page.mouse.down()
    page.mouse.move(corner["x"] + corner["width"] / 2 + 30,
                    corner["y"] + corner["height"] / 2 + 35, steps=8)
    page.mouse.up()
    after = surface.bounding_box()
    assert after is not None
    assert abs(after["x"] - before["x"]) < 2
    assert abs(after["y"] - before["y"]) < 2
    assert after["width"] >= before["width"] + 20
    assert after["height"] >= before["height"] + 25


def test_float_panel_buttons_can_be_hidden(page):
    """The controls list selects title-bar actions and updates live (#679)."""
    panel = FloatPanel("Content", contained=False, controls=["close"])
    serve_component(page, panel)
    expect(page.get_by_role("button", name="Minimize floating panel")).to_have_count(0)
    expect(page.get_by_role("button", name="Maximize floating panel")).to_have_count(0)
    expect(page.get_by_role("button", name="Close floating panel")).to_be_visible()
    panel.controls = []
    expect(page.get_by_role("button", name="Close floating panel")).to_have_count(0)
    panel.controls = ["maximize"]
    expect(page.get_by_role("button", name="Maximize floating panel")).to_be_visible()


def test_float_panel_no_controls(page):
    """A floating toolbar can omit all title-bar actions (#679)."""
    panel = FloatPanel(Button(label="Submit"), contained=False, position="center", controls=[])
    serve_component(page, panel)
    surface = page.get_by_role("group", name="Floating panel")
    expect(surface.get_by_role("button")).to_have_count(1)
    expect(page.get_by_role("button", name="Submit")).to_be_visible()
