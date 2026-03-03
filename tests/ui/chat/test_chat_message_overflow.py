import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.chat import ChatInterface
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

DETAILS_HTML = """
<details>
  <summary>Click to expand</summary>
  <p>This is expanded content that takes up space.</p>
  <p>More content here.</p>
  <p>And even more content.</p>
</details>
"""


def test_details_expand_no_overlap(page):
    """Expanding <details> should push subsequent messages down, not overlap."""
    chat = ChatInterface(height=600)
    serve_component(page, chat)

    chat.send(DETAILS_HTML, user="Assistant", respond=False)
    chat.send("Second message", user="User", respond=False)

    wait_until(lambda: len(chat.objects) == 2, page)

    # Expand details
    details_summary = page.locator("summary").first
    details_summary.click()
    expect(page.locator("details").first).to_have_attribute("open", "")

    # After expanding, messages should not overlap
    box1 = page.locator("details").first.bounding_box()
    box2 = page.get_by_text("Second message").bounding_box()
    assert box1 is not None and box2 is not None
    assert box1["y"] + box1["height"] <= box2["y"] + 5  # 5px tolerance


def test_details_expand_via_keyboard(page):
    """Keyboard expand should also reflow correctly."""
    chat = ChatInterface(height=600)
    serve_component(page, chat)

    chat.send(DETAILS_HTML, user="Assistant", respond=False)
    chat.send("Second message", user="User", respond=False)

    wait_until(lambda: len(chat.objects) == 2, page)

    summary = page.locator("summary").first
    summary.focus()
    summary.press("Enter")
    expect(page.locator("details").first).to_have_attribute("open", "")

    box1 = page.locator("details").first.bounding_box()
    box2 = page.get_by_text("Second message").bounding_box()
    assert box1 is not None and box2 is not None
    assert box1["y"] + box1["height"] <= box2["y"] + 5
