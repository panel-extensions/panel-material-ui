import pytest

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.widgets import Button

pytestmark = pytest.mark.ui


def set_body_data(page, key, value):
    page.evaluate(f"() => {{ document.body.dataset.{key} = {value!r} }}")


@pytest.mark.parametrize('key, dark, light', [
    ('vscodeThemeKind', 'vscode-dark', 'vscode-light'),
    ('vscodeThemeKind', 'vscode-high-contrast', 'vscode-high-contrast-light'),
    ('jpThemeLight', 'false', 'true'),
])
def test_follows_host_theme(page, key, dark, light):
    button = Button(label="Click")
    serve_component(page, button)
    expect(page.locator(".mui-light .MuiButton-root")).to_have_count(1)

    set_body_data(page, key, dark)
    wait_until(lambda: button.dark_theme, page)
    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(1)

    set_body_data(page, key, light)
    wait_until(lambda: not button.dark_theme, page)
    expect(page.locator(".mui-light .MuiButton-root")).to_have_count(1)


def test_host_theme_applied_on_mount(page):
    col = pn.Column(pn.pane.Markdown("Hello"))
    serve_component(page, col)
    expect(page.locator(".markdown")).to_have_count(1)

    set_body_data(page, 'vscodeThemeKind', 'vscode-dark')
    button = Button(label="Click")
    col.append(button)
    wait_until(lambda: button.dark_theme, page)
    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(1)
