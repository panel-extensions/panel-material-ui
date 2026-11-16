import pytest

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Column, Row
from panel_material_ui.template import Page, ThemeToggle
from panel_material_ui.widgets import Button

pytestmark = pytest.mark.ui

COUNT_WS_SENDS = """
window.__ws_sent = 0
const _send = WebSocket.prototype.send
WebSocket.prototype.send = function(data) { window.__ws_sent++; return _send.call(this, data) }
"""


@pytest.fixture(autouse=True)
def reset_theme():
    try:
        yield
    finally:
        pn.config.theme = 'default'


def test_dark_toggle_syncs_once_and_updates_python(page):
    page.add_init_script(COUNT_WS_SENDS)
    buttons = [Button(label=f"B{i}") for i in range(20)]
    toggle = ThemeToggle()
    serve_component(page, Column(toggle, *buttons))
    expect(page.locator(".MuiButton-root")).to_have_count(20)
    page.wait_for_timeout(500)

    sent = page.evaluate("() => window.__ws_sent")
    page.locator('[aria-label="Toggle theme"]').click()

    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(20)
    wait_until(lambda: all(b.dark_theme for b in buttons), page)
    page.wait_for_timeout(500)
    # One message for the toggle's value and dark_theme each, instead of one
    # per component.
    assert page.evaluate("() => window.__ws_sent") - sent <= 3


def test_page_toggle_does_not_flip_from_component_change(page):
    button = Button(label="Click")
    other = Button(label="Other")
    pg = Page(main=[button, other])
    serve_component(page, pg)
    expect(page.locator(".MuiButton-root").first).to_be_visible()

    button.dark_theme = True

    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(1)
    page.wait_for_timeout(300)
    assert not pg.dark_theme
    assert not other.dark_theme


def test_bokeh_toolbar_stylesheets_do_not_grow(page):
    from bokeh.plotting import figure
    fig = figure(title="Plot")
    fig.line([0, 1], [0, 1])
    serve_component(page, Column(ThemeToggle(), pn.pane.Bokeh(fig)))
    expect(page.locator(".bk-Figure")).to_have_count(1)
    wait_until(lambda: len(fig.toolbar.stylesheets) > 0, page)
    initial = len(fig.toolbar.stylesheets)

    toggle = page.locator('[aria-label="Toggle theme"]')
    for _ in range(4):
        toggle.click()
        page.wait_for_timeout(200)
    page.wait_for_timeout(500)

    assert len(fig.toolbar.stylesheets) == initial


def test_page_header_contrast_follows_theme_config(page):
    button = Button(label="Header", variant="contained", color="primary")
    pg = Page(theme_config={'palette': {'primary': {'main': '#ffeb3b'}}}, header=[button])
    serve_component(page, pg)

    header_button = page.locator(".MuiAppBar-root .MuiButton-root")
    expect(page.locator(".MuiAppBar-root")).to_have_css("background-color", "rgb(255, 235, 59)")
    # A light primary color gets a dark header palette, so the contained
    # button is black with the primary color as its text.
    expect(header_button).to_have_css("background-color", "rgb(0, 0, 0)")
    expect(header_button).to_have_css("color", "rgb(255, 235, 59)")


def test_unmanaged_root_updates_page_style(page):
    page.add_init_script("""
      new MutationObserver((_, observer) => {
        if (document.documentElement) {
          document.documentElement.setAttribute("data-theme-managed", "false")
          observer.disconnect()
        }
      }).observe(document, {childList: true})
    """)
    col = Column(Button(label="Click"))
    serve_component(page, col)
    expect(page.locator(".MuiButton-root")).to_have_count(1)

    def background():
        return page.evaluate("""() => {
          const el = document.querySelector('#page-style')
          return el && (el.textContent.match(/--mui-palette-background-default:\\s*([^;]*)/) || [])[1]
        }""")
    wait_until(lambda: background() == '#fff', page)

    col.dark_theme = True
    wait_until(lambda: background() == '#121212', page)


def test_render_error_is_contained_and_recovers(page):
    msgs = []
    page.on("console", lambda msg: msgs.append(msg.text))
    broken = Button(label="Broken")
    ok = Button(label="Fine")
    row = Row(broken, ok)
    serve_component(page, row)
    expect(page.locator(".MuiButton-root")).to_have_count(2)

    model_id = broken._models[next(iter(row._models))][0].ref['id']
    # React refuses to render a plain object as a child, which throws.
    page.evaluate(f"""() => {{
      const model = Bokeh.documents[0].get_model_by_id({model_id!r})
      model.data.setv({{label: {{not: "renderable"}}}}, {{sync: false}})
    }}""")

    expect(page.locator(".MuiButton-root")).to_have_count(1)
    expect(page.locator(".MuiButton-root")).to_have_text("Fine")
    wait_until(lambda: any("Button failed to render" in m for m in msgs), page)

    broken.label = "Recovered"
    expect(page.locator(".MuiButton-root")).to_have_count(2)
    expect(page.locator(".MuiButton-root").first).to_have_text("Recovered")
