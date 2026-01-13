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
