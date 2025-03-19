import panel as pn

from panel_material_ui.widgets import Button, Toggle


def test_button(document, comm):
    button = Button(label='Test Button')
    assert button.label == 'Test Button'
    widget = button.get_root(document, comm=comm)
    assert isinstance(widget, pn.models.esm.ReactComponent)
    button._process_events({'clicks': 1})
    assert button.clicks == 1


def test_button_event():
    button = Button(name='Button')

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
    button = Button(name='Button')
    code = 'console.log("Clicked!")'
    button.jscallback(clicks=code)

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
