import panel as pn
from panel_material_ui import ChatInterface

pn.extension()


def test_chat_interface_basic_creation():
    """Test that ChatInterface can be created with basic parameters."""
    def on_click_send(event, instance):
        instance.send("Received new message.")

    chat_interface = ChatInterface(
        on_submit=on_click_send,
    )

    chat_interface._click_send(None, chat_interface)
    assert chat_interface.objects[0].object == "Received new message."


def test_chat_interface_default_sizing_mode():
    """Test that ChatInterface defaults to stretch_both for proper sticky input layout."""
    chat = ChatInterface()
    assert chat.sizing_mode == "stretch_both"
    assert chat._chat_log.height_policy == "max"


def test_chat_interface_sizing_mode_override():
    """Test that ChatInterface respects explicit sizing_mode."""
    chat = ChatInterface(sizing_mode="stretch_width")
    assert chat.sizing_mode == "stretch_width"


def test_chat_interface_height_override():
    """Test that ChatInterface respects explicit height (does not set stretch_both)."""
    chat = ChatInterface(height=400)
    assert chat.height == 400
    assert chat.sizing_mode != "stretch_both"
