import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until

from panel_material_ui.layout import Row
from panel_material_ui.widgets import Button, IntSlider

pytestmark = pytest.mark.ui


@pytest.mark.parametrize("align, expected", [("start", 0), ("center", 0.5), ("end", 1)])
def test_row_child_align(page, align, expected):
    row = Row(
        Button(label="Tall", height=100),
        IntSlider(align=align, css_classes=["aligned"]),
        css_classes=["test-row-align"],
    )
    serve_component(page, row)

    row_el = page.locator(".test-row-align").first
    slider_el = page.locator(".aligned").first

    def aligned():
        rb, sb = row_el.bounding_box(), slider_el.bounding_box()
        if not rb or not sb:
            return False
        free = rb["height"] - sb["height"]
        return free > 20 and abs((sb["y"] - rb["y"]) - free * expected) <= 12

    wait_until(aligned, page)
