import uuid
from typing import Any

import param

from .base import MaterialComponent


class Notification(param.Parameterized):

    background = param.Color(default=None)

    duration = param.Integer(default=3000, constant=True)

    icon = param.String(default=None)

    message = param.String(default='', constant=True)

    notification_type = param.String(default='default', constant=True, label='type')

    _rendered = param.Boolean(default=False)

    _destroyed = param.Boolean(default=False)

    _uuid = param.String(default=None)

    def __init__(self, **params):
        if '_uuid' not in params:
            params['_uuid'] = uuid.uuid4().hex
        super().__init__(**params)

    def destroy(self) -> None:
        pass


class NotificationArea(MaterialComponent):

    js_events = param.Dict(default={}, doc="""
        A dictionary that configures notifications for specific Bokeh Document
        events, e.g.:

          {'connection_lost': {'type': 'error', 'message': 'Connection Lost!', 'duration': 5}}

        will trigger a warning on the Bokeh ConnectionLost event.""")

    max_notifications = param.Integer(default=10, doc="""
        The maximum number of notifications to display at once.""")

    notifications = param.List(item_type=Notification)

    position = param.Selector(default='bottom-right', objects=[
        'bottom-right', 'bottom-left', 'bottom-center', 'top-left',
        'top-right', 'top-center'])

    _esm_base = "NotificationArea.jsx"

    _notification_type = Notification

    def __init__(self, **params):
        super().__init__(**params)
        self._notification_watchers = {}

    def _process_events(self, events: dict[str, Any]) -> None:
        if 'notifications' in events:
            old = {n._uuid: n for n in self.notifications}
            notifications = []
            for notification in events.pop('notifications'):
                if notification._uuid in old:
                    notifications.append(old[notification._uuid])
            self.notifications[:] = notifications
        return super()._process_events(events)

    def send(self, message, duration=3000, type='default', background=None, icon=None):
        """
        Sends a notification to the frontend.
        """
        notification = self._notification_type(
            message=message, duration=duration, notification_type=type,
            background=background, icon=icon
        )
        self._notification_watchers[notification] = (
            notification.param.watch(self._remove_notification, '_destroyed')
        )
        self.notifications.append(notification)
        self.param.trigger('notifications')
        return notification

    def error(self, message, duration=3000):
        return self.send(message, duration, type='error')

    def info(self, message, duration=3000):
        return self.send(message, duration, type='info')

    def success(self, message, duration=3000):
        return self.send(message, duration, type='success')

    def warning(self, message, duration=3000):
        return self.send(message, duration, type='warning')

    def clear(self):
        self._clear += 1
        self.notifications[:] = []

    def _remove_notification(self, event):
        if event.obj in self.notifications:
            self.notifications.remove(event.obj)
        event.obj.param.unwatch(self._notification_watchers.pop(event.obj))
