import pytest

from panel_material_ui.layout import Paper
from panel_material_ui.pane import Typography
from panel_material_ui.wrappers import Fullscreen


def test_fullscreen_defaults():
    wrapper = Fullscreen()
    assert wrapper.active is False
    assert wrapper.disabled is False
    assert wrapper.toolbar == []
    assert wrapper.hide_delay == 2500
    assert wrapper.inert is True
    assert wrapper.native is False
    assert wrapper.placement == "top-right"
    assert wrapper.show_button is True
    assert wrapper.supported is False
    assert wrapper.toggle_class == ""


def test_fullscreen_object_positional():
    paper = Paper("Dashboard")
    assert Fullscreen(paper).object is paper


def test_fullscreen_toggle():
    wrapper = Fullscreen(Paper("Dashboard"))
    wrapper.toggle()
    assert wrapper.active is True
    wrapper.toggle()
    assert wrapper.active is False


@pytest.mark.parametrize("name", ["native", "supported"])
def test_fullscreen_browser_state_is_readonly(name):
    wrapper = Fullscreen()
    with pytest.raises(TypeError):
        setattr(wrapper, name, True)


def test_fullscreen_hide_delay_none():
    assert Fullscreen(hide_delay=None).hide_delay is None


def test_fullscreen_placement_validated():
    with pytest.raises(ValueError):
        Fullscreen(placement="middle")


def test_fullscreen_renders_toolbar(document, comm):
    wrapper = Fullscreen(Paper("Dashboard"), toolbar=[Typography("Status")])
    model = wrapper.get_root(document, comm=comm)
    assert len(model.data.toolbar) == 1
    assert model.data.object is not None


def test_fullscreen_class_names():
    assert Fullscreen.TOGGLE_CLASS == "pmui-fullscreen-toggle"
    assert Fullscreen.EXIT_CLASS == "pmui-fullscreen-exit"
    assert Fullscreen.KEEP_CLASS == "pmui-fullscreen-keep"
    assert Fullscreen.TOGGLE_EVENT == "pmui:fullscreen"


def test_fullscreen_browser_updates_readonly_state(document, comm):
    wrapper = Fullscreen(Paper("Dashboard"))
    wrapper.get_root(document, comm=comm)
    wrapper._process_events({"native": True, "supported": True})
    assert wrapper.native is True
    assert wrapper.supported is True
