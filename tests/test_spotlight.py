import pytest

from panel_material_ui import Spotlight


def test_spotlight_defaults():
    spotlight = Spotlight()
    assert spotlight.color == "primary"
    assert spotlight.duration == 2200
    assert spotlight.width == 0
    assert spotlight.height == 0
    assert spotlight.margin == 0


def test_spotlight_scroll_to_sends_message():
    spotlight = Spotlight()
    sent = []
    spotlight._send_msg = sent.append
    spotlight.scroll_to("late")
    assert sent == [{"css_class": "late", "highlight": True, "focus": False, "block": "center"}]


def test_spotlight_scroll_to_options():
    spotlight = Spotlight()
    sent = []
    spotlight._send_msg = sent.append
    spotlight.scroll_to("late", highlight=False, focus=True, block="start")
    assert sent == [{"css_class": "late", "highlight": False, "focus": True, "block": "start"}]


def test_spotlight_color_validated():
    with pytest.raises(ValueError):
        Spotlight(color="rainbow")


def test_spotlight_renders(document, comm):
    model = Spotlight(color="error").get_root(document, comm=comm)
    assert model.data.color == "error"
