import pytest

pytest.importorskip('playwright')

from panel_material_ui.template import Page

from playwright.sync_api import expect
from panel.tests.util import serve_component

pytestmark = pytest.mark.ui


def test_page_theme_config_header_color(page):
    pg = Page()

    serve_component(page, pg)

    header = page.locator(".MuiAppBar-root")
    expect(header).to_have_css("background-color", "rgb(0, 114, 181)")

    pg.theme_config = {
        "palette": {
            "primary": {
                "main": "#000000"
            }
        }
    }
    expect(header).to_have_css("background-color", "rgb(0, 0, 0)")
