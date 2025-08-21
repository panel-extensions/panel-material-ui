from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import param
from panel.chat.interface import CallbackState
from panel.chat.interface import ChatInterface as PnChatInterface
from panel.layout import Column, Row
from panel.pane.markup import Markdown

from .feed import ChatFeed
from .input import ChatAreaInput

if TYPE_CHECKING:
    pass

ICON_MAP = {
    "arrow-back": "undo",
    "trash": "delete",
}


class ChatInterface(ChatFeed, PnChatInterface):
    """
    A chat interface that uses Material UI components.

    :References:

    - https://panel-material-ui.holoviz.org/reference/chat/ChatInterface.html
    - https://panel.holoviz.org/reference/chat/ChatInterface.html

    :Example:

    >>> ChatInterface().servable()
    """

    input_params = param.Dict(
        default={}, doc="Additional parameters to pass to the ChatAreaInput widget, like `enable_upload`."
    )

    on_submit = param.Callable(default=None, doc="""
        Callback to invoke when the send button or enter is pressed; should accept an event and instance as args.
        If unspecified, the default behavior is to send a Column containing the input text and views.
        This only affects the user-facing input, and does not affect the `send` method.""")

    widgets = param.Parameter(constant=True, doc="Not supported by panel-material-ui ChatInterface.")

    _input_type = ChatAreaInput

    _rename = {"loading": "loading"}

    def __init__(self, **params):
        self._widget = None
        self._send_watcher = None
        super().__init__(**params)

    @param.depends("_callback_state", watch=True)
    async def _update_input_disabled(self):
        busy_states = (CallbackState.RUNNING, CallbackState.GENERATING)
        if not self.show_stop or self._callback_state not in busy_states or self._callback_future is None:
            self._widget.loading = False
        else:
            self._widget.loading = True

    @param.depends("button_properties", watch=True)
    def _init_widgets(self):
        if self._widget is None:
            self._widget = ChatAreaInput(sizing_mode="stretch_width", disabled=self.param.disabled, **self.input_params)
            self._widget.on_action("stop", self._click_stop)
            input_container = Row(self._widget, sizing_mode="stretch_width")
            self._input_container.objects = [input_container]
            self._input_layout = input_container
            self._init_button_data()
        else:
            self._widget.param.unwatch(self._send_watcher)
        actions = {}
        for name, data in self._button_data.items():
            if (
                name in ("send", "stop") or (name == "rerun" and not self.show_rerun) or
                (name == "undo" and not self.show_undo) or (name == "clear" and not self.show_clear)
            ):
                continue
            actions[name] = {'icon': ICON_MAP.get(data.icon, data.icon), 'callback': partial(data.callback, self), 'label': name.title()}
        self._widget.actions = actions
        callback = partial(self._button_data["send"].callback, instance=self)
        self._send_watcher = self._widget.param.watch(callback, "value")

    def _click_send(
        self,
        event: param.parameterized.Event | None = None,
        instance: ChatInterface | None = None
    ) -> None:
        if self.disabled:
            return

        if self.on_submit is not None:
            self.on_submit(event, instance)
            return

        objects = self._widget.views
        if event.new:
            objects.append(Markdown(event.new))
        if not objects:
            return
        value = Column(*objects) if len(objects) > 1 else objects[0]
        self.send(value=value, user=self.user, avatar=self.avatar, respond=True)

    @param.depends("placeholder_text", "placeholder_params", watch=True, on_init=True)
    def _update_placeholder(self):
        self._placeholder = self._message_type(
            self.placeholder_text,
            avatar='PLACEHOLDER',
            css_classes=["message"],
            **self.placeholder_params
        )

__all__ = ["ChatInterface"]
