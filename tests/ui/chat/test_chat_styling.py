import re

import pytest

pytest.importorskip("playwright")

from panel.pane import Markdown
from panel.tests.util import serve_component, wait_until
from panel.viewable import Viewer
from playwright.sync_api import expect

from panel_material_ui.chat import ChatAreaInput, ChatFeed, ChatInterface, ChatMessage
from panel_material_ui.layout import Column

pytestmark = pytest.mark.ui


def _bubble(page, text):
    return page.locator(".MuiPaper-root").filter(has_text=text).last


def test_chat_interface_user_message_right_aligned(page):
    chat = ChatInterface(user="Philipp", width=800)
    chat.send("From me", user="Philipp", respond=False)
    chat.send("From the assistant", user="Assistant", respond=False)
    serve_component(page, chat)

    own = _bubble(page, "From me").bounding_box()
    other = _bubble(page, "From the assistant").bounding_box()
    assert own["x"] > 400
    assert other["x"] < 400


def test_chat_interface_messages_aligned_with_input_when_wide(page):
    page.set_viewport_size({"width": 1900, "height": 800})
    chat = ChatInterface(sizing_mode="stretch_both")
    chat.send("From me", respond=False)
    chat.send("From the assistant", user="Assistant", respond=False)
    serve_component(page, chat)

    own = _bubble(page, "From me").bounding_box()
    other = page.get_by_text("From the assistant").bounding_box()
    textarea = page.locator(".MuiOutlinedInput-root").first.bounding_box()
    # The avatar column sits between the bubble and the edge of the column.
    assert abs(textarea["x"] + textarea["width"] - (own["x"] + own["width"])) < 60
    assert abs(textarea["x"] - other["x"]) < 60


def test_chat_interface_grows_without_height(page):
    chat = ChatInterface(callback=lambda contents, user, instance: f"Echo: {contents}")
    serve_component(page, chat)

    textarea = page.locator("textarea").first
    expect(textarea).to_be_editable()
    textarea.fill("Hello")
    textarea.press("Enter")
    # The textarea keeps its text until the callback finishes, so match
    # the rendered messages only
    expect(page.locator("p", has_text=re.compile(r"^Hello$"))).to_be_visible()
    expect(page.locator("p", has_text=re.compile(r"^Echo: Hello$"))).to_be_visible()


def test_chat_message_meta_revealed_on_hover(page):
    message = ChatMessage("Hover me", user="Assistant")
    serve_component(page, message)

    copy = page.get_by_role("button", name="Copy")
    timestamp = page.locator(".MuiTypography-caption.chat-message-hover")
    expect(copy).to_have_css("opacity", "0")
    expect(timestamp).to_have_css("opacity", "0")
    page.get_by_text("Hover me").hover()
    expect(copy).to_have_css("opacity", "1")
    expect(timestamp).to_have_css("opacity", "1")
    expect(page.get_by_role("button", name="Copy")).to_be_visible()


def test_chat_message_reactions(page):
    message = ChatMessage(
        "Looks good!",
        reactions=["like"],
        reaction_icons={"like": "thumbup", "dislike": "thumb-down"},
    )
    serve_component(page, message)

    like = page.get_by_role("button", name="like", exact=True)
    dislike = page.get_by_role("button", name="dislike", exact=True)
    expect(like).to_have_attribute("aria-pressed", "true")
    expect(like).to_have_text("thumb_up")
    expect(like).to_have_css("opacity", "1")
    expect(dislike).to_have_css("opacity", "0")
    expect(dislike).to_have_text("thumb_down")

    page.get_by_text("Looks good!").hover()
    dislike.click()
    wait_until(lambda: message.reactions == ["like", "dislike"], page)
    expect(dislike).to_have_attribute("aria-pressed", "true")
    like.click()
    wait_until(lambda: message.reactions == ["dislike"], page)


def test_chat_message_copy_hidden_for_non_text(page):
    feed = ChatFeed()
    feed.add_step("Working", title="Step", user="Assistant")
    serve_component(page, feed)

    expect(page.get_by_text("Working")).to_be_visible()
    expect(page.get_by_role("button", name="Copy")).to_have_count(0)


def test_chat_message_hides_user_and_avatar_by_default(page):
    message = ChatMessage("Hi", user="Assistant")
    serve_component(page, message)

    expect(page.get_by_text("Hi")).to_be_visible()
    expect(page.get_by_text("Assistant")).to_have_count(0)
    expect(page.locator(".MuiAvatar-root")).to_have_count(0)


def test_chat_feed_shows_users_and_avatars_when_multiple_agents_reply(page):
    feed = ChatFeed()
    feed.send("Question", user="User", respond=False)
    feed.send("Answer", user="Agent A", respond=False)
    serve_component(page, feed)

    expect(page.get_by_text("Answer")).to_be_visible()
    expect(page.get_by_text("Agent A")).to_have_count(0)
    expect(page.locator(".MuiAvatar-root")).to_have_count(0)
    feed.send("Second opinion", user="Agent B", respond=False)
    expect(page.get_by_text("Agent A")).to_be_visible()
    expect(page.get_by_text("Agent B")).to_be_visible()
    # The right aligned User message stays without an avatar.
    expect(page.locator(".MuiAvatar-root")).to_have_count(2)
    expect(page.locator(".MuiTypography-caption").filter(has_text="User")).to_have_count(0)


def test_chat_feed_grouped_message_hides_user(page):
    feed = ChatFeed(message_params={"show_user": True})
    feed.send("First", user="Assistant", respond=False)
    feed.send("Second", user="Assistant", respond=False)
    serve_component(page, feed)

    expect(page.get_by_text("Second")).to_be_visible()
    expect(page.locator(".MuiTypography-caption").filter(has_text="Assistant")).to_have_count(1)


def test_chat_feed_help_message_hides_user(page):
    feed = ChatFeed(help_text="Ask me anything")
    serve_component(page, feed)

    expect(page.get_by_text("Ask me anything")).to_be_visible()
    expect(page.locator(".MuiTypography-caption").filter(has_text="Help")).to_have_count(0)


def test_chat_area_send_disabled_when_empty(page):
    widget = ChatAreaInput()
    serve_component(page, widget)

    send = page.get_by_role("button", name="Send message")
    expect(send).to_be_disabled()
    page.locator("textarea").first.fill("Hello")
    expect(send).to_be_enabled()
    page.locator("textarea").first.fill("   ")
    expect(send).to_be_disabled()


def test_chat_interface_actions_menu(page):
    chat = ChatInterface()
    chat.send("Hello", respond=False)
    serve_component(page, chat)

    page.get_by_role("button", name="Actions").click()
    page.get_by_role("menuitem", name="Clear").click()
    wait_until(lambda: len(chat.objects) == 0, page)
    expect(page.get_by_role("menu")).to_have_count(0)


@pytest.mark.parametrize("margin", [0, (0, 0, 0, 20), (5, 10)])
def test_chat_message_short_markdown_does_not_wrap(page, margin):
    text = "Let me check which tables are available in the database."
    feed = ChatFeed(width=900, height=300)
    feed.send(ChatMessage(Markdown(text, margin=margin), user="Assistant"), respond=False)
    serve_component(page, feed)

    paragraph = page.locator("p").filter(has_text=text)
    expect(paragraph).to_have_count(1)
    line_height = paragraph.evaluate("el => parseFloat(getComputedStyle(el).lineHeight)")
    assert paragraph.bounding_box()["height"] < 1.5 * line_height


def test_chat_message_viewer_renders_at_natural_height(page):
    feed = ChatFeed(width=600, height=800)
    feed.send(ChatMessage(_Summary(), user="Assistant"), respond=False)
    serve_component(page, feed)

    expect(page.get_by_text("Summary text")).to_be_visible()
    assert _bubble(page, "Summary text").bounding_box()["height"] < 200


class _Summary(Viewer):

    def __panel__(self):
        return Column(Markdown("Summary text"))
