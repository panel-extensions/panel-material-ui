import time
import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.chat import ChatInterface
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_chat_interface_input_retains_focus_after_response(page):
    """Test that the input retains focus after a callback response."""
    def echo(contents, user, instance):
        time.sleep(0.1)
        return f"Echo: {contents}"

    chat = ChatInterface(callback=echo)
    serve_component(page, chat)

    textarea = page.locator("textarea").first
    textarea.click()
    textarea.fill("Hello")
    textarea.press("Enter")

    # Wait for the response to appear
    wait_until(lambda: len(chat.objects) >= 2, page)

    # The input should retain focus after the response
    expect(textarea).to_be_focused()
