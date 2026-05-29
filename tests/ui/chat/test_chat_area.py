import time
import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.chat import ChatAreaInput
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_chat_area_pending_uploads(page):
    widget = ChatAreaInput()
    serve_component(page, widget)

    # Initially no pending uploads
    assert widget.pending_uploads == 0

    file_input = page.locator('input[type="file"]')

    # Upload first file
    file_input.set_input_files({"name": "file1.txt", "mimeType": "text/plain", "buffer": b"content1"})
    wait_until(lambda: widget.pending_uploads == 1, page)

    # Upload second file
    file_input.set_input_files({"name": "file2.txt", "mimeType": "text/plain", "buffer": b"content2"})
    wait_until(lambda: widget.pending_uploads == 2, page)


def test_chat_area_pending_uploads_reset_after_sync(page):
    widget = ChatAreaInput()
    serve_component(page, widget)

    file_input = page.locator('input[type="file"]')
    file_input.set_input_files({"name": "test.txt", "mimeType": "text/plain", "buffer": b"content"})

    wait_until(lambda: widget.pending_uploads == 1, page)

    # Sync files
    widget.sync()

    # Pending uploads should reset to 0 after sync
    wait_until(lambda: widget.pending_uploads == 0, page)
    assert "test.txt" in widget.value_uploaded


def test_chat_area_transfer(page):
    widget = ChatAreaInput()
    serve_component(page, widget)

    file_input = page.locator('input[type="file"]')
    file_name = "test_file.txt"
    file_content = b"Hello world"

    file_input.set_input_files({"name": file_name, "mimeType": "text/plain", "buffer": file_content})

    # Wait for the file to be processed by the client
    expect(page.locator('.MuiChip-label .MuiTypography-root')).to_have_text(f"{file_name} (11 B)")

    # Verify value_uploaded is initially empty
    assert widget.value_uploaded == {}

    # Trigger sync programmatically
    widget.sync()

    # Wait for the upload to complete and sync back to python
    wait_until(lambda: file_name in widget.value_uploaded, page)

    # Verify content
    assert widget.value_uploaded[file_name]['value'] == file_content
    assert widget.value_uploaded[file_name]['mime_type'] == "text/plain"


def test_chat_area_send_syncs_files(page):
    widget = ChatAreaInput()
    serve_component(page, widget)

    file_input = page.locator('input[type="file"]')
    file_name = "test_send.txt"
    file_content = b"Send me"

    file_input.set_input_files({"name": file_name, "mimeType": "text/plain", "buffer": file_content})
    expect(page.locator('.MuiChip-label')).to_contain_text(file_name)

    # Click send button
    page.locator('button').last.click()

    wait_until(lambda: file_name in widget.value_uploaded, page)
    assert widget.value_uploaded[file_name]['value'] == file_content



def test_chat_area_clears_on_send_button_click(page):
    """Test that ChatAreaInput clears after clicking the send button."""
    widget = ChatAreaInput()
    serve_component(page, widget)

    # Locate the textarea (first one is the actual input, second is hidden for measuring)
    textarea = page.locator('textarea').first

    # Type a message
    test_message = "Hello, this is a test message"
    textarea.fill(test_message)

    # Verify the message is in the textarea
    expect(textarea).to_have_value(test_message)

    # Click the send button (last button is the send button)
    send_button = page.locator('button').last
    send_button.click()

    # Verify the textarea is cleared
    expect(textarea).to_have_value("")


def test_chat_area_clears_on_enter_key(page):
    """Test that ChatAreaInput clears after pressing Enter."""
    widget = ChatAreaInput(enter_sends=True)
    serve_component(page, widget)

    # Locate the textarea (first one is the actual input)
    textarea = page.locator('textarea').first

    # Type a message
    test_message = "Testing enter key submission"
    textarea.fill(test_message)

    # Verify the message is in the textarea
    expect(textarea).to_have_value(test_message)

    # Press Enter to send
    textarea.press("Enter")

    # Verify the textarea is cleared
    expect(textarea).to_have_value("")


def test_chat_area_clears_on_ctrl_enter_key(page):
    """Test that ChatAreaInput clears after pressing Ctrl+Enter when enter_sends is False."""
    widget = ChatAreaInput(enter_sends=False)
    serve_component(page, widget)

    # Locate the textarea (first one is the actual input)
    textarea = page.locator('textarea').first

    # Type a message
    test_message = "Testing Ctrl+Enter submission"
    textarea.fill(test_message)

    # Verify the message is in the textarea
    expect(textarea).to_have_value(test_message)

    # Press Ctrl+Enter to send
    textarea.press("Control+Enter")

    # Verify the textarea is cleared
    expect(textarea).to_have_value("")


def test_chat_area_clears_value_input_on_send(page):
    """Test that both value and value_input are cleared after sending."""
    widget = ChatAreaInput()
    serve_component(page, widget)

    # Locate the textarea (first one is the actual input)
    textarea = page.locator('textarea').first

    # Type a message
    test_message = "Check value_input clearing"
    textarea.fill(test_message)

    # Wait for value_input to update
    wait_until(lambda: widget.value_input == test_message, page)

    # Click send
    send_button = page.locator('button').last
    send_button.click()

    # Wait for clearing to happen
    wait_until(lambda: widget.value_input == "", page)

    # Verify both value and value_input are cleared
    assert widget.value_input == ""
    assert widget.value == ""


def test_chat_area_clears_with_files_attached(page):
    """Test that ChatAreaInput clears after sending a message with files."""
    widget = ChatAreaInput(enable_upload=True)
    serve_component(page, widget)

    # Locate the textarea (first one is the actual input) and file input
    textarea = page.locator('textarea').first
    file_input = page.locator('input[type="file"]')

    # Upload a file
    file_input.set_input_files({"name": "test.txt", "mimeType": "text/plain", "buffer": b"file content"})

    # Wait for the file chip to appear
    expect(page.locator('.MuiChip-label')).to_contain_text("test.txt")

    # Type a message
    test_message = "Message with attachment"
    textarea.fill(test_message)

    # Verify the message is in the textarea
    expect(textarea).to_have_value(test_message)

    # Click send
    send_button = page.locator('button').last
    send_button.click()

    # Verify the textarea is cleared
    expect(textarea).to_have_value("")

    # Verify file was uploaded and the file chip is removed
    wait_until(lambda: "test.txt" in widget.value_uploaded, page)
    wait_until(lambda: widget.pending_uploads == 0, page)


def test_chat_area_preserves_text_on_shift_enter(page):
    """Test that ChatAreaInput does NOT clear when Shift+Enter is pressed (creates new line)."""
    widget = ChatAreaInput(enter_sends=True)
    serve_component(page, widget)

    # Locate the textarea (first one is the actual input)
    textarea = page.locator('textarea').first

    # Type a message
    test_message = "Line 1"
    textarea.fill(test_message)

    # Press Shift+Enter to create a new line (should NOT submit)
    textarea.press("Shift+Enter")

    # Type more text
    textarea.type("Line 2")

    # The text should still be there (not cleared)
    expect(textarea).to_contain_text("Line 1")
    expect(textarea).to_contain_text("Line 2")


def test_chat_area_disabled_does_not_clear_on_send(page):
    """Test that disabled ChatAreaInput does not submit or clear."""
    widget = ChatAreaInput(disabled=True)
    serve_component(page, widget)

    # Locate the textarea (first one is the actual input)
    textarea = page.locator('textarea').first
    send_button = page.locator('button').last

    # Verify textarea is disabled
    expect(textarea).to_be_disabled()

    # Try to click send button (it should be disabled)
    expect(send_button).to_be_disabled()
