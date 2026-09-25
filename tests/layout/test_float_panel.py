import panel_material_ui as pmui


def test_float_panel_defaults_and_list_api():
    """FloatPanel is exported and accepts regular Panel layout children (#679)."""
    panel = pmui.FloatPanel("First")

    assert panel.position == (24, 24)
    assert panel.width == panel.height == 0
    assert panel.sizing_mode == "fixed"
    assert len(panel.objects) == 1

    panel.append("Second")
    assert len(panel.objects) == 2
    panel.position = (60, 80)
    assert panel.position == (60, 80)
