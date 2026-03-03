import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.chat import ChatInterface
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


# --- Focus tests (#578) ---

def test_chat_interface_focus_after_callback(page):
    """Input should retain focus after callback response renders."""
    def echo(contents, user, instance):
        return f"Echo: {contents}"

    chat = ChatInterface(callback=echo)
    serve_component(page, chat)

    input_locator = page.locator("textarea").first
    input_locator.click()
    input_locator.fill("Hello")
    input_locator.press("Enter")

    wait_until(lambda: len(chat.objects) == 2, page)
    expect(input_locator).to_be_focused(timeout=5000)


def test_chat_interface_focus_after_rapid_sends(page):
    """Focus should recover after multiple rapid sends."""
    def echo(contents, user, instance):
        return f"Echo: {contents}"

    chat = ChatInterface(callback=echo)
    serve_component(page, chat)

    input_locator = page.locator("textarea").first
    for i in range(3):
        input_locator.click()
        input_locator.fill(f"Message {i}")
        input_locator.press("Enter")
        wait_until(lambda i=i: len(chat.objects) == (i + 1) * 2, page)

    expect(input_locator).to_be_focused(timeout=5000)


# --- Auto-scroll and sticky input tests (#580) ---

def test_chat_interface_input_visible_with_many_messages(page):
    """Input should remain visible at the bottom with many messages."""
    chat = ChatInterface(height=600)
    serve_component(page, chat)

    for i in range(25):
        chat.send(f"Message {i}", user="User", respond=False)

    # Wait for the last message to appear in the DOM
    expect(page.get_by_text("Message 24")).to_be_attached(timeout=30000)

    input_box = page.locator("textarea").first.bounding_box()
    viewport = page.viewport_size
    assert input_box is not None, "Input textarea not found"
    assert input_box["y"] + input_box["height"] <= viewport["height"], (
        f"Input bottom ({input_box['y'] + input_box['height']}) exceeds viewport ({viewport['height']})"
    )


def test_chat_interface_auto_scroll_on_new_message(page):
    """New messages should auto-scroll into view when user is near bottom."""
    def echo(contents, user, instance):
        return f"Echo: {contents}"

    chat = ChatInterface(callback=echo, height=600)
    serve_component(page, chat)

    for i in range(20):
        chat.send(f"Message {i}", user="User", respond=False)

    # Wait for the last pre-filled message to render
    expect(page.get_by_text("Message 19")).to_be_attached(timeout=30000)

    input_locator = page.locator("textarea").first
    input_locator.click()
    input_locator.fill("New message")
    input_locator.press("Enter")

    wait_until(lambda: len(chat.objects) == 22, page)

    # The latest message should be visible
    last_msg = page.get_by_text("Echo: New message")
    expect(last_msg).to_be_visible(timeout=5000)
