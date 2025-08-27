from __future__ import annotations

from typing import Callable

import param
from panel.viewable import Children

from ..base import ThemedTransform
from ..widgets.input import TextAreaInput, _FileUploadArea


class ChatAreaInput(TextAreaInput, _FileUploadArea):
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

    accept = param.String(default=None, doc="""
        A comma separated string of file extensions (with dots) or MIME types
        that should be accepted for upload. Examples: '.csv,.json,.txt' or
        'text/csv,application/json'.""")

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

    enable_upload = param.Boolean(
        default=True,
        doc="If True, enables uploading of files."
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

    placeholder = param.String(default="Ask anything...")

    rows = param.Integer(default=1)

    value_uploaded = param.Dict(default={}, doc="""
        Dictionary containing raw file data keyed by filename after user sends uploads.
        Each entry contains mime_type, value (bytes), and size.""")

    views = param.List(default=[], doc="""
        Views generated from uploaded files.""")

    footer_objects = Children(default=[], doc="""
        A list of panel objects to display in the footer area below the input.""")

    _esm_base = "ChatArea.jsx"

    _esm_transforms = [ThemedTransform]

    _rename = {"loading": "loading", "views": None, "value_uploaded": None, "footer_objects": "footer_objects"}

    def __init__(self, **params):
        super().__init__(**params)
        self._action_callbacks = {}
        self._update_actions()
        self.param.watch(self._update_actions, 'actions')

    def _update_actions(self, event=None):
        if event and event.old:
            for action, spec in event.old.items():
                if 'callback' in spec:
                    self.remove_on_action(action, spec['callback'])
        for action, spec in self.actions.items():
            if 'callback' in spec:
                self.on_action(action, spec['callback'])

    def _process_param_change(self, params):
        props = super()._process_param_change(params)
        if 'actions' in props:
            actions = {}
            for action, spec in props['actions'].items():
                if 'callback' in spec:
                    spec = dict(spec)
                    del spec['callback']
                actions[action] = spec
            props['actions'] = actions
        return props

    @param.depends("accept", watch=True, on_init=True)
    def _validate_accept(self):
        if self.accept is None:
            return

        extensions = [ext.strip() for ext in self.accept.split(',')]
        for ext in extensions:
            if not ext:  # Skip empty strings
                continue

            if '/' in ext:
                # This should be a MIME type (e.g., 'text/csv', 'image/png')
                parts = ext.split('/')
                if len(parts) != 2 or not parts[0] or not parts[1]:
                    raise ValueError(
                        f"Invalid MIME type '{ext}'. MIME types should be in format 'type/subtype' "
                        f"(e.g., 'text/csv', 'application/json')."
                    )
                # Check for invalid subtypes like '.csv' in 'text/.csv'
                if parts[1].startswith('.'):
                    raise ValueError(
                        f"Invalid MIME type '{ext}'. The subtype '{parts[1]}' should not start with a dot. "
                        f"Use '{parts[0]}/{parts[1][1:]}' or file extension '{parts[1]}' instead."
                    )
            elif not ext.startswith('.') and len(ext) <= 10:
                # This looks like a file extension without a dot
                raise ValueError(
                    f"File extension '{ext}' should start with a dot (e.g., '.{ext}'). "
                    f"Use file extensions like '.csv,.json' or MIME types like 'text/csv,application/json'."
                )

    def _handle_msg(self, msg) -> None:
        if msg['type'] == 'input':
            try:
                if msg["value"] == "" and msg["value"] == self.value and self.value_uploaded:
                    self.param.trigger("value")
                else:
                    self.value = msg['value']
                self.param.trigger('enter_pressed')
                self._send_msg({"status": "finished"})
            except Exception as e:
                self._send_msg({"status": "error", "error": str(e)})
            with param.discard_events(self):
                self.value = ""
                self.views = []
        elif msg['type'] == 'action':
            for callback in self._action_callbacks.get(msg['action'], []):
                try:
                    callback(msg)
                except Exception:
                    pass
        else:
            _FileUploadArea._handle_msg(self, msg)

    def _update_file(
        self,
        filename: str | list[str],
        mime_type: str | list[str],
        value: bytes | list[bytes],
    ):
        if not isinstance(filename, list):
            filename = [filename]
            mime_type = [mime_type]
            value = [value]

        # Store raw file data
        self.value_uploaded = {
            fname: {
                "mime_type": mtype,
                "value": fdata,
                "size": len(fdata) if fdata else 0
            }
            for fname, mtype, fdata in zip(filename, mime_type, value, strict=False)
        }

        # Create views
        self.views = [
            self._single_view(self._single_object(fdata, fname, mtype), fname, mtype)
            for fname, mtype, fdata in zip(filename, mime_type, value, strict=False)
        ]

    def on_action(self, name: str, callback: Callable):
        """
        Registers a callback that is invoked when an action triggered.

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

    def remove_on_action(self, name: str, callback: Callable):
        """
        Removes a callback that was registered with on_action.

        Parameters
        ----------
        name: str
            The name of the action to register the callback for.
        callback: callable
            The callback to invoke when the action is triggered.
        """
        if name in self._action_callbacks:
            self._action_callbacks[name].remove(callback)

    def _update_loading(self, *_) -> None:
        """
        Loading handler handled client-side.
        """


__all__ = ["ChatAreaInput"]
