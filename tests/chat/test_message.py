import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component
from playwright.sync_api import expect

from panel_material_ui.chat import ChatMessage

pytestmark = pytest.mark.ui


def test_chat_message_main_content(page):
    """Test that the main content (object) is rendered."""
    widget = ChatMessage(object="Hello, this is the main message content!")
    serve_component(page, widget)

    # The main content should be visible
    expect(page.get_by_text("Hello, this is the main message content!")).to_be_visible()


def test_chat_message_header_objects(page):
    """Test that header_objects are rendered."""
    widget = ChatMessage(
        object="Main content",
        header_objects=["Header Item 1", "Header Item 2"]
    )
    serve_component(page, widget)

    # Both header items should be visible
    expect(page.get_by_text("Header Item 1")).to_be_visible()
    expect(page.get_by_text("Header Item 2")).to_be_visible()


def test_chat_message_footer_objects(page):
    """Test that footer_objects are rendered."""
    widget = ChatMessage(
        object="Main content",
        footer_objects=["Footer Item 1", "Footer Item 2"]
    )
    serve_component(page, widget)

    # Both footer items should be visible
    expect(page.get_by_text("Footer Item 1")).to_be_visible()
    expect(page.get_by_text("Footer Item 2")).to_be_visible()


def test_chat_message_header_footer_layout(page):
    """#719: Header and footer objects stack; the footer precedes message icons."""
    widget = ChatMessage(
        object="Main content",
        header_objects=["Header A", "Header B"],
        footer_objects=["Footer A", "Footer B"],
        show_copy_icon=True,
    )
    serve_component(page, widget)

    header = page.get_by_text("Header A")
    header_next = page.get_by_text("Header B")
    footer = page.get_by_text("Footer A")
    footer_next = page.get_by_text("Footer B")
    icon = page.locator('.MuiIconButton-root').first
    expect(icon).to_be_visible()

    assert header.bounding_box()['y'] < header_next.bounding_box()['y']
    assert footer.bounding_box()['y'] < footer_next.bounding_box()['y']
    assert footer_next.bounding_box()['y'] < icon.bounding_box()['y']


def test_chat_message_all_sections(page):
    """Test that main content, header_objects, and footer_objects are all rendered."""
    widget = ChatMessage(
        object="This is the main message",
        header_objects=["Header content"],
        footer_objects=["Footer content"]
    )
    serve_component(page, widget)

    # Verify all three sections are rendered
    expect(page.get_by_text("This is the main message")).to_be_visible()
    expect(page.get_by_text("Header content")).to_be_visible()
    expect(page.get_by_text("Footer content")).to_be_visible()
