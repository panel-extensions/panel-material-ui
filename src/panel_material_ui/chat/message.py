from __future__ import annotations

import datetime
from contextlib import ExitStack
from io import BytesIO
from pathlib import PurePath
from zoneinfo import ZoneInfo

import param
from panel.chat.message import DEFAULT_AVATARS as DEFAULT_AVATARS_PANEL
from panel.chat.message import ChatMessage, ChatReactionIcons
from panel.io import state
from panel.layout import Panel, Row
from panel.pane import Placeholder
from panel.pane import panel as as_panel
from panel.pane.image import FileBase, Image, ImageBase
from panel.pane.markup import HTMLBasePane
from panel.util import isfile
from panel.viewable import Child
from panel.widgets import Widget

from ..base import MaterialComponent
from .input import ChatAreaInput

_MESSAGE_BG = ":host(.message), .message { background-color: unset !important; box-shadow: unset !important; }"

DEFAULT_AVATARS = {
    "system": {"type": "icon", "icon": "settings"},
    **DEFAULT_AVATARS_PANEL
}


class MessageState(param.Parameterized):

    avatar = param.Parameter(allow_refs=True)

    timestamp = param.String(allow_refs=True)


class ChatMessage(MaterialComponent, ChatMessage):
    """
    Renders another component as a chat message with an associated user
    and avatar with support for various content types.

    This widget provides a structured view of chat messages, including features like:

    - Displaying user avatars, which can be text, emoji, or images.
    - Showing the user's name.
    - Displaying the message timestamp in a customizable format.
    - Associating reactions with messages and mapping them to icons.
    - Rendering various content types including text, images, audio, video, and more.

    :References:

    - https://panel-material-ui.holoviz.org/reference/chat/ChatMessage.html
    - https://panel.holoviz.org/reference/chat/ChatMessage.html

    :Example:

    >>> ChatMessage(object="Hello world!", user="New User", avatar="😊")
    """

    avatar = param.ClassSelector(default="", class_=(str, BytesIO, bytes, ImageBase, dict), doc="""
        The avatar to use for the user. Can be a single character text, an emoji, or anything
        supported by `pn.pane.Image`. If not set, checks if the user is available in the
        default_avatars mapping; else uses the first character of the name.""")

    css_classes = param.List(default=[],doc="""
        The CSS classes to apply to the widget.""")

    default_avatars = param.Dict(default=DEFAULT_AVATARS, doc="""
        A default mapping of user names to their corresponding avatars
        to use when the user is specified but the avatar is. You can
        modify, but not replace the dictionary.""")

    default_layout = param.ClassSelector(class_=(Panel), precedence=-1)

    elevation = param.Integer(default=2, doc="The elevation of the message.")

    placement = param.Selector(default="left", objects=["left", "right"], doc="The placement of the message.")

    _internal_state = param.ClassSelector(class_=MessageState, default=MessageState())
    _object_panel = Child()

    _esm_base = "ChatMessage.jsx"
    _rename = {
        "avatar": None,
        "avatar_lookup": None,
        "default_avatars": None,
        "object": None
    }

    def __init__(self, object=None, **params):
        self._exit_stack = ExitStack()
        if 'placement' not in params and ChatMessage.placement is None:
            user = params.get('user', ChatMessage.user).lower()
            params['placement'] = 'right' if user == 'user' else 'left'
        if params.get("timestamp") is None:
            tz = params.get("timestamp_tz")
            if tz is not None:
                tz = ZoneInfo(tz)
            elif state.browser_info and state.browser_info.timezone:
                tz = ZoneInfo(state.browser_info.timezone)
            params["timestamp"] = datetime.datetime.now(tz=tz)
        reaction_icons = params.get("reaction_icons", {"favorite": "heart"})
        if isinstance(reaction_icons, dict):
            params["reaction_icons"] = ChatReactionIcons(options=reaction_icons, default_layout=Row, sizing_mode=None)
        self._internal = True
        if not self.avatar:
            self._update_avatar()
        self._internal_state = MessageState(
            avatar=self.param.avatar,
        )
        if not ChatMessage.width and params.get('width') is None and params.get('sizing_mode', None) is None:
            params['sizing_mode'] = 'stretch_width'
        MaterialComponent.__init__(self, object=object, **params)
        self._internal_state.timestamp = self.param.timestamp.rx().strftime(self.param.timestamp_format)
        self._build_layout()

    @param.depends('avatar', watch=True, on_init=True)
    def _render_avatar_html(self):
        avatar = self.avatar
        if isinstance(avatar, dict):
            self._internal_state.avatar = avatar
        elif isinstance(avatar, ImageBase) or (isinstance(avatar, str) and Image.applies(avatar)):
            avatar = as_panel(avatar)
            if self.embed or (isfile(avatar.object) or not isinstance(avatar.object, (str, PurePath))):
                data = avatar._data(avatar.object)
                src = avatar._b64(data)
            elif isinstance(avatar.object, PurePath):
                raise ValueError(f"Could not find Avatar {type(avatar).__name__}.object {avatar.object}.")
            else:
                src = self.avatar.object
            self._internal_state.avatar = {"type": "image", "src": src}
        else:
            self._internal_state.avatar = {"type": "text", "text": self.avatar}

    @property
    def _synced_params(self) -> list[str]:
        """
        Parameters which are synced with properties using transforms
        applied in the _process_param_change method.
        """
        ignored = ['default_layout', 'loading', 'background']
        return [p for p in self.param if p not in self._manual_params+ignored]

    def _handle_msg(self, msg):
        if msg == 'edit':
            self._toggle_edit(msg)
        elif msg == 'copy':
            object_panel = self._object_panel
            if isinstance(object_panel, HTMLBasePane):
                object_panel = object_panel.object
            elif isinstance(object_panel, Widget):
                object_panel = object_panel.value
            self._send_msg({"type": "copy", "text": object_panel if isinstance(object_panel, str) else ""})

    def _build_layout(self):
        self._object_panel = self._create_panel(self.object)
        self._placeholder = Placeholder(
            object=self._object_panel,
            css_classes=["placeholder"],
            stylesheets=self._stylesheets + self.param.stylesheets.rx(),
            sizing_mode='stretch_width',
        )
        self._edit_area = ChatAreaInput(
            css_classes=["edit-area"],
            stylesheets=self._stylesheets + self.param.stylesheets.rx()
        )
        self.param.watch(self._update_object_pane, "object")
        self.param.watch(self._update_reaction_icons, "reaction_icons")
        self.edit_icon.param.watch(self._toggle_edit, "value")
        self._edit_area.param.watch(self._submit_edit, "enter_pressed")
        self._composite = Row()

    def _include_styles(self, obj):
        obj = as_panel(obj)
        combined = self._stylesheets + self.stylesheets + [_MESSAGE_BG]
        for o in obj.select():
            params = {
                "stylesheets": [
                    stylesheet for stylesheet in combined
                    if stylesheet not in o.stylesheets
                ] + o.stylesheets
            }
            is_markup = isinstance(o, HTMLBasePane) and not isinstance(o, FileBase)
            if is_markup:
                params["sizing_mode"] = None
                if not o.css_classes and len(str(o.object)) > 0:  # only show a background if there is content
                    params["css_classes"] = [
                        *(css for css in o.css_classes if css != "message"), "message"
                    ]
            o.param.update(**params)

    def _process_param_change(self, params):
        params = super()._process_param_change(params)
        if 'stylesheets' in params:
            params['stylesheets'] += [".message { font-size: 1.25em; overflow-wrap: anywhere; word-break: break-word; width; max-width: calc(100% - 20px); }"]
        return params

__all__ = ["ChatMessage"]
