import panel_material_ui as pmui


def test_float_panel_defaults_and_list_api():
    """FloatPanel is exported and accepts regular Panel layout children (#679)."""
    panel = pmui.FloatPanel("First")

    assert panel.position == "right-top"
    assert panel.contained is True
    assert panel.offsetx == panel.offsety == 0
    assert panel.status == "normalized"
    assert panel.show_close_button and panel.show_maximize_button and panel.show_minimize_button
    assert panel.width is None and panel.height is None
    assert len(panel.objects) == 1

    panel.append("Second")
    assert len(panel.objects) == 2
    panel.position = "center"
    panel.status = "minimized"
    assert panel.position == "center"
    assert panel.status == "minimized"
