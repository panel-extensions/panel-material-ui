import pytest

pytest.importorskip('playwright')

import panel as pn
from bokeh.plotting import figure
from panel.tests.util import serve_component, wait_until

from panel_material_ui.template import Page

pytestmark = pytest.mark.ui


def model_state(page, model_type, expr):
    return page.evaluate(f"""() => {{
      const model = [...Bokeh.documents[0].all_models].find(m => m.type.endsWith({model_type!r}))
      const view = model && Bokeh.index.find_one_by_id(model.id)
      return model && view ? {expr} : null
    }}""")


def toggle_theme(page):
    page.get_by_label('Toggle theme').click()


def test_transparent_figure_is_not_boxed(page):
    serve_component(page, Page(main=[pn.indicators.Dial(value=40)]))

    toggle_theme(page)

    wait_until(lambda: model_state(
        page, 'Figure', '[model.outline_line_color, model.background_fill_alpha, model.border_fill_alpha]'
    ) == [None, 0, 0], page)


def test_opaque_figure_is_themed(page):
    fig = figure(width=300, height=200)
    fig.line([0, 1], [0, 1])
    serve_component(page, Page(main=[pn.pane.Bokeh(fig)]))

    toggle_theme(page)

    wait_until(lambda: model_state(
        page, 'Figure', '[model.outline_line_color, model.border_fill_color]'
    ) == ['#fff', '#121212'], page)


def test_terminal_follows_theme(page):
    serve_component(page, Page(main=[pn.widgets.Terminal('Hello', height=100)]))

    wait_until(lambda: model_state(
        page, 'Terminal', '[model.options.theme.background, model.options.theme.foreground]'
    ) == ['#fff', '#212121'], page)

    toggle_theme(page)

    wait_until(lambda: model_state(
        page, 'Terminal', '[model.options.theme.foreground, view.term.getOption("theme").foreground]'
    ) == ['#fff', '#fff'], page)


def test_gauge_follows_theme(page):
    pn.extension('echarts')
    serve_component(page, Page(main=[pn.indicators.Gauge(value=40)]))

    wait_until(lambda: model_state(page, 'ECharts', 'model.theme') == 'default', page)

    toggle_theme(page)

    wait_until(lambda: model_state(page, 'ECharts', 'model.theme') == 'dark', page)


def test_icon_filter_variable_follows_theme(page):
    serve_component(page, Page(main=['Content']))
    icon_filter = "getComputedStyle(document.documentElement).getPropertyValue('--panel-icon-filter').trim()"

    wait_until(lambda: page.evaluate(icon_filter) == 'none', page)

    toggle_theme(page)

    wait_until(lambda: page.evaluate(icon_filter) == 'invert(1)', page)
