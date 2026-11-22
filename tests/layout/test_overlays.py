import asyncio

from panel_material_ui.layout import Drawer, Popup


def test_popup_is_modal_by_default(document, comm):
    popup = Popup('Content')
    model = popup.get_root(document, comm=comm)
    assert popup.modal is True
    assert model.data.modal is True
    assert model.data.label is None


def test_popup_non_modal_params_sync(document, comm):
    popup = Popup('Content', modal=False, label='Details')
    model = popup.get_root(document, comm=comm)
    assert model.data.modal is False
    assert model.data.label == 'Details'
    popup.label = 'More details'
    assert model.data.label == 'More details'


def test_drawer_resize_on_toggle_default(document, comm):
    drawer = Drawer('Content')
    model = drawer.get_root(document, comm=comm)
    assert model.data.resize_on_toggle is True


def test_drawer_on_transition_callback():
    drawer = Drawer('Content')
    events = []
    drawer.on_transition(events.append)
    drawer._handle_msg({'type': 'transition', 'open': True})
    drawer._handle_msg({'type': 'transition', 'open': False})
    assert events == [True, False]


def test_drawer_on_transition_ignores_other_messages():
    drawer = Drawer('Content')
    events = []
    drawer.on_transition(events.append)
    drawer._handle_msg({'type': 'other'})
    assert events == []


def test_drawer_remove_on_transition():
    drawer = Drawer('Content')
    events = []
    drawer.on_transition(events.append)
    drawer.remove_on_transition(events.append)
    drawer._handle_msg({'type': 'transition', 'open': True})
    assert events == []


def test_drawer_on_transition_async_callback():
    drawer = Drawer('Content')
    events = []

    async def callback(open):
        events.append(open)

    drawer.on_transition(callback)

    async def run():
        drawer._handle_msg({'type': 'transition', 'open': True})
        await asyncio.sleep(0.05)

    asyncio.run(run())
    assert events == [True]
