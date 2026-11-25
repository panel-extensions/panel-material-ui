import pytest

pytest.importorskip('playwright')

from bokeh.plotting import figure
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.template import Page

pytestmark = pytest.mark.ui


def plot_style(page):
    return page.evaluate("""() => {
      const model = [...Bokeh.documents[0].all_models].find(m => m.name === 'custom-plot')
      return model && [model.outline_line_color, model.outline_line_alpha, model.background_fill_color]
    }""")


def assert_custom_style(page):
    try:
        wait_until(lambda: plot_style(page) == ['#ff0066', 1, '#abcdef'], page)
    except TimeoutError:
        details = page.evaluate("""() => [...Bokeh.documents[0].all_models]
          .filter(m => m.type.endsWith('Figure'))
          .map(m => ({name: m.name, color: m.outline_line_color,
            alpha: m.outline_line_alpha, background: m.background_fill_color,
            dirty: ['outline_line_color', 'outline_line_alpha', 'background_fill_color']
              .map(p => m.properties[p].dirty)}))""")
        pytest.fail(f'Custom plot style was not preserved: {details}')


def default_background(page):
    return page.evaluate("""() => {
      const model = [...Bokeh.documents[0].all_models].find(m => m.name === 'default-plot')
      return model && model.background_fill_color
    }""")


def switch_theme(page):
    previous = default_background(page)
    page.get_by_label('Toggle theme').click()
    wait_until(lambda: default_background(page) != previous, page)


@pytest.mark.parametrize('backend', ['bokeh', 'holoviews'])
def test_page_preserves_explicit_plot_styles(page, backend):
    if backend == 'holoviews':
        hv = pytest.importorskip('holoviews')
        hv.extension('bokeh')

        def customize(plot, element):
            plot.state.name = 'custom-plot'
            plot.state.outline_line_color = '#ff0066'
            plot.state.outline_line_alpha = 1

        plot = hv.Curve([1, 2, 3]).opts(bgcolor='#abcdef', hooks=[customize])
    else:
        plot = figure(
            name='custom-plot', outline_line_color='#ff0066',
            outline_line_alpha=1, background_fill_color='#abcdef',
        )
        plot.line([0, 1], [0, 1])

    baseline = figure(name='default-plot')
    baseline.line([0, 1], [0, 1])
    serve_component(page, Page(main=[plot, baseline]))
    expect(page.locator('.bk-Figure')).to_have_count(2)
    assert_custom_style(page)

    for _ in range(2):
        switch_theme(page)
        assert_custom_style(page)


def test_plot_style_updated_after_render_survives_theme_switch(page):
    plot = figure(name='custom-plot')
    plot.line([0, 1], [0, 1])
    baseline = figure(name='default-plot')
    baseline.line([0, 1], [0, 1])
    serve_component(page, Page(main=[plot, baseline]))
    expect(page.locator('.bk-Figure')).to_have_count(2)

    def update_style():
        plot.outline_line_color = '#ff0066'
        plot.outline_line_alpha = 1
        plot.background_fill_color = '#abcdef'

    plot.document.add_next_tick_callback(update_style)
    assert_custom_style(page)

    switch_theme(page)
    assert_custom_style(page)
