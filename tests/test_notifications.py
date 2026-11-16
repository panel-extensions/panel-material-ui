import gc

from bokeh.document import Document

from panel_material_ui.notifications import MuiNotification, NotificationArea


def _payload(area, exclude=None):
    return [
        {k: v for k, v in n.param.values().items() if k not in ('name', 'notification_area')}
        for n in area.notifications if n is not exclude
    ]


def test_notification_area_frontend_sync_reuses_notifications():
    area = NotificationArea()
    area.get_root(Document())
    sent = [area.send(f'msg {i}') for i in range(3)]
    area._process_events({'notifications': _payload(area)})
    assert area.notifications == sent
    assert set(area._notification_watchers) == set(sent)


def test_notification_area_frontend_close_releases_notifications():
    area = NotificationArea()
    area.get_root(Document())
    for i in range(10):
        area.send(f'msg {i}')
    while area.notifications:
        closing = area.notifications[0]
        area._process_events({'notifications': _payload(area, exclude=closing)})
        area._handle_msg({'type': 'destroy', 'uuid': closing._uuid})
    del closing
    gc.collect()
    assert area._notification_watchers == {}
    assert not any(
        isinstance(o, MuiNotification) and o.notification_area is area
        for o in gc.get_objects()
    )


def test_notification_area_destroy_removes_notification():
    area = NotificationArea()
    notification = area.send('msg')
    notification.destroy()
    assert area.notifications == []
    assert area._notification_watchers == {}


def test_notification_area_clear_assigned_notifications():
    area = NotificationArea()
    notification = MuiNotification(message='x', notification_area=area)
    area.notifications = [notification]
    assert notification in area._notification_watchers
    area.clear()
    assert area.notifications == []
    assert area._notification_watchers == {}
