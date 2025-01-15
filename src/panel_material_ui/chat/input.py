import param

from ..widgets import TextAreaInput


class ChatAreaInput(TextAreaInput):
    """
    The `ChatAreaInput` allows entering any multiline string using a text input
    box, with the ability to press enter to submit the message.

    Unlike TextAreaInput, the `ChatAreaInput` defaults to auto_grow=True and
    max_rows=10, and the value is not synced to the server until the enter key
    is pressed so bind on `value_input` if you need to access the existing value.

    Lines are joined with the newline character `\\n`.

    Reference: https://panel.holoviz.org/reference/chat/ChatAreaInput.html

    :Example:

    >>> ChatAreaInput(max_rows=10)
    """

    auto_grow = param.Boolean(default=True)

    disabled_enter = param.Boolean(
        default=False,
        doc="If True, disables sending the message by pressing the `enter_sends` key.",
    )

    enter_sends = param.Boolean(
        default=True,
        doc="If True, pressing the Enter key sends the message, if False it is sent by pressing the Ctrl+Enter.",
    )

    enter_pressed = param.Event(
        default=False,
        doc="If True, pressing the Enter key sends the message, if False it is sent by pressing the Ctrl+Enter.",
    )

    max_rows = param.Integer(default=10)

    max_length = param.Integer(default=50000, doc="""
        Max count of characters in the input field.""")

    rows = param.Integer(default=1)

    _esm_base = "ChatArea.jsx"

    def _handle_msg(self, msg) -> None:
        """
        Clear value on shift enter key down.
        """
        self.value = msg
        self.param.trigger('enter_pressed')
        with param.discard_events(self):
            self.value = ""
        self.value_input = ""
