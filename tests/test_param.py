"""
Widgets Panel generates for parameters are Material widgets, whether Panel
resolves them through MaterialDesign (Panel >= 1.10) or through the patched
mappings on older releases.
"""
import panel as pn
import param
import pytest
from panel.config import config
from panel.interact import interactive
from panel.param import Param

import panel_material_ui as pmui
from panel_material_ui.theme import PANEL_DESIGN_HOOKS, MaterialDesign


class Params(param.Parameterized):

    action = param.Action(lambda self: None)
    boolean = param.Boolean()
    dictionary = param.Dict({})
    integer = param.Integer(1)
    listing = param.List([])
    number = param.Number(1, bounds=(0, 10))
    selector = param.Selector(objects=['a', 'b'])
    span = param.Range((0, 1), bounds=(0, 2))
    unbounded_span = param.Range((0, 1))
    partially_bounded_span = param.Range((0, 1), bounds=(0, None))
    string = param.String()


@pytest.fixture
def material():
    with config.set(design=MaterialDesign):
        yield


def test_param_widgets_are_material(material):
    widgets = {w.label: type(w) for w in Param(Params()).layout[1:]}

    assert widgets == {
        'Action': pmui.Button,
        'Boolean': pmui.Checkbox,
        'Dictionary': pmui.DictInput,
        'Integer': pmui.IntInput,
        'Listing': pmui.ListInput,
        'Number': pmui.FloatSlider,
        'Selector': pmui.Select,
        'Span': pmui.RangeSlider,
        'Unbounded span': pmui.TupleInput,
        'Partially bounded span': pmui.TupleInput,
        'String': pmui.TextInput,
    }


@pytest.mark.skipif(not PANEL_DESIGN_HOOKS, reason='Requires Panel >= 1.10')
def test_interact_widgets_are_material(material):
    result = interactive(lambda s, i, o: None, s='a', i=1, o=['a', 'b'])

    assert {name: type(w) for name, w in result._widgets.items()} == {
        's': pmui.TextInput, 'i': pmui.IntSlider, 'o': pmui.Select,
    }


@pytest.mark.skipif(not PANEL_DESIGN_HOOKS, reason='Requires Panel >= 1.10')
def test_classic_design_keeps_classic_widgets():
    with config.set(design=None):
        widgets = {w.label: type(w) for w in Param(Params()).layout[1:]}

    assert widgets['String'] is pn.widgets.TextInput
    assert widgets['Boolean'] is pn.widgets.Checkbox


@pytest.mark.skipif(not PANEL_DESIGN_HOOKS, reason='Requires Panel >= 1.10')
def test_import_does_not_patch_panel():
    assert Param.mapping[param.String] is pn.widgets.TextInput
    assert Param.input_widgets[int] is pn.widgets.IntInput
    assert pn.pane.HoloViews.default_widgets['scrubber'] is pn.widgets.Player
