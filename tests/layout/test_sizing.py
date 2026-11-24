import pytest

from bokeh.document import Document
from panel.io.state import set_curdoc
from panel.pane import Markdown

from panel_material_ui.layout import Column, Row

PROPS = ('sizing_mode', 'width', 'min_width', 'height', 'min_height')


def _render(layout):
    doc = Document()
    with set_curdoc(doc):
        model = layout.get_root(doc)
    return doc, model


def _sizing(model):
    return {prop: getattr(model, prop) for prop in PROPS}


def _fresh_sizing(layout_type, objects):
    _, model = _render(layout_type(*objects()))
    return _sizing(model)


@pytest.mark.parametrize('layout_type', [Column, Row])
@pytest.mark.parametrize('child', [
    dict(sizing_mode='stretch_width'),
    dict(sizing_mode='stretch_height'),
    dict(sizing_mode='stretch_both'),
    dict(sizing_mode='stretch_width', min_width=500),
])
def test_layout_reinfers_sizing_on_append(layout_type, child):
    layout = layout_type(Markdown('fixed', width=200))
    doc, model = _render(layout)
    with set_curdoc(doc):
        layout.append(Markdown('new', **child))

    expected = _fresh_sizing(layout_type, lambda: [Markdown('fixed', width=200), Markdown('new', **child)])
    assert _sizing(model) == expected
    assert model.sizing_mode == expected['sizing_mode'] != None  # noqa: E711


@pytest.mark.parametrize('layout_type', [Column, Row])
def test_empty_layout_reinfers_sizing_when_filled(layout_type):
    layout = layout_type()
    doc, model = _render(layout)
    with set_curdoc(doc):
        layout.objects = [Markdown('a', sizing_mode='stretch_both')]

    assert _sizing(model) == _fresh_sizing(layout_type, lambda: [Markdown('a', sizing_mode='stretch_both')])
    assert model.sizing_mode == 'stretch_both'


@pytest.mark.parametrize('layout_type', [Column, Row])
def test_explicit_layout_sizing_mode_is_kept_on_update(layout_type):
    layout = layout_type(Markdown('fixed', width=200), sizing_mode='fixed', width=300)
    doc, model = _render(layout)
    with set_curdoc(doc):
        layout.append(Markdown('wide', sizing_mode='stretch_width'))

    expected = _fresh_sizing(
        lambda *objs: layout_type(*objs, sizing_mode='fixed', width=300),
        lambda: [Markdown('fixed', width=200), Markdown('wide', sizing_mode='stretch_width')]
    )
    assert _sizing(model) == expected
