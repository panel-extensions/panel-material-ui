import param
import pytest

from panel_material_ui.widgets import ToggleIcon


def test_toggle_icon_width():
    assert isinstance(ToggleIcon.param.width, param.Integer)
    assert ToggleIcon().width is None
    assert ToggleIcon(width=100).width == 100
    with pytest.raises(ValueError):
        ToggleIcon(width=-1)


def test_toggle_icon_aria_params_sync(document, comm):
    widget = ToggleIcon(icon='star', aria_label='Favorite', aria={'describedby': 'hint'})
    model = widget.get_root(document, comm=comm)
    assert model.data.aria_label == 'Favorite'
    assert model.data.aria == {'describedby': 'hint'}
