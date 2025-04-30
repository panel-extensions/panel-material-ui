import pytest

pytest.importorskip("playwright")

from playwright.sync_api import expect

from panel_material_ui.notifications import NotificationArea
from panel.config import config
from panel.io.state import state
from panel.layout import Row
from panel.pane import Markdown
from panel.tests.util import serve_component, wait_until
from panel.widgets import Button

pytestmark = pytest.mark.ui


def test_notifications(page):
    def callback(event):
        state.notifications.error('MyError')

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        button = Button(name='Display error')
        button.on_click(callback)
        return button

    serve_component(page, app)

    page.click('.bk-btn')

    expect(page.locator('.MuiAlert-message')).to_have_text('MyError')


def test_notifications_clear(page):
    def callback(event):
        state.notifications.error('MyError', duration=0)
        state.notifications.info('MyInfo', duration=0)

    notifications = []

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        button = Button(name='Display error')
        button.on_click(callback)
        notifications.append(state.notifications)
        return button

    serve_component(page, app)

    page.click('.bk-btn')

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
        add = Button(name='Add')
        remove = Button(name='Remove')
        add.on_click(add_notifications)
        remove.on_click(destroy_notifications)
        return Row(add, remove)

    serve_component(page, app)

    # Add and destroy two notifications
    messages = page.locator('.MuiAlert-message')
    page.locator('.bk-btn').nth(0).click()
    expect(messages).to_have_count(2)
    page.locator('.bk-btn').nth(1).click()
    expect(messages).to_have_count(1)
    page.locator('.bk-btn').nth(1).click()
    expect(messages).to_have_count(0)


def test_notifications_custom_background(page):
    def callback(event):
        state.notifications.send('Custom notification', background='#000000', duration=0)

    def app():
        config.notifications = True
        assert isinstance(state.notifications, NotificationArea)
        button = Button(name='Display error')
        button.on_click(callback)
        return button

    serve_component(page, app)

    page.click('.bk-btn')

    expect(page.locator('.MuiAlert-message')).to_have_text('Custom notification')
    expect(page.locator('.MuiPaper-root')).to_have_css('background-color', 'rgb(0, 0, 0)')


def test_notifications_custom_type(page):
    def callback(event):
        state.notifications.send('Custom notification', type='custom', duration=0)

    def app():
        config.notifications = True
        state.notifications.types = [{'type': 'custom', 'background': '#000000', 'icon': 'home'}]
        assert isinstance(state.notifications, NotificationArea)
        button = Button(name='Display error')
        button.on_click(callback)
        return button

    serve_component(page, app)

    page.click('.bk-btn')

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
        button = Button(name='Display error')
        button.on_click(callback)
        notifications.append(state.notifications)
        return button

    serve_component(page, app)

    page.click('.bk-btn')

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
        button = Button(name='Stop server')
        button.js_on_click(code="""
        Bokeh.documents[0].event_manager.send_event({'event_name': 'connection_lost', 'publish': false})
        """)
        return button

    serve_component(page, app)

    page.click('.bk-btn')

    expect(page.locator('.MuiAlert-message')).to_have_text('Disconnected!')


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
