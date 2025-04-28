from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

import param
from bokeh.models.callbacks import CustomJS
from panel.io.datamodel import _DATA_MODELS, construct_data_model
from panel.io.notifications import Notification as _Notification
from panel.io.notifications import NotificationAreaBase
from panel.io.state import _state
from panel.layout import Column

from .base import MaterialComponent
from .widgets import Button, ColorPicker, NumberInput, Select, TextInput

if TYPE_CHECKING:
    from bokeh.document import Document
    from bokeh.models import Model
    from pyviz_comms import Comm


class MuiNotification(_Notification):

    _uuid = param.String(default=None)

    def __init__(self, **params):
        if '_uuid' not in params:
            params['_uuid'] = uuid.uuid4().hex
        super().__init__(**params)


class NotificationArea(MaterialComponent, NotificationAreaBase):

    notifications = param.List(item_type=(MuiNotification, dict))

    types = param.List(default=[], doc="""
        Custom notification types.

        Each type is a dictionary with the following keys:
        - 'type': The type of the notification.
        - 'background': The background color of the notification.
        - 'icon': The icon of the notification.
        """)

    _esm_base = "NotificationArea.jsx"

    _notification_type = MuiNotification

    _rename = {"max_notifications": "max_notifications", "anchor": "anchor"}

    _root_node = '#notistack-container'

    def __init__(self, **params):
        super().__init__(**params)
        self._notification_watchers = {}

    def _get_model(
        self, doc: Document, root: Model | None = None,
        parent: Model | None = None, comm: Comm | None = None
    ) -> Model:
        model = super()._get_model(doc, root, parent, comm)
        for event, notification in self.js_events.items():
            doc.js_on_event(event, CustomJS(code=f"""
            const config = {{
              message: {notification['message']!r},
              duration: {notification.get('duration', 0)},
              notification_type: {notification['type']!r},
              _destroyed: false,
              _uuid: Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
            }}
            notifications.document.event_manager.trigger(
              {{event_name: 'esm_event', model: notifications, data: {{type: 'enqueue', notification: config}}}}
            )
            notifications.data.notifications = [...notifications.data.notifications, config]
            """, args={'notifications': model}))
        return model

    def _process_events(self, events: dict[str, Any]) -> None:
        if 'notifications' in events:
            old = {n._uuid: n for n in self.notifications}
            notifications = []
            for notification in events.pop('notifications'):
                if isinstance(notification, dict):
                    notification = MuiNotification(notification_area=self, **notification)
                    self._notification_watchers[notification] = (
                        notification.param.watch(self._remove_notification, '_destroyed')
                    )
                if notification._uuid in old:
                    notifications.append(old[notification._uuid])
                else:
                    notifications.append(notification)
            self.notifications = notifications
        return super()._process_events(events)

    def _get_properties(self, doc):
        props = super()._get_properties(doc)
        props['root_node'] = '#notistack-container'
        return props

    @classmethod
    def demo(cls, **params):
        """
        Generates a layout which allows demoing the component.
        """
        msg = TextInput(label='Message', value='This is a message', **params)
        duration = NumberInput(label='Duration', value=0, end=10000, **params)
        ntype = Select(
            label='Type', options=['info', 'warning', 'error', 'success', 'custom'],
            value='info', **params
        )
        background = ColorPicker(label='Color', value='#000000', **params)
        button = Button(label='Notify', **params)
        notifications = cls()
        button.js_on_click(
            args={
                'notifications': notifications, 'msg': msg, 'duration': duration,
                'ntype': ntype, 'color': background
            }, code="""
            const config = {
              message: msg.data.value,
              duration: duration.data.value,
              notification_type: ntype.data.value,
              _destroyed: false,
              _uuid: Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15)
            }
            if (ntype.data.value === 'custom') {
              config.background = color.data.value
            }
            notifications.document.event_manager.trigger({event_name: 'esm_event', model: notifications, data: {type: 'enqueue', notification: config}})
            notifications.data.notifications = [...notifications.data.notifications, config]
            """
        )

        return Column(msg, duration, ntype, background, button, notifications)

    def send(self, message, duration=3000, type='default', background=None, icon=None):
        """
        Sends a notification to the frontend.
        """
        notification = self._notification_type(
            message=message, duration=duration, notification_type=type,
            background=background, icon=icon, notification_area=self
        )
        self._notification_watchers[notification] = (
            notification.param.watch(self._remove_notification, '_destroyed')
        )
        self.notifications.append(notification)
        self.param.trigger('notifications')
        self._send_msg({
            'type': 'enqueue',
            'notification': {
                k: v for k, v in notification.param.values().items()
                if k != 'notification_area'
            }
        })
        return notification

    def clear(self):
        for notification in self.notifications:
            notification.param.unwatch(self._notification_watchers.pop(notification))
            self._send_msg({'type': 'destroy', 'uuid': notification._uuid})
        self.notifications = []

    def _handle_msg(self, msg):
        if msg['type'] == 'destroy':
            self.notifications = [n for n in self.notifications if n._uuid != msg['uuid']]

    def _remove_notification(self, event):
        if event.obj in self.notifications:
            self.notifications.remove(event.obj)
        event.obj.param.unwatch(self._notification_watchers.pop(event.obj))
        self.param.trigger('notifications')
        self._send_msg({'type': 'destroy', 'uuid': event.obj._uuid})


_state._notification_type = NotificationArea
_DATA_MODELS[MuiNotification] = construct_data_model(MuiNotification, f'MuiNotification{uuid.uuid4().hex}')
