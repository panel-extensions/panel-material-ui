from bokeh.document import Document
from panel.util import edit_readonly
from panel_material_ui.layout import Feed


def test_feed_scroll_to_latest_keeps_load_buffer_when_window_lags():
    feed = Feed(*range(100), load_buffer=10)
    model = feed.get_root(Document())
    sent = []
    feed._send_msg = sent.append

    # A slow frontend last reported a child far behind the newest one.
    with edit_readonly(feed):
        feed.visible_range = (40, 41)
    assert feed._last_synced == (30, 51)

    feed.objects = [*feed.objects, *range(100, 103)]
    feed.scroll_to_latest()

    assert feed._last_synced == (92, 103)
    assert len(model.data.objects) == 11
    assert sent[-1]["rerender"] is True
