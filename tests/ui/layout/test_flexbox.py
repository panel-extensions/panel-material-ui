import pytest

pytest.importorskip('playwright')

from panel.layout import Spacer
from panel.tests.util import serve_component, wait_until

from panel_material_ui.layout import FlexBox

pytestmark = pytest.mark.ui


def test_flexbox_row_children_use_width_as_basis(page):
    layout = FlexBox(
        Spacer(width=400, height=100, styles={'background': 'red'}),
        Spacer(width=200, height=100, styles={'background': 'blue'}),
        flex_wrap='nowrap',
    )
    serve_component(page, layout)

    spacers = page.locator('.bk-Spacer')
    wait_until(lambda: spacers.nth(0).bounding_box()['width'] == 400, page)
    assert spacers.nth(1).bounding_box()['width'] == 200


def test_flexbox_column_children_use_height_as_basis(page):
    layout = FlexBox(
        Spacer(width=100, height=150, styles={'background': 'red'}),
        Spacer(width=100, height=50, styles={'background': 'blue'}),
        flex_direction='column', height=400,
    )
    serve_component(page, layout)

    spacers = page.locator('.bk-Spacer')
    wait_until(lambda: spacers.nth(0).bounding_box()['height'] == 150, page)
    assert spacers.nth(1).bounding_box()['height'] == 50


def test_flexbox_stretches_width_by_default(page):
    layout = FlexBox(Spacer(sizing_mode='stretch_width', height=50, styles={'background': 'red'}))
    serve_component(page, layout)

    spacer = page.locator('.bk-Spacer')
    wait_until(lambda: spacer.bounding_box()['width'] > 500, page)
