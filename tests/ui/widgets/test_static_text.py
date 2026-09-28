import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from playwright.sync_api import expect

from panel_material_ui.widgets import StaticText

pytestmark = pytest.mark.ui


def test_static_text_renders_label_and_html(page):
    widget = StaticText(label='Status', value='<b>Running</b>')
    serve_component(page, widget)
    expect(page.locator('.MuiFormLabel-root')).to_have_text('Status')
    expect(page.locator('b')).to_have_text('Running')

    widget.value = 3
    expect(page.locator('.MuiTypography-root')).to_have_text('3')
