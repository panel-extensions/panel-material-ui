from unittest.mock import patch

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


def test_chat_interface_auto_scroll_limit_default():
    """auto_scroll_limit should default to 2000."""
    chat = ChatInterface()
    assert chat.auto_scroll_limit == 2000


def test_chat_interface_auto_scroll_limit_override():
    """User-provided auto_scroll_limit should not be overridden."""
    chat = ChatInterface(auto_scroll_limit=500)
    assert chat.auto_scroll_limit == 500


def test_chat_interface_chat_log_flex_stylesheet():
    """_chat_log should have the flex stylesheet for sticky input."""
    chat = ChatInterface()
    assert any("flex: 1 1 0px" in s for s in chat._chat_log.stylesheets)


def test_chat_area_input_focus():
    """ChatAreaInput.focus() should send a focus message."""
    chat = ChatInterface()
    with patch.object(chat._widget, '_send_msg') as mock_send:
        chat._widget.focus()
        mock_send.assert_called_once_with({"type": "focus"})


def test_chat_interface_focus_after_callback_state():
    """_update_input_disabled should call focus() when callback finishes."""
    import asyncio

    chat = ChatInterface()
    with patch.object(chat._widget, 'focus') as mock_focus:
        chat._widget.loading = True
        # Simulate callback finishing — loading goes to False and focus is called
        asyncio.get_event_loop().run_until_complete(chat._update_input_disabled())
        mock_focus.assert_called_once()
