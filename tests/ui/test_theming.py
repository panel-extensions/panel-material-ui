import pytest

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Column, Row, Tabs
from panel_material_ui.template import Page, ThemeToggle
from panel_material_ui.widgets import Button, Chip, RadioButtonGroup, TextInput

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


RECORD_LIGHT = """
window.__light_seen = false
new MutationObserver((records) => {
  for (const r of records) {
    const nodes = r.type === "attributes" ? [r.target] : [...r.addedNodes]
    for (const n of nodes) {
      if (n.classList && n.classList.contains("mui-light")) {
        window.__light_seen = true
      }
    }
  }
}).observe(document, {subtree: true, childList: true, attributes: true, attributeFilter: ["class"]})
const _attach = Element.prototype.attachShadow
Element.prototype.attachShadow = function(init) {
  const root = _attach.call(this, init)
  new MutationObserver((records) => {
    for (const r of records) {
      const nodes = r.type === "attributes" ? [r.target] : [...r.addedNodes]
      for (const n of nodes) {
        if (n.classList && n.classList.contains("mui-light")) {
          window.__light_seen = true
        }
      }
    }
  }).observe(root, {subtree: true, childList: true, attributes: true, attributeFilter: ["class"]})
  return root
}
"""


def body_background(page):
    return page.evaluate("() => getComputedStyle(document.body).backgroundColor")


def test_explicit_dark_component_makes_page_dark(page):
    button = Button(label="Dark Button", dark_theme=True)
    serve_component(page, button)

    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(1)
    wait_until(lambda: body_background(page) == "rgb(18, 18, 18)", page)
    assert pn.config.theme == "default"


def test_explicit_dark_component_switches_siblings(page):
    other = Button(label="Other")
    dark = Button(label="Dark", dark_theme=True)
    serve_component(page, Row(other, dark))

    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(2)
    wait_until(lambda: other.dark_theme, page)


def test_dark_column_renders_dark_from_first_paint(page):
    page.add_init_script(RECORD_LIGHT)
    serve_component(page, Column(Button(label="A"), Button(label="B"), dark_theme=True))

    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(2)
    page.wait_for_timeout(300)
    assert not page.evaluate("() => window.__light_seen")


def test_python_component_change_switches_page(page):
    button = Button(label="Click")
    other = Button(label="Other")
    serve_component(page, Column(button, other))
    expect(page.locator(".mui-light .MuiButton-root")).to_have_count(2)

    button.dark_theme = True

    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(2)
    assert other.dark_theme


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


def test_rerendered_explicit_layout_does_not_override_toggle(page):
    w = pn.widgets.IntInput(value=0)
    toggle = ThemeToggle()
    other = Button(label="Other")
    bound = pn.bind(lambda v: Column(Button(label=f"dyn{v}"), dark_theme=True), w)
    serve_component(page, Column(toggle, other, bound))
    wait_until(lambda: body_background(page) == "rgb(18, 18, 18)", page)

    page.locator('[aria-label="Toggle theme"]').click()
    wait_until(lambda: body_background(page) == "rgb(255, 255, 255)", page)

    w.value = 1
    expect(page.locator(".MuiButton-root", has_text="dyn1")).to_have_count(1)
    page.wait_for_timeout(500)
    assert body_background(page) == "rgb(255, 255, 255)"
    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(0)
    assert not toggle.value


def test_theme_toggle_without_value_does_not_override_explicit(page):
    other = Button(label="Other")
    serve_component(page, Column(Button(label="Dark", dark_theme=True), ThemeToggle(), other))
    wait_until(lambda: body_background(page) == "rgb(18, 18, 18)", page)
    page.wait_for_timeout(300)
    assert body_background(page) == "rgb(18, 18, 18)"


def test_servable_factory_explicit_component_aligns_siblings(page):
    objs = {}

    def app():
        objs['other'] = Button(label="Other")
        return Row(objs['other'], Button(label="Dark", dark_theme=True))

    serve_component(page, app)
    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(2)
    wait_until(lambda: body_background(page) == "rgb(18, 18, 18)", page)
    wait_until(lambda: objs['other'].dark_theme, page)


def test_invalid_theme_config_falls_back_and_recovers(page):
    msgs = []
    page.on("console", lambda msg: msgs.append(msg.text))
    bad = Button(label="Bad", theme_config={'palette': {'primary': {'main': 'teal'}}})
    serve_component(page, Row(bad, Button(label="Fine")))

    expect(page.locator(".MuiButton-root")).to_have_count(2)
    wait_until(lambda: any("invalid theme_config" in m for m in msgs), page)

    bad.theme_config = {'palette': {'primary': {'main': '#ff0000'}}}
    expect(page.locator(".MuiButton-root").first).to_have_css("background-color", "rgb(255, 0, 0)")


PRIMARY = {'palette': {'primary': {'main': '#0072B5'}}}
PRIMARY_RGB = "rgb(0, 114, 181)"
PRIMARY_TEXT_RGB = "rgb(89, 163, 207)"


def _primary_components(dark, theme_config=PRIMARY):
    return Column(
        Button(label="Text", variant="text"),
        Button(label="Outlined", variant="outlined"),
        Button(label="Contained", variant="contained"),
        Tabs(("A", "a"), ("B", "b")),
        RadioButtonGroup(options=["X", "Y"], value="X", variant="outlined"),
        Chip(label="Chip", variant="outlined"),
        TextInput(label="Name"),
        pn.pane.Markdown("A [link](https://holoviz.org)"),
        dark_theme=dark, theme_config=theme_config,
    )


def _expect_primary_colors(page, text, fill):
    buttons = page.locator(".MuiButton-root")
    expect(buttons.nth(0)).to_have_css("color", text)
    expect(buttons.nth(1)).to_have_css("color", text)
    expect(buttons.nth(2)).to_have_css("background-color", fill)
    expect(page.locator(".MuiTab-root.Mui-selected")).to_have_css("color", text)
    expect(page.locator(".MuiTabs-indicator")).to_have_css("background-color", text)
    expect(page.locator(".MuiToggleButton-root.Mui-selected")).to_have_css("color", text)
    expect(page.locator(".MuiChip-root")).to_have_css("color", text)
    page.locator(".MuiInputBase-input").click()
    expect(page.locator(".MuiInputLabel-root.Mui-focused")).to_have_css("color", text)
    expect(page.locator(".Mui-focused .MuiOutlinedInput-notchedOutline")).to_have_css("border-top-color", text)


def _expect_link_color(page, color):
    expect(page.locator(".markdown a")).to_have_css("color", color)


def test_light_primary_text_is_unchanged(page):
    serve_component(page, _primary_components(False))
    _expect_primary_colors(page, PRIMARY_RGB, PRIMARY_RGB)
    _expect_link_color(page, PRIMARY_RGB)


def test_dark_primary_text_uses_tint(page):
    serve_component(page, _primary_components(True))
    _expect_primary_colors(page, PRIMARY_TEXT_RGB, PRIMARY_RGB)
    _expect_link_color(page, PRIMARY_TEXT_RGB)


def test_dark_primary_text_follows_theme_toggle(page):
    toggle = ThemeToggle()
    serve_component(page, Column(toggle, _primary_components(False)))
    _expect_primary_colors(page, PRIMARY_RGB, PRIMARY_RGB)
    page.locator('[aria-label="Toggle theme"]').click()
    _expect_primary_colors(page, PRIMARY_TEXT_RGB, PRIMARY_RGB)


def test_dark_primary_text_can_be_overridden(page):
    config = {'palette': {'primary': {'main': '#0072B5', 'text': '#ff00ff'}}}
    serve_component(page, _primary_components(True, config))
    _expect_primary_colors(page, "rgb(255, 0, 255)", PRIMARY_RGB)
