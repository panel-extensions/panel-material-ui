import panel_material_ui as pmui
import pytest


def test_float_panel_defaults_and_list_api():
    """FloatPanel is exported and accepts regular Panel layout children (#679)."""
    panel = pmui.FloatPanel("First")

    assert panel.position == "right-top"
    assert panel.contained is True
    assert panel.offsetx == panel.offsety == 0
    assert panel.status == "normalized"
    assert panel.controls == ["minimize", "maximize", "close"]
    assert panel.width is None and panel.height is None
    assert len(panel.objects) == 1

    panel.append("Second")
    assert len(panel.objects) == 2
    panel.position = "center"
    panel.status = "minimized"
    assert panel.position == "center"
    assert panel.status == "minimized"


def test_float_panel_controls_validate_options():
    """Unknown window controls are rejected instead of silently disappearing (#679)."""
    with pytest.raises(ValueError):
        pmui.FloatPanel(controls=["unknown"])
