import panel as pn
import param
from panel.viewable import Viewer

from panel_material_ui.chat import ChatMessage
from panel_material_ui.chat.step import ChatStep
from panel_material_ui.layout import Card, Column


class Summary(Viewer):

    text = param.String(default="Summary")

    def __panel__(self):
        return Column(pn.pane.Markdown(self.text))


def test_chat_message_viewer_has_no_fixed_height():
    message = ChatMessage(Summary())
    assert message._object_panel.height is None


def test_chat_message_viewer_contents_are_styled_as_message():
    message = ChatMessage(Summary())
    markdown = message._object_panel[0]
    assert "message" in markdown.css_classes


def test_chat_message_markdown_streamed_from_empty_gets_message_class():
    md = pn.pane.Markdown("")
    ChatMessage(md)
    assert "message" not in md.css_classes
    md.object = "Hello"
    assert "message" in md.css_classes


def test_chat_message_string_streamed_from_empty_gets_message_class():
    message = ChatMessage("")
    message.object = "Hello"
    assert "message" in message._object_panel.css_classes


def test_chat_message_styles_markup_in_plain_layouts():
    md = pn.pane.Markdown("Text", sizing_mode="stretch_width")
    ChatMessage(Column(pn.Row(md)))
    assert "message" in md.css_classes
    assert md.sizing_mode is None


def test_chat_message_does_not_restyle_markup_inside_components():
    inner = pn.pane.HTML("<b>tool</b>", sizing_mode="stretch_width")
    empty = pn.pane.HTML("", sizing_mode="stretch_width")
    ChatMessage(Column(Card(inner, empty)))
    for pane in (inner, empty):
        assert pane.sizing_mode == "stretch_width"
        assert pane.css_classes == []


def test_chat_message_does_not_restyle_chat_step_contents():
    inner = pn.pane.Markdown("Thinking", sizing_mode="stretch_width")
    ChatMessage(ChatStep(inner))
    assert inner.sizing_mode == "stretch_width"
    assert "message" not in inner.css_classes


def test_chat_message_keeps_explicit_css_classes():
    md = pn.pane.Markdown("Text", css_classes=["custom"])
    ChatMessage(md)
    assert md.css_classes == ["custom"]


def test_chat_message_applies_stylesheets_to_nested_components():
    inner = pn.pane.HTML("<b>tool</b>")
    message = ChatMessage(Column(Card(inner)))
    assert all(s in inner.stylesheets for s in message._stylesheets)


def test_chat_message_markup_without_object_is_not_styled():
    html = pn.pane.HTML(None)
    ChatMessage(html)
    assert "message" not in html.css_classes
