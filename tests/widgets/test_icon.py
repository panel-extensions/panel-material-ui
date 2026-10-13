import param
import pytest

from panel_material_ui.widgets import ToggleIcon


def test_toggle_icon_width():
    assert isinstance(ToggleIcon.param.width, param.Integer)
    assert ToggleIcon().width is None
    assert ToggleIcon(width=100).width == 100
    with pytest.raises(ValueError):
        ToggleIcon(width=-1)
