import panel as pn
from panel.chat import ChatReactionIcons

from panel_material_ui import ChatFeed, ChatInterface, ChatMessage, ChatStep, Column


def test_chat_message_placement_defaults_to_user():
    assert ChatMessage("Hi", user="User").placement == "right"
    assert ChatMessage("Hi", user="Assistant").placement == "left"


def test_chat_message_explicit_placement():
    assert ChatMessage("Hi", user="User", placement="left").placement == "left"


def test_chat_interface_places_own_user_right():
    chat = ChatInterface(user="Philipp")
    own = chat.send("Hi", user="Philipp", respond=False)
    other = chat.send("Hello", user="Assistant", respond=False)
    assert own.placement == "right"
    assert other.placement == "left"


def test_chat_interface_respects_message_params_placement():
    chat = ChatInterface(user="Philipp", message_params={"placement": "left"})
    assert chat.send("Hi", user="Philipp", respond=False).placement == "left"


def test_chat_feed_groups_consecutive_messages():
    feed = ChatFeed()
    first = feed.send("One", user="Assistant", respond=False)
    second = feed.send("Two", user="Assistant", respond=False)
    third = feed.send("Three", user="User", respond=False)
    fourth = feed.send("Four", user="Assistant", respond=False)
    assert [m._internal_state.grouped for m in (first, second, third, fourth)] == [False, True, False, False]


def test_chat_feed_auto_show_user():
    feed = ChatFeed()
    question = feed.send("Question", user="User", respond=False)
    answer = feed.send("Answer", user="Agent A", respond=False)
    assert ChatMessage("Hi").show_user == "auto"
    assert not answer._internal_state.show_user
    other = feed.send("Second opinion", user="Agent B", respond=False)
    assert answer._internal_state.show_user
    assert other._internal_state.show_user
    assert not question._internal_state.show_user


def test_chat_feed_regroups_on_removal():
    feed = ChatFeed()
    feed.send("One", user="Assistant", respond=False)
    second = feed.send("Two", user="Assistant", respond=False)
    feed.objects = feed.objects[1:]
    assert not second._internal_state.grouped


def test_chat_feed_help_message():
    feed = ChatFeed(help_text="Ask me anything")
    help_message = feed.objects[0]
    assert help_message._internal_state.help
    assert not help_message.show_user
    assert not help_message.show_timestamp
    message = feed.send("Hi", user="Help", respond=False)
    assert not message._internal_state.grouped


def test_chat_feed_help_message_respects_message_params():
    feed = ChatFeed(help_text="Ask me anything", message_params={"show_timestamp": True})
    assert feed.objects[0].show_timestamp


def test_chat_message_has_text():
    message = ChatMessage("Hi")
    assert message._internal_state.has_text
    message.object = Column(pn.pane.Markdown("Hi"))
    assert not message._internal_state.has_text
    message.object = pn.pane.Markdown("Hello")
    assert message._internal_state.has_text


def test_chat_message_reaction_options():
    message = ChatMessage("Hi", reaction_icons={"like": "thumbup", "favorite": "heart", "dislike": "thumb-down"})
    assert message._internal_state.reaction_options == {
        "like": {"icon": "thumb_up", "active_icon": "thumb_up"},
        "favorite": {"icon": "favorite", "active_icon": "favorite"},
        "dislike": {"icon": "thumb_down", "active_icon": "thumb_down"},
    }
    message.reaction_icons = ChatReactionIcons(options={"star": "star"})
    assert list(message._internal_state.reaction_options) == ["star"]


def test_chat_message_reaction_toggle():
    message = ChatMessage("Hi", reaction_icons={"like": "thumb-up"})
    message._handle_msg({"type": "reaction", "reaction": "like"})
    assert message.reactions == ["like"]
    message._handle_msg({"type": "reaction", "reaction": "like"})
    assert message.reactions == []


def test_chat_message_empty_text_not_copyable():
    assert not ChatMessage("")._internal_state.has_text


def test_chat_feed_steps_layout():
    feed = ChatFeed()
    feed.add_step("Running", title="Step", user="Assistant")
    steps = feed.objects[-1].object
    assert steps.title == "Steps"
    assert steps.elevation == 0
    assert isinstance(steps.objects[0], ChatStep)
