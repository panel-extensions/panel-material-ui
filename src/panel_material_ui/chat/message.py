from __future__ import annotations

import datetime
import typing as t
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

_SLOT_STYLESHEET = """
:host { color: var(--mui-palette-text-secondary); font-size: 0.875rem; }
:host > div > :first-child { margin-top: 0; }
:host > div > :last-child { margin-bottom: 0; }
"""

# Undoes the bubble styling Panel's chat_message.css applies to markup panes,
# since the Paper in ChatMessage.jsx draws the bubble.
_MESSAGE_STYLESHEET = """
:host(.message), .message, :host(.step-message) {
  background-color: unset !important;
  box-shadow: unset !important;
  color: inherit;
  font-size: inherit;
  min-height: unset;
  padding: 0;
}
/* Panel's chat_message.css pads markdown children from the parent's scope. */
.markdown { padding-inline: 0; }
:host(.message) > div > :first-child, :host(.step-message) > div > :first-child { margin-top: 0; }
:host(.message) > div > :last-child, :host(.step-message) > div > :last-child { margin-bottom: 0; }
.MuiPaper-root:has(.edit-area) { width: 100% !important; }
.edit-area { height: unset; }
:host(.message) table {
  border: 1px solid var(--mui-palette-divider);
  border-collapse: separate;
  border-radius: var(--mui-shape-borderRadius, 4px);
  border-spacing: 0;
  overflow: hidden;
}
:host(.message) th, :host(.message) td {
  border: 0;
  border-bottom: 1px solid var(--mui-palette-divider);
  padding: 6px 12px;
}
:host(.message) thead th {
  background-color: var(--mui-palette-action-hover);
  font-weight: 500;
}
:host(.message) tbody tr:last-child td { border-bottom: 0; }
:host(.message) a { color: var(--pmui-chat-link-color, var(--mui-palette-primary-main)); }
:host(.message) :not(pre) > code {
  background-color: var(--pmui-chat-code-bg, var(--mui-palette-action-hover));
  border-radius: 4px;
  color: inherit;
  font-size: 0.875em;
  padding: 0.1em 0.35em;
}
:host(.message) .codehilite { margin: 0.5em 0; position: relative; }
/* Panel's copy button takes up a line of its own when the pre is the
   .codehilite element, so float it over the code instead. */
:host(.message) pre.codehilite > .copybtn { position: absolute; top: 0.5em; right: 0.5em; left: auto; }
"""

DEFAULT_AVATARS = {
    "system": {"type": "icon", "icon": "settings"},
    **DEFAULT_AVATARS_PANEL
}


# Reaction icons are Material Icons names; tabler names, which Panel's reaction
# icons use, are translated since most only differ by using dashes.
_TABLER_ICONS = {"heart": "favorite", "thumbup": "thumb_up", "thumbdown": "thumb_down"}


def _material_icon(name: str) -> str:
    name = name.strip().lower().replace("-", "_").replace(" ", "_").removesuffix("_filled")
    return _TABLER_ICONS.get(name, name)


class MessageState(param.Parameterized):

    avatar = param.Parameter(allow_refs=True)

    grouped = param.Boolean(default=False, doc="""
        Whether the message continues a run of messages from the same user.""")

    has_text = param.Boolean(default=False, doc="""
        Whether the rendered object is text that can be copied or edited.""")

    help = param.Boolean(default=False, doc="""
        Whether the message is the help text of a feed.""")

    reaction_options = param.Dict(default={}, doc="""
        Material icon names for each reaction, in its inactive and active state.""")

    multi_user = param.Boolean(default=False, doc="""
        Whether a feed resolved 'auto' for show_user and show_avatar to
        show the user's identity.""")

    timestamp = param.String(allow_refs=True)


class ChatMessage(MaterialComponent, ChatMessage):  # type: ignore[no-redef]
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

    default_layout = param.ClassSelector(class_=(Panel), precedence=-1)  # type: ignore[assignment]

    elevation = param.Integer(default=0, doc="""
        The elevation of the message. At 0 right aligned messages render in
        a primary colored bubble and left aligned messages without a container; a
        positive elevation renders every message on a raised card.""")

    placement: t.Literal['left', 'right'] | None = param.Selector(
        default=None, objects=["left", "right"], allow_None=True, doc="""
        The placement of the message. If None, messages from the user named
        'User' are placed on the right and all others on the left.""")  # type: ignore[assignment]

    show_avatar: t.Literal["auto"] | bool = param.Selector(default="auto", objects=["auto", True, False], doc="""
        Whether to display the avatar of the user. With 'auto' the avatar is
        only shown in a feed where messages from more than one other user,
        e.g. multiple agents, are placed on the left.""")  # type: ignore[assignment]

    show_user: t.Literal["auto"] | bool = param.Selector(default="auto", objects=["auto", True, False], doc="""
        Whether to display the name of the user. With 'auto' the name is only
        shown in a feed where messages from more than one other user, e.g.
        multiple agents, are placed on the left.""")  # type: ignore[assignment]

    _internal_state = param.ClassSelector(class_=MessageState, default=MessageState())
    _object_panel = Child()

    _esm_base = "ChatMessage.jsx"
    _rename = {
        "avatar": None,
        "avatar_lookup": None,
        "default_avatars": None,
        "object": None,
        "reaction_icons": None,
    }

    def __init__(self, object=None, **params):
        self._exit_stack = ExitStack()
        if params.get('placement') is None and type(self).placement is None:
            user = str(params.get('user', type(self).user)).lower()
            params['placement'] = 'right' if user == 'user' else 'left'
        if params.get("timestamp") is None:
            tz = params.get("timestamp_tz")
            if tz is not None:
                tz = ZoneInfo(tz)
            elif state.browser_info and state.browser_info.timezone:
                tz = ZoneInfo(state.browser_info.timezone)
            params["timestamp"] = datetime.datetime.now(tz=tz)
        reaction_icons = params.get("reaction_icons", {"favorite": "favorite"})
        if isinstance(reaction_icons, dict):
            params["reaction_icons"] = ChatReactionIcons(options=reaction_icons, default_layout=Row, sizing_mode=None)
        self._internal = True
        if not ChatMessage.width and params.get('width') is None and params.get('sizing_mode', None) is None:
            params['sizing_mode'] = 'stretch_width'
        MaterialComponent.__init__(self, object=object, **params)
        if not self.avatar:
            self._update_avatar()
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
            # Toggle between edit area and object panel since the
            # React frontend renders _object_panel directly (not _placeholder)
            if self._object_panel is self._edit_area:
                self._object_panel = self._original_object_panel
            else:
                self._original_object_panel = self._object_panel
                if isinstance(self._object_panel, HTMLBasePane):
                    self._edit_area.value = self._object_panel.object
                elif isinstance(self._object_panel, Widget):
                    self._edit_area.value = self._object_panel.value
                self._object_panel = self._edit_area
        elif isinstance(msg, dict) and msg.get('type') == 'reaction':
            reaction = msg['reaction']
            if reaction in self.reactions:
                self.reactions = [r for r in self.reactions if r != reaction]
            else:
                self.reactions = [*self.reactions, reaction]
        elif msg == 'copy':
            object_panel = self._object_panel
            if isinstance(object_panel, HTMLBasePane):
                object_panel = object_panel.object
            elif isinstance(object_panel, Widget):
                object_panel = object_panel.value
            self._send_msg({"type": "copy", "text": object_panel if isinstance(object_panel, str) else ""})

    def _submit_edit(self, event):
        # Restore the original panel and update the object with edited content
        if hasattr(self, '_original_object_panel'):
            self._object_panel = self._original_object_panel
        if isinstance(self.object, HTMLBasePane):
            self.object.object = self._edit_area.value
        elif isinstance(self.object, Widget):
            self.object.value = self._edit_area.value
        else:
            self.object = self._edit_area.value
        self.param.trigger("object")
        self.edited = True

    def _build_layout(self):
        self._object_panel = self._create_panel(self.object)
        self._original_object_panel = self._object_panel
        self._placeholder = Placeholder(
            object=self._object_panel,
            css_classes=["placeholder"],
            stylesheets=self._stylesheets + self.param.stylesheets.rx(),
            sizing_mode='stretch_width',
        )
        self._edit_area = ChatAreaInput(
            css_classes=["edit-area"],
            stylesheets=self._stylesheets + self.param.stylesheets.rx(),
            sizing_mode='stretch_width',
            placeholder="Edit message...",
        )
        self.param.watch(self._update_object_pane, "object")
        self.param.watch(self._update_reaction_icons, "reaction_icons")
        self._edit_area.param.watch(self._submit_edit, "enter_pressed")
        self._composite = Row()
        self._update_chat_copy_icon()
        self._update_reaction_icons()

    def _update_reaction_icons(self, event=None):
        icons = self.reaction_icons
        if isinstance(icons, dict):
            options, active_icons = icons, {}
        else:
            options, active_icons = icons.options, icons.active_icons
        self._internal_state.reaction_options = {
            reaction: {"icon": _material_icon(icon), "active_icon": _material_icon(active_icons.get(reaction, icon))}
            for reaction, icon in options.items()
        }

    def _update_chat_copy_icon(self):
        # Replaces Panel's ChatCopyIcon handling, the frontend renders the
        # copy and edit actions itself.
        object_panel = self._object_panel
        if isinstance(object_panel, HTMLBasePane):
            object_panel = object_panel.object
        elif isinstance(object_panel, Widget):
            object_panel = object_panel.value
        self._internal_state.has_text = isinstance(object_panel, str) and bool(object_panel)

    @param.depends('header_objects', 'footer_objects', watch=True, on_init=True)
    def _trim_slot_margins(self):
        # Header and footer text is secondary to the message, and paragraph
        # margins would push it away from the bubble and off-center from the
        # action buttons.
        for obj in (*self.header_objects, *self.footer_objects):
            for o in obj.select(HTMLBasePane):
                if _SLOT_STYLESHEET not in o.stylesheets:
                    o.stylesheets = [*o.stylesheets, _SLOT_STYLESHEET]

    def _include_styles(self, obj):
        obj = as_panel(obj)
        combined = self._stylesheets + self.stylesheets + [_MESSAGE_STYLESHEET]
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
        if 'stylesheets' in params and _MESSAGE_STYLESHEET not in params['stylesheets']:
            params['stylesheets'] += [_MESSAGE_STYLESHEET]
        return params

__all__ = ["ChatMessage"]
