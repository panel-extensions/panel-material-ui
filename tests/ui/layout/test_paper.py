import pytest

pytest.importorskip('playwright')

from panel_material_ui.layout import Paper

from playwright.sync_api import expect
from panel.tests.util import serve_component

pytestmark = pytest.mark.ui

def test_paper(page):
    layout = Paper(name="Paper", objects=[1, 2, 3])
    serve_component(page, layout)
    expect(page.locator('.paper')).to_have_count(1)
