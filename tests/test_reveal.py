import pytest

from panel_material_ui import Reveal


def test_reveal_defaults():
    reveal = Reveal()
    assert reveal.color == "primary"
    assert reveal.duration == 2200
    assert reveal.width == 0
    assert reveal.height == 0
    assert reveal.margin == 0


def test_reveal_scroll_to_sends_message():
    reveal = Reveal()
    sent = []
    reveal._send_msg = sent.append
    reveal.scroll_to("late")
    assert sent == [{"css_class": "late", "highlight": True, "focus": False, "block": "center"}]


def test_reveal_scroll_to_options():
    reveal = Reveal()
    sent = []
    reveal._send_msg = sent.append
    reveal.scroll_to("late", highlight=False, focus=True, block="start")
    assert sent == [{"css_class": "late", "highlight": False, "focus": True, "block": "start"}]


def test_reveal_color_validated():
    with pytest.raises(ValueError):
        Reveal(color="rainbow")


def test_reveal_renders(document, comm):
    model = Reveal(color="error").get_root(document, comm=comm)
    assert model.data.color == "error"
