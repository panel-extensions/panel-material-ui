from __future__ import annotations

import param
from panel._param import Margin
from panel.chat.step import ChatStep as _PnChatStep
from panel.chat.utils import stream_to
from panel.layout import Row
from panel.pane.image import ImageBase
from panel.pane.markup import HTMLBasePane, Markdown
from panel.util import edit_readonly

from ..layout import Card


class ChatStep(Card, _PnChatStep):
    """
    A component that makes it easy to provide status updates and the
    ability to stream updates to both the output(s) and the title.

    :References:

    - https://panel-material-ui.holoviz.org/reference/chat/ChatStep.html
    - https://panel.holoviz.org/reference/chat/ChatStep.html

    :Example:

    >>> ChatStep("Hello world!", title="Running calculation...', status="running")
    """

    margin = Margin(default=(5, 0, 0, 0))

    sizing_mode = param.Selector(default="stretch_width")

    _esm_base = "ChatStep.jsx"
    _rename = {
        "objects": "objects", "title": "title", "status": "status"
    }
    _stylesheets = []

    def __init__(self, *objects, **params):
        self._instance = None
        self._failed_title = ""
        Card.__init__(self, *objects, **params)
        self._title_pane.styles = {'font-size': '1.25em', 'text-align': 'left', 'overflow-wrap': 'break-word'}
        with edit_readonly(self):
            self.header = Row(
                self._title_pane,
                stylesheets=self._stylesheets + self.param.stylesheets.rx(),
                css_classes=["step-header"],
                margin=(5, 0),
                width=self.width,
                max_width=self.max_width,
                min_width=self.min_width,
                sizing_mode=self.sizing_mode,
            )

    @param.depends("status", "default_badges", watch=True)
    def _render_avatar(self):
        return

    def stream(self, token: str | None, replace: bool = False):
        """
        Stream a token to the last available string-like object.

        Parameters
        ----------
        token : str
            The token to stream.
        replace : bool
            Whether to replace the existing text.

        Returns
        -------
        Viewable
            The updated message pane.
        """
        if token is None:
            token = ""

        if (
            len(self.objects) == 0 or not isinstance(self.objects[-1], HTMLBasePane) or isinstance(self.objects[-1], ImageBase)
        ):
            message = Markdown(token, styles={'font-size': '1.25em', 'padding-block': '0px', 'padding-inline': '7px', 'overflow-wrap': 'break-word'})
            self.append(message)
        else:
            stream_to(self.objects[-1], token, replace=replace)

        if self._instance is not None:
            self._instance._chat_log.scroll_to_latest(self._instance.auto_scroll_limit)


__all__ = ["ChatStep"]
