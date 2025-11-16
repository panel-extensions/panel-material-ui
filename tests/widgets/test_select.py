import numpy as np
import pytest
from panel.pane import panel
from panel_material_ui.widgets import AutocompleteInput, Select


@pytest.mark.parametrize('widget', [AutocompleteInput, Select])
def test_list_constructor(widget):
    select = widget(options=['A', 1], value=1)
    assert select.options == ['A', 1]

@pytest.mark.parametrize('widget', [AutocompleteInput, Select])
def test_select_float_option_with_equality(widget):
    opts = {'A': 3.14, '1': 2.0}
    select = widget(options=opts, value=3.14, name='Select')
    assert select.value == 3.14

    select.value = 2
    assert select.value == 2.0

    select.value = 3.14
    assert select.value == 3.14

@pytest.mark.parametrize('widget', [AutocompleteInput, Select])
def test_select_text_option_with_equality(widget):
    opts = {'A': 'ABC', '1': 'DEF'}
    select = widget(options=opts, value='DEF', name='Select')
    assert select.value == 'DEF'

    select.value = 'ABC'
    assert select.value == 'ABC'

    select.value = 'DEF'
    assert select.value == 'DEF'

def test_autocomplete(document, comm):
    opts = {'A': 'a', '1': 1}
    select = AutocompleteInput(options=opts, value=opts['1'], name='Autocomplete')

    widget = select.get_root(document, comm=comm)

    assert widget.data.label == 'Autocomplete'
    assert widget.data.value == str(opts['1'])
    assert widget.data.options == list(opts)

    select._process_events({'value': 'A'})
    assert select.value == 'a'

    widget.data.value = '1'
    select.value = opts['1']
    assert select.value == opts['1']

    select.value = opts['A']
    assert widget.data.value == 'A'

def test_autocomplete_reset_none(document, comm):
    widget = AutocompleteInput(options=['A', 'B', 'C'], value='B')

    model = widget.get_root(document, comm=comm)

    assert widget.value == model.data.value == 'B'

    model.data.value = None

    assert widget.value is None

def test_autocomplete_unrestricted(document, comm):
    opts = {'A': 'a', '1': 1}
    select = AutocompleteInput(options=opts, value=opts['1'], name='Autocomplete', restrict=False)

    widget = select.get_root(document, comm=comm)

    assert widget.data.label == 'Autocomplete'
    assert widget.data.value == str(opts['1'])
    assert widget.data.options == list(opts)

    select._process_events({'value': str(opts['A'])})
    assert select.value == opts['A']

    select._process_events({'value': 'foo'})
    assert select.value == 'foo'

    select.value = 'bar'
    assert widget.data.value == 'bar'

def test_autocomplete_clone_with_value():
    autocomplete = AutocompleteInput(
        value='Biology', options=['Biology', 'Chemistry', 'Physics'],
    )
    autocomplete.clone(value='Mathematics', restrict=False)

def test_select(document, comm):
    opts = {'A': 'a', '1': 1}
    select = Select(options=opts, value=opts['1'], name='Select')

    widget = select.get_root(document, comm=comm)

    assert widget.data.label == 'Select'
    assert widget.data.value == str(opts['1'])
    assert widget.data.options == list(opts)

    select._process_events({'value': str(opts['A'])})
    assert select.value == opts['A']

    widget.data.value = str(opts['1'])
    select.value = opts['1']
    assert select.value == opts['1']

    select.value = opts['A']
    assert widget.data.value == 'A'

def test_select_groups_list_options(document, comm):
    groups = dict(a=[1, 2], b=[3])
    select = Select(value=groups['a'][0], groups=groups, name='Select')

    widget = select.get_root(document, comm=comm)

    assert widget.data.label == 'Select'
    assert widget.data.value == str(groups['a'][0])
    assert widget.data.options == {gr: [(str(v), str(v)) for v in values] for gr, values in groups.items()}

    select._process_events({'value': str(groups['a'][1])})
    assert select.value == groups['a'][1]

    select._process_events({'value': str(groups['a'][0])})
    assert select.value == groups['a'][0]

    select.value = groups['a'][1]
    assert widget.data.value == str(groups['a'][1])

def test_select_groups_dict_options(document, comm):
    groups = dict(A=dict(a=1, b=2), B=dict(c=3))
    select = Select(value=groups['A']['a'], groups=groups, name='Select')

    widget = select.get_root(document, comm=comm)

    assert widget.data.label == 'Select'
    assert widget.data.value == 'a'
    assert widget.data.options == {'A': [('1', 'a'), ('2', 'b')], 'B': [('3', 'c')]}

    select._process_events({'value': str(groups['B']['c'])})
    assert select.value == groups['B']['c']

    select._process_events({'value': str(groups['A']['b'])})
    assert select.value == groups['A']['b']

    select.value = groups['A']['a']
    assert widget.data.value == 'a'

def test_select_change_groups(document, comm):
    groups = dict(A=dict(a=1, b=2), B=dict(c=3))
    select = Select(value=groups['A']['a'], groups=groups, name='Select')

    widget = select.get_root(document, comm=comm)

    new_groups = dict(C=dict(d=4), D=dict(e=5, f=6))
    select.groups = new_groups
    assert select.value == new_groups['C']['d']
    assert widget.data.value == 'd'
    assert widget.data.options == {'C': [('4', 'd')], 'D': [('5', 'e'), ('6', 'f')]}

    select.groups = {}
    assert select.value is None
    assert widget.data.value is None

def test_select_groups_error_with_options():
    # Instantiate with groups and options
    with pytest.raises(ValueError):
        Select(options=[1, 2], groups=dict(a=[1], b=[2]), name='Select')

    opts = [1, 2, 3]
    groups = dict(a=[1, 2], b=[3])

    # Instamtiate with options and then update groups
    select = Select(options=opts, name='Select')
    with pytest.raises(ValueError):
        select.groups = groups

    # Instantiate with groups and then update options
    select = Select(groups=groups, name='Select')
    with pytest.raises(ValueError):
        select.options = opts

@pytest.mark.parametrize('widget', [AutocompleteInput, Select])
def test_select_change_options(widget, document, comm):
    opts = {'A': 'a', '1': 1}
    select = widget(options=opts, value=opts['1'], name='Select')

    widget = select.get_root(document, comm=comm)

    select.options = {'A': 'a'}
    if select._allows_none:
        assert select.value is None
        assert widget.data.value is None
    else:
        assert select.value == opts['A']
        assert widget.data.value == 'A'

    select.options = {}
    assert select.value is select.param['value'].default
    assert widget.data.value == select.param['value'].default

@pytest.mark.parametrize('widget', [AutocompleteInput, Select])
def test_select_non_hashable_options(widget, document, comm):
    opts = {'A': np.array([1, 2, 3]), '1': np.array([3, 4, 5])}
    select = widget(options=opts, value=opts['1'], name='Select')

    widget = select.get_root(document, comm=comm)

    if select._allows_none:
        select.value = None
        assert select.value is None
        assert widget.data.value is None
    else:
        select.value = opts['A']
        assert select.value is opts['A']
        assert widget.data.value == (str(opts['A']) if select._allows_values else 'A')

    opts.pop('A')
    select.options = opts
    if select._allows_none:
        assert select.value is None
        assert widget.data.value is None
    else:
        assert select.value is opts['1']
        assert widget.data.value == '1'

def test_select_mutables(document, comm):
    opts = {'A': [1,2,3], 'B': [2,4,6], 'C': dict(a=1,b=2)}
    select = Select(options=opts, value=opts['B'], name='Select')

    widget = select.get_root(document, comm=comm)

    assert widget.data.label == 'Select'
    assert widget.data.value == 'B'
    assert widget.data.options == list(opts)

    widget.data.value = str(opts['B'])
    select._process_events({'value': str(opts['A'])})
    assert select.value == opts['A']

    widget.data.value = str(opts['B'])
    select._process_events({'value': str(opts['B'])})
    assert select.value == opts['B']

    select.value = opts['A']
    assert widget.data.value == 'A'

def test_select_change_options_on_watch(document, comm):
    select = Select(options={'A': 'A', '1': 1, 'C': object},
                    value='A', name='Select')

    def set_options(event):
        if event.new == 1:
            select.options = {'D': 2, 'E': 'a'}
    select.param.watch(set_options, 'value')

    model = select.get_root(document, comm=comm)

    select.value = 1
    assert select.value == 2
    assert model.data.value == 'D'
    assert model.data.options == list(select.options)
