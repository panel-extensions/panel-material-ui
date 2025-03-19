from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import param
from panel.chat.interface import CallbackState, ChatInterface
from panel.layout import Row

from ..layout import Card
from .input import ChatAreaInput
from .message import ChatMessage
from .step import ChatStep

if TYPE_CHECKING:
    pass

ICON_MAP = {
    "arrow-back": "undo",
    "trash": "delete",
}


class ChatInterface(ChatInterface):
    """
    A chat interface that uses Material UI components.

    Reference: https://panel.holoviz.org/reference/chat/ChatInterface.html

    :Example:

    >>> ChatInterface().servable()
    """

    _card_type = Card
    _input_type = ChatAreaInput
    _message_type = ChatMessage
    _step_type = ChatStep

    _rename = {"loading": "loading"}

    @param.depends("_callback_state", watch=True)
    async def _update_input_disabled(self):
        busy_states = (CallbackState.RUNNING, CallbackState.GENERATING)
        if not self.show_stop or self._callback_state not in busy_states or self._callback_future is None:
            self._widget.loading = False
        else:
            self._widget.loading = True

    @param.depends("widgets", "button_properties", watch=True)
    def _init_widgets(self):
        if len(self.widgets) > 1:
            raise ValueError("Only one widget is supported")
        self._init_button_data()
        self._widget = ChatAreaInput(
            sizing_mode="stretch_width",
            actions={
                name: {'icon': ICON_MAP.get(data.icon, data.icon), 'callback': partial(data.callback, self), 'label': name.title()}
                for name, data in self._button_data.items() if name not in ("send", "stop")
            }
        )
        self.link(self._widget, disabled="disabled_enter")
        callback = partial(self._button_data["send"].callback, self)
        self._widget.param.watch(callback, "value")
        self._widget.on_action("stop", self._click_stop)
        input_container = Row(self._widget, sizing_mode="stretch_width")
        self._input_container.objects = [input_container]
        self._input_layout = input_container

    @param.depends("placeholder_text", "placeholder_params", watch=True, on_init=True)
    def _update_placeholder(self):
        self._placeholder = self._message_type(
            self.placeholder_text,
            avatar='PLACEHOLDER',
            css_classes=["message"],
            **self.placeholder_params
        )
