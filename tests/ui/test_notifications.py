import pytest

pytest.importorskip("playwright")

import panel.io.document
import panel.io.server
from panel.config import config
from panel.io.state import state
from panel.layout import Row
from panel.pane import Markdown
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.notifications import NotificationArea
from panel_material_ui.widgets import Button

pytestmark = pytest.mark.ui

# Panel releases that write a locked callback's changes in one message
# (holoviz/panel#9106) but still send changes to models the client was
# never sent (fixed by holoviz/panel#8906) reject the whole patch.
PANEL_DROPS_ONLOAD_PATCH = (
    hasattr(panel.io.server, '_serialize_patches') and
    not hasattr(panel.io.document, '_drop_unsent_model_changes')
)


def test_notifications(page):
    def callback(event):
        state.notifications.error('MyError')

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        button = Button(label='Display error')
        button.on_click(callback)
        return button

    serve_component(page, app)

    page.click('.MuiButton-root')

    expect(page.locator('.MuiAlert-message')).to_have_text('MyError')


def test_notifications_clear(page):
    def callback(event):
        state.notifications.error('MyError', duration=0)
        state.notifications.info('MyInfo', duration=0)

    notifications = []

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        button = Button(label='Display error')
        button.on_click(callback)
        notifications.append(state.notifications)
        return button

    serve_component(page, app)

    page.click('.MuiButton-root')

    expect(page.locator('.MuiAlert-message')).to_have_count(2)

    notifications[0].clear()

    expect(page.locator('.MuiAlert-message')).to_have_count(0)


def test_notifications_destroy(page):

    notifications = []

    def add_notifications(event):
        notifications.extend([
            state.notifications.error('MyError', duration=0),
            state.notifications.info('MyInfo', duration=0),
        ])

    def destroy_notifications(event):
        notifications.pop(0).destroy()

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        add = Button(label='Add')
        remove = Button(label='Remove')
        add.on_click(add_notifications)
        remove.on_click(destroy_notifications)
        return Row(add, remove)

    serve_component(page, app)

    # Add and destroy two notifications
    messages = page.locator('.MuiAlert-message')
    page.locator('.MuiButton-root').nth(0).click()
    expect(messages).to_have_count(2)
    page.locator('.MuiButton-root').nth(1).click()
    expect(messages).to_have_count(1)
    page.locator('.MuiButton-root').nth(1).click()
    expect(messages).to_have_count(0)


def test_notifications_custom_background(page):
    def callback(event):
        state.notifications.send('Custom notification', background='#000000', duration=0)

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        button = Button(label='Display error')
        button.on_click(callback)
        return button

    serve_component(page, app)

    page.click('.MuiButton-root')

    expect(page.locator('.MuiAlert-message')).to_have_text('Custom notification')
    expect(page.locator('.MuiPaper-root')).to_have_css('background-color', 'rgb(0, 0, 0)')


def test_notifications_custom_type(page):
    def callback(event):
        state.notifications.send('Custom notification', type='custom', duration=0)

    def app():
        config.notifications = True
        state.notifications.types = [{'type': 'custom', 'background': '#000000', 'icon': 'home'}]
        assert isinstance(state.notifications, NotificationArea)
        button = Button(label='Display error')
        button.on_click(callback)
        return button

    serve_component(page, app)

    page.click('.MuiButton-root')

    expect(page.locator('.MuiAlert-message')).to_have_text('Custom notification')
    expect(page.locator('.MuiPaper-root')).to_have_css('background-color', 'rgb(0, 0, 0)')
    expect(page.locator('.MuiAlert-icon')).to_have_text('home')


def test_notifications_dismiss(page):
    def callback(event):
        state.notifications.error('MyError', duration=0)

    notifications = []

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        button = Button(label='Display error')
        button.on_click(callback)
        notifications.append(state.notifications)
        return button

    serve_component(page, app)

    page.click('.MuiButton-root')

    expect(page.locator('.MuiAlert-message')).to_have_text('MyError')

    page.click('.MuiIconButton-root')

    expect(page.locator('.MuiAlert-message')).to_be_hidden()

    wait_until(lambda: len(notifications[0].notifications) == 0, page)


def test_ready_notification(page):
    def app():
        config.ready_notification = 'Ready!'
        assert isinstance(state.notifications, NotificationArea)
        return Markdown('Ready app')

    serve_component(page, app)

    expect(page.locator('.MuiAlert-message')).to_have_text('Ready!')


def test_disconnect_notification(page):
    def app():
        config.disconnect_notification = 'Disconnected!'
        assert isinstance(state.notifications, NotificationArea)
        button = Button(label='Stop server')
        button.js_on_click(code="""
        Bokeh.documents[0].event_manager.send_event({'event_name': 'connection_lost', 'publish': false})
        """)
        return button

    serve_component(page, app)

    page.click('.MuiButton-root')

    expect(page.locator('.MuiAlert-message')).to_have_text('Disconnected!')


@pytest.mark.xfail(
    PANEL_DROPS_ONLOAD_PATCH, strict=False,
    reason="Panel bug from holoviz/panel#9106, fixed by holoviz/panel#8906"
)
def test_onload_notification(page):
    def onload_callback():
        state.notifications.warning("Warning", duration=0)
        state.notifications.info("Info", duration=0)

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        state.onload(onload_callback)
        return Markdown("# Hello world")

    serve_component(page, app)

    expect(page.locator('.MuiAlert-message')).to_have_count(2)
    expect(page.locator('.MuiAlert-colorWarning .MuiAlert-message')).to_have_text("Warning")
    expect(page.locator('.MuiAlert-colorInfo .MuiAlert-message')).to_have_text("Info")


def test_notifications_dismiss_releases_watchers(page):
    area = NotificationArea()
    serve_component(page, area)

    for i in range(5):
        area.send(f'Message {i}', duration=0)

    expect(page.locator('.MuiAlert-message')).to_have_count(5)

    for _ in range(5):
        page.locator('.MuiAlert-action .MuiIconButton-root').first.click()

    expect(page.locator('.MuiAlert-message')).to_have_count(0)
    wait_until(lambda: area.notifications == [] and area._notification_watchers == {}, page)


def test_notifications_remount_removes_handlers(page):
    area = NotificationArea()
    row = Row(area)
    serve_component(page, row)

    def count_callbacks():
        return page.evaluate("""() => {
          const callbacks = Bokeh.documents[0]._document_callbacks
          return (callbacks.get('connection_lost') || []).length
        }""")

    wait_until(lambda: count_callbacks() > 0, page)
    initial = count_callbacks()

    for _ in range(3):
        row.objects = []
        page.wait_for_timeout(200)
        row.objects = [area]
        page.wait_for_timeout(200)

    area.send('After remount', duration=0)
    expect(page.locator('.MuiAlert-message')).to_have_text('After remount')
    expect(page.locator('.MuiAlert-message')).to_have_count(1)
    assert count_callbacks() == initial
