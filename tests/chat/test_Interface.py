import panel as pn
from panel_material_ui import ChatInterface

pn.extension()


def test_chat_interface_basic_creation():
    """Test that ChatInterface can be created with basic parameters."""
    def on_send(event, instance):
        instance.send("Received new message.")

    chat_interface = ChatInterface(
        send_callback=on_send,
    )

    chat_interface._click_send(None, chat_interface)
    assert chat_interface.objects[0].object == "Received new message."
