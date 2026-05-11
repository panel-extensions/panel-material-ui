import panel as pn

from panel_material_ui.chat import ChatMessage
from panel_material_ui.chat.input import ChatAreaInput

pn.extension()


def test_build_layout_initializes_original_object_panel():
    """_build_layout should set _original_object_panel to the created panel."""
    msg = ChatMessage(object="Hello")
    assert hasattr(msg, '_original_object_panel')
    assert msg._original_object_panel is msg._object_panel


def test_handle_edit_swaps_to_edit_area():
    """Sending 'edit' should swap _object_panel to the edit area."""
    msg = ChatMessage(object="Hello")
    original_panel = msg._object_panel
    msg._handle_msg('edit')
    assert msg._object_panel is msg._edit_area
    assert msg._original_object_panel is original_panel


def test_handle_edit_populates_edit_area_value():
    """Sending 'edit' should populate the edit area with the current content."""
    msg = ChatMessage(object="Hello")
    msg._handle_msg('edit')
    assert msg._edit_area.value == "Hello"


def test_handle_edit_toggle_cancels():
    """Sending 'edit' twice should toggle back to the original panel."""
    msg = ChatMessage(object="Hello")
    original_panel = msg._object_panel
    msg._handle_msg('edit')
    assert msg._object_panel is msg._edit_area
    msg._handle_msg('edit')
    assert msg._object_panel is original_panel


def test_submit_edit_restores_original_panel():
    """Submitting an edit should restore _object_panel to original."""
    msg = ChatMessage(object="Hello")
    msg._handle_msg('edit')
    msg._edit_area.value = "Updated"
    msg._submit_edit(None)
    assert msg._object_panel is not msg._edit_area
    assert msg._object_panel is msg._original_object_panel


def test_submit_edit_updates_object():
    """Submitting an edit should update the message object."""
    msg = ChatMessage(object="Hello")
    msg._handle_msg('edit')
    msg._edit_area.value = "Updated content"
    msg._submit_edit(None)
    assert msg.object == "Updated content"


def test_submit_edit_fires_edited_event():
    """Submitting an edit should trigger the edited event."""
    msg = ChatMessage(object="Hello")
    events = []
    msg.param.watch(lambda e: events.append(e), 'edited')
    msg._handle_msg('edit')
    msg._edit_area.value = "Edited"
    msg._submit_edit(None)
    assert len(events) == 1


def test_edit_area_is_chat_area_input():
    """The edit area should be a ChatAreaInput instance."""
    msg = ChatMessage(object="Hello")
    assert isinstance(msg._edit_area, ChatAreaInput)


def test_edit_area_has_stretch_width():
    """The edit area should have sizing_mode='stretch_width' so background stretches."""
    msg = ChatMessage(object="Hello")
    assert msg._edit_area.sizing_mode == 'stretch_width'


def test_edit_area_has_edit_css_class():
    """The edit area should have 'edit-area' CSS class for Paper width detection."""
    msg = ChatMessage(object="Hello")
    assert 'edit-area' in msg._edit_area.css_classes
