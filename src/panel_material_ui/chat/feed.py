from panel.chat.feed import ChatFeed as _PnChatFeed
from panel.layout import Column

from ..layout import Card
from .message import ChatMessage
from .step import ChatStep


class ChatFeed(_PnChatFeed):
    """
    A ChatFeed holds a list of `ChatMessage` objects and provides convenient APIs.
    to interact with them.

    This includes methods to:
    - Send (append) messages to the chat log.
    - Stream tokens to the latest `ChatMessage` in the chat log.
    - Execute callbacks when a user sends a message.
    - Undo a number of sent `ChatMessage` objects.
    - Clear the chat log of all `ChatMessage` objects.

    :References:

    - https://panel-material-ui.holoviz.org/reference/chat/ChatFeed.html
    - https://panel.holoviz.org/reference/chat/ChatFeed.html

    :Example:

    >>> async def say_welcome(contents, user, instance):
    >>>    yield "Welcome!"
    >>>    yield "Glad you're here!"

    >>> chat_feed = ChatFeed(callback=say_welcome, header="Welcome Feed")
    >>> chat_feed.send("Hello World!", user="New User", avatar="😊")
    """
    _card_type = Card
    _message_type = ChatMessage
    _step_type = ChatStep

    def _build_steps_layout(self, step, layout_params, default_layout):
        layout_params = layout_params or {}
        input_layout_params = dict(
            min_width=100
        )
        if default_layout == "column":
            layout = Column
        elif default_layout == "card":
            layout = self._card_type
            title = layout_params.pop("title", None)
            input_layout_params["title"] = title or "🪜 Steps"
            input_layout_params["sizing_mode"] = "stretch_width"
        else:
            raise ValueError(
                f"Invalid default_layout {default_layout!r}; "
                f"expected 'column' or 'card'."
            )
        if layout_params:
            input_layout_params.update(layout_params)
        return layout(step, **input_layout_params)

__all__ = ["ChatFeed"]
