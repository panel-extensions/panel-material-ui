import pytest

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import MaterialWrapper, Row
from panel_material_ui.template import Page
from panel_material_ui.widgets import Button

pytestmark = pytest.mark.ui


def set_body_data(page, key, value, element='body'):
    page.evaluate(f"() => {{ document.{element}.dataset.{key} = {value!r} }}")


@pytest.mark.parametrize('element, key, dark, light', [
    ('body', 'vscodeThemeKind', 'vscode-dark', 'vscode-light'),
    ('body', 'vscodeThemeKind', 'vscode-high-contrast', 'vscode-high-contrast-light'),
    ('body', 'jpThemeLight', 'false', 'true'),
    ('documentElement', 'theme', 'dark', 'light'),
])
def test_follows_host_theme(page, element, key, dark, light):
    button = Button(label="Click")
    serve_component(page, button)
    expect(page.locator(".mui-light .MuiButton-root")).to_have_count(1)

    set_body_data(page, key, dark, element)
    wait_until(lambda: button.dark_theme, page)
    expect(page.locator(".mui-dark .MuiButton-root")).to_have_count(1)

    set_body_data(page, key, light, element)
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


def strip_theme_managed(page):
    # Emulates a host like Jupyter, which owns the document element.
    page.add_init_script("""
      new MutationObserver((_, observer) => {
        if (document.documentElement) {
          document.documentElement.removeAttribute("data-theme-managed")
          observer.disconnect()
        }
      }).observe(document, {childList: true})
    """)


@pytest.mark.parametrize('managed', [True, False])
def test_wrapped_classic_root_resolves_theme_variables(page, managed):
    if not managed:
        strip_theme_managed(page)
    md = pn.pane.Markdown("Hello")
    serve_component(page, MaterialWrapper(md))
    expect(page.locator(".markdown")).to_have_count(1)

    assert page.evaluate(
        "() => document.documentElement.hasAttribute('data-theme-managed')"
    ) is managed
    divider = page.locator(".markdown").evaluate(
        "el => getComputedStyle(el).getPropertyValue('--mui-palette-divider').trim()"
    )
    assert divider


def test_unmanaged_root_does_not_style_host_document(page):
    strip_theme_managed(page)
    serve_component(page, MaterialWrapper(pn.pane.Markdown("Hello")))
    expect(page.locator(".markdown")).to_have_count(1)

    assert page.evaluate("() => document.head.querySelector('#global-styles-panel-mui')") is None
    assert page.evaluate("""() => [...document.querySelectorAll('*')].some(
      el => el.shadowRoot?.querySelector('#global-styles-panel-mui')
    )""")
    assert page.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('--mui-palette-divider').trim()"
    ) == ''


def test_unmanaged_root_follows_host_theme(page):
    strip_theme_managed(page)
    md = pn.pane.Markdown("Hello")
    wrapper = MaterialWrapper(md)
    serve_component(page, wrapper)
    expect(page.locator(".markdown")).to_have_count(1)

    def divider():
        return page.locator(".markdown").evaluate(
            "el => getComputedStyle(el).getPropertyValue('--mui-palette-divider').trim()"
        )
    light = divider()

    set_body_data(page, 'jpThemeLight', 'false')
    wait_until(lambda: wrapper.dark_theme, page)
    wait_until(lambda: divider() not in ('', light), page)


def themed_figure():
    from bokeh.plotting import figure
    fig = figure(title="Plot")
    fig.line([0, 1], [0, 1])
    return fig


def test_unmanaged_standalone_figure_is_grounded(page):
    strip_theme_managed(page)
    fig = themed_figure()
    serve_component(page, Row(fig))
    expect(page.locator(".bk-Figure")).to_have_count(1)

    axis = fig.yaxis[0]
    wait_until(lambda: axis.axis_line_alpha == 1 and axis.major_tick_line_alpha == 1, page)
    assert axis.minor_tick_line_alpha == 0
    assert fig.outline_line_alpha == 0.3
    assert fig.title.text_font_style == "bold"


def test_unmanaged_explicit_minimal_figure(page):
    strip_theme_managed(page)
    fig = themed_figure()
    serve_component(page, Row(fig, theme_config={"chart_style": "minimal"}))
    expect(page.locator(".bk-Figure")).to_have_count(1)

    axis = fig.yaxis[0]
    wait_until(lambda: axis.axis_line_alpha == 0 and axis.major_tick_line_alpha == 0, page)
    assert fig.title.text_font_style == "normal"


def test_page_figure_stays_minimal(page):
    fig = themed_figure()
    serve_component(page, Page(main=[fig]))
    expect(page.locator(".bk-Figure")).to_have_count(1)

    axis = fig.yaxis[0]
    wait_until(lambda: axis.axis_line_alpha == 0 and axis.major_tick_line_alpha == 0, page)
    assert fig.title.text_font_style == "normal"


def test_page_figure_standard_chart_style(page):
    fig = themed_figure()
    serve_component(page, Page(main=[fig], theme_config={"chart_style": "standard"}))
    expect(page.locator(".bk-Figure")).to_have_count(1)

    axis = fig.yaxis[0]
    wait_until(lambda: axis.axis_line_alpha == 1 and axis.major_tick_line_alpha == 1, page)
    assert axis.minor_tick_line_alpha == 0
    assert fig.title.text_font_style == "bold"
