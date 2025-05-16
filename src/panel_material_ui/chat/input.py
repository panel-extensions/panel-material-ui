from __future__ import annotations

from typing import Callable

import param

from ..base import ThemedTransform
from ..widgets import TextAreaInput


class ChatAreaInput(TextAreaInput):
    """
    The `ChatAreaInput` allows entering any multiline string using a text input
    box, with the ability to press enter to submit the message.

    Unlike TextAreaInput, the `ChatAreaInput` defaults to auto_grow=True and
    max_rows=10, and the value is not synced to the server until the enter key
    is pressed so bind on `value_input` if you need to access the existing value.

    Lines are joined with the newline character `\\n`.

    :References:

    - https://panel-material-ui.holoviz.org/reference/chat/ChatAreaInput.html
    - https://panel.holoviz.org/reference/chat/ChatAreaInput.html

    :Example:

    >>> ChatAreaInput(max_rows=10)
    """

    actions = param.Dict(default={}, doc="""
        A dictionary of actions that can be invoked via the speed dial to the
        left of input area. The actions should be defined as a dictionary indexed
        by the name of the action mapping to values that themselves are dictionaries
        containing an icon. Users can define callbacks by registering callbacks using
        the on_action method.""")

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

    loading = param.Boolean(default=False)

    max_rows = param.Integer(default=10)

    max_length = param.Integer(default=50000, doc="""
        Max count of characters in the input field.""")

    rows = param.Integer(default=1)

    _esm_base = "ChatArea.jsx"

    _esm_transforms = [ThemedTransform]

    _rename = {"loading": "loading"}

    def __init__(self, **params):
        action_callbacks = {}
        if 'actions' in params:
            actions = {}
            for action, value in params['actions'].items():
                value = dict(value)
                if 'callback' in value:
                    action_callbacks[action] = value.pop('callback')
                actions[action] = value
            params['actions'] = actions
        super().__init__(**params)
        self._action_callbacks = {}
        for action, callback in action_callbacks.items():
            self.on_action(action, callback)

    def _handle_msg(self, msg) -> None:
        if msg['type'] == 'input':
            self.value = msg['value']
            self.param.trigger('enter_pressed')
            with param.discard_events(self):
                self.value = ""
        elif msg['type'] == 'action':
            for callback in self._action_callbacks.get(msg['action'], []):
                try:
                    callback(msg)
                except Exception:
                    pass

    def on_action(self, name: str, callback: Callable):
        """
        Allows registering a callback invoked when an action is defined.

        Parameters
        ----------
        name: str
            The name of the action to register the callback for.
        callback: callable
            The callback to invoke when the action is triggered.
        """
        if name not in self._action_callbacks:
            self._action_callbacks[name] = []
        self._action_callbacks[name].append(callback)

    def _update_loading(self, *_) -> None:
        """
        Loading handler handled client-side.
        """


__all__ = ["ChatAreaInput"]
