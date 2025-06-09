import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets.menus import Pagination
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_pagination_basic(page):
    widget = Pagination(count=5)
    serve_component(page, widget)

    pagination = page.locator('.MuiPagination-root')
    expect(pagination).to_have_count(1)

    # Check number of page buttons (including prev/next)
    page_buttons = page.locator('.MuiPaginationItem-root')
    expect(page_buttons).to_have_count(7)  # 5 pages + prev/next buttons

def test_pagination_navigation(page):
    widget = Pagination(count=5)
    serve_component(page, widget)

    # Click second page
    page.locator('.MuiPaginationItem-root').nth(2).click()
    wait_until(lambda: widget.value == 1, page)
