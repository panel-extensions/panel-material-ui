from __future__ import annotations

import param
from panel._param import Margin
from panel.chat.step import ChatStep as _PnChatStep

from ..layout import Card


class ChatStep(Card, _PnChatStep):
    """
    A component that makes it easy to provide status updates and the
    ability to stream updates to both the output(s) and the title.

    Reference: https://panel.holoviz.org/reference/chat/ChatStep.html

    :Example:

    >>> ChatStep("Hello world!", title="Running calculation...', status="running")
    """

    margin = Margin(default=(5, 0, 0, 0))

    _esm_base = "ChatStep.jsx"
    _rename = {
        "objects": "objects", "title": "title", "status": "status"}

    def __init__(self, *objects, **params):
        self._instance = None
        self._failed_title = ""
        Card.__init__(self, *objects, **params)

    @param.depends("status", "default_badges", watch=True)
    def _render_avatar(self):
        return
