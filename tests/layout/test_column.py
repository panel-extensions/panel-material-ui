from panel_material_ui.layout import Column


def test_column_scroll_params_available():
    col = Column(
        auto_scroll_limit=100,
        scroll_button_threshold=50,
        scroll_position=10,
        scroll_index=1,
        view_latest=True,
    )

    assert col.auto_scroll_limit == 100
    assert col.scroll_button_threshold == 50
    assert col.scroll_position == 10
    assert col.scroll_index == 1
    assert col.view_latest is True

def test_column_scroll_to_updates_scroll_index():
    col = Column("a", "b", "c")
    events = []
    col._send_msg = events.append

    col.scroll_to(2)

    assert events == [{"type": "scroll_to", "index": 2}]
