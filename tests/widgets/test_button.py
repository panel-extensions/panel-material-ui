import panel as pn
import pytest

from panel_material_ui.widgets import Button, FileDownload, FileInput, IconButton, MenuButton, MenuToggle, SplitButton, Toggle


@pytest.mark.filterwarnings('ignore:.*button_style.*:PendingDeprecationWarning')
@pytest.mark.parametrize('widget_type', [Button, Toggle, FileDownload, FileInput, IconButton, MenuButton, MenuToggle, SplitButton])
@pytest.mark.parametrize(('classic', 'material'), [('solid', 'contained'), ('outline', 'outlined')])
def test_classic_variant_compatibility(widget_type, classic, material):
    widget = widget_type(variant=classic)
    assert widget.variant == material
    widget = widget_type(button_style=classic)
    assert widget.variant == material
    widget.variant = classic
    assert widget.variant == material
    widget.param.update(variant=classic)
    assert widget.variant == material
    widget.button_style = classic
    assert widget.variant == material
    assert widget._process_param_change({'variant': widget.variant})['variant'] == material


@pytest.mark.filterwarnings('ignore:.*button_style.*:PendingDeprecationWarning')
def test_variant_wins_over_button_style():
    assert Button(variant='outline', button_style='solid').variant == 'outlined'


@pytest.mark.filterwarnings('ignore:.*button_style.*:PendingDeprecationWarning')
def test_material_variant_can_change_after_button_style():
    widget = Button(button_style='solid')
    widget.variant = 'outline'
    assert widget.variant == 'outlined'


def test_fab_variant_keeps_shape_semantics():
    from panel_material_ui.widgets import Fab

    assert Fab(variant='extended').variant == 'extended'
    with pytest.raises(ValueError):
        Fab(variant='solid')


def test_button(document, comm):
    button = Button(label='Test Button')
    assert button.label == 'Test Button'
    widget = button.get_root(document, comm=comm)
    assert isinstance(widget, pn.models.esm.ReactComponent)
    button._process_events({'clicks': 1})
    assert button.clicks == 1


def test_button_event():
    button = Button(label='Button')

    events = []
    def callback(event):
        events.append(event.new)

    button.param.watch(callback, 'value')
    assert button.value == False

    event = {"clicks": 1, "value": True}
    button._process_events(event)
    assert events == [True]
    assert button.value == False


def test_button_jscallback_clicks(document, comm):
    button = Button(label='Button')
    code = 'console.log("Clicked!")'
    button.jscallback(clicks=code)

    widget = button.get_root(document, comm=comm)
    assert len(widget.js_event_callbacks) == 1
    callbacks = widget.js_event_callbacks
    assert 'dom_event' in callbacks
    assert len(callbacks['dom_event']) == 1
    assert code in callbacks['dom_event'][0].code

def test_button_js_on_click(document, comm):
    code = 'console.log("Clicked!")'
    button = Button(label='Button', js_on_click=code)

    widget = button.get_root(document, comm=comm)
    assert len(widget.js_event_callbacks) == 1
    callbacks = widget.js_event_callbacks
    assert 'dom_event' in callbacks
    assert len(callbacks['dom_event']) == 1
    assert code in callbacks['dom_event'][0].code


def test_toggle(document, comm):
    toggle = Toggle(label='Test Toggle', value=True)
    assert toggle.value == True
    assert toggle.label == 'Test Toggle'

    widget = toggle.get_root(document, comm=comm)
    assert isinstance(widget, pn.models.esm.ReactComponent)

    toggle._process_events({'value': False})
    assert toggle.value == False
    toggle._process_events({'value': True})
    assert toggle.value == True
