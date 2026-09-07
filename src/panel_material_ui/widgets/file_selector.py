"""
Defines a Material UI FileSelector widget which allows browsing the
filesystem on the server and selecting one or more files.

The filesystem access is delegated to Panel's file provider abstraction,
so the widget can browse the local filesystem or any ``fsspec``
filesystem, while the browser UI is implemented in ``FileSelector.jsx``.
"""
from __future__ import annotations

import os
import pathlib
import typing as t

import param
from panel.widgets.file_selector import (
    BaseFileProvider,
    BaseFileSelector,
    LocalFileProvider,
)

from ..base import COLORS, ColorType
from .base import MaterialWidget

if t.TYPE_CHECKING:
    from fsspec import AbstractFileSystem


class FileSelector(MaterialWidget, BaseFileSelector):
    """
    The `FileSelector` widget allows browsing the filesystem on the
    server and selecting one or more files in a directory.

    The widget renders a Material UI file browser consisting of a
    navigation toolbar (back, forward, up and reload), a breadcrumb trail
    and an editable path field, a list of the entries in the current
    directory and a collapsible summary of the current selection.

    By default the directory the widget is initialized with also becomes
    the `root_directory`, i.e. the boundary the user cannot navigate
    above. Since the browser is a filesystem read primitive, always set
    `root_directory` explicitly when serving a `FileSelector` to
    untrusted users.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/FileSelector.html
    - https://panel.holoviz.org/reference/widgets/FileSelector.html
    - https://mui.com/material-ui/react-list/

    :Example:

    >>> FileSelector(directory='~', file_pattern='*.png')
    """

    color: ColorType = param.Selector(
        objects=COLORS, default="primary", doc="The color of the checkboxes and links."
    )  # type: ignore[assignment]

    directory = param.String(default=os.getcwd(), doc="""
        The directory to explore.""")

    file_pattern = param.String(default='*', doc="""
        A glob-like pattern to filter the files.""")

    only_files = param.Boolean(default=False, doc="""
        Whether to only allow selecting files.""")

    refresh_period = param.Integer(default=None, doc="""
        If set to non-None value indicates how frequently to refresh
        the directory contents in milliseconds.""")

    root_directory = param.String(default=None, doc="""
        The root directory beyond which users cannot navigate. If not
        set it is pinned to the directory the widget was initialized
        with.""")

    show_hidden = param.Boolean(default=False, doc="""
        Whether to show hidden files and directories (starting with
        a period).""")

    size = param.Integer(default=10, doc="""
        The approximate number of entries shown at once, which bounds
        the height of the entry list.""")

    value = param.List(default=[], item_type=(str, pathlib.Path), doc="""
        List of selected files.""")

    width = param.Integer(default=None, bounds=(0, None), allow_None=True, doc="""
        Width of the widget.""")

    _can_back = param.Boolean(default=False, doc="Whether the back button is enabled.")

    _can_forward = param.Boolean(default=False, doc="Whether the forward button is enabled.")

    _can_up = param.Boolean(default=False, doc="Whether the up button is enabled.")

    _crumbs = param.List(default=[], item_type=dict, doc="""
        Breadcrumb trail from the root directory to the current directory.""")

    _items = param.List(default=[], item_type=dict, doc="""
        The entries in the current directory.""")

    _esm_base = "FileSelector.jsx"

    _rename = {
        "file_pattern": None,
        "refresh_period": None,
        "root_directory": None,
        "show_hidden": None,
    }

    def __init__(
        self,
        directory: str | os.PathLike | None = None,
        fs: AbstractFileSystem | None = None,
        **params,
    ):
        provider = BaseFileProvider.from_filesystem(fs)
        if directory is not None:
            params["directory"] = directory

        # Navigation state has to exist before the first listing is built.
        self._provider = provider
        self._stack: list[str] = []
        self._position = -1
        self._cwd = ""
        self._push = True
        self._updating = False

        resolved = self._normalize(params.pop("directory", type(self).directory))
        root_directory = params.pop("root_directory", None)
        resolved_root = self._normalize(root_directory) if root_directory else resolved

        super().__init__(**params)

        # BaseFileSelector.__init__ is invoked as part of the cooperative
        # super() chain but does not see the fs argument, so it builds a
        # LocalFileProvider and normalizes whatever directory and
        # root_directory it is handed with it, which mangles remote paths
        # such as 's3://bucket'. Keep both out of that call and apply the
        # values normalized by the real provider afterwards.
        self._provider = provider
        self.param.update(directory=resolved, root_directory=resolved_root)

        self.param.watch(self._update_files, "directory")
        self.param.watch(self._reload, ["file_pattern", "only_files", "show_hidden"])
        self._update_files()

    #  ------------------------------------------------------------------
    #  Path helpers
    #  ------------------------------------------------------------------

    @property
    def _is_local(self) -> bool:
        return isinstance(self._provider, LocalFileProvider)

    @property
    def _sep(self) -> str:
        return getattr(self._provider, "sep", os.path.sep)

    def _normalize(self, path: str | os.PathLike, root: str | None = None) -> str:
        """
        Normalize a path through the provider and, for remote providers,
        canonicalize the separators.

        Remote paths are compared textually by the root check, so they have
        to arrive in one form. Two things get in the way: `fsspec`
        implementations disagree on whether the names they list are
        absolute, so `RemoteFileProvider.ls` can return 'memory:///a' where
        the directory is 'memory://a'; and a caller can hand in a path
        built with the OS separator, e.g. `os.path.join` on Windows, while
        the provider lists with '/'.
        """
        normalized = str(self._provider.normalize(path, root))
        if self._is_local:
            return normalized
        normalized = normalized.replace(os.path.sep, self._sep)
        scheme, sep, rest = normalized.partition("://")
        return f"{scheme}://{rest.lstrip('/')}" if sep else normalized

    def _basename(self, path: str) -> str:
        stripped = path.rstrip(self._sep)
        if self._sep in stripped:
            return stripped.rsplit(self._sep, 1)[-1]
        return stripped or path

    def _strip(self, path: str) -> str:
        return path.rstrip(self._sep) or self._sep

    def _parent_path(self, path: str) -> str:
        stripped = self._strip(path)
        if self._sep not in stripped:
            return stripped
        return stripped.rsplit(self._sep, 1)[0] or self._sep

    def _same_path(self, path: str, other: str) -> bool:
        if self._is_local:
            try:
                return pathlib.Path(path).resolve() == pathlib.Path(other).resolve()
            except OSError:
                return False
        return self._strip(path) == self._strip(other)

    def _is_within_root(self, path: str) -> bool:
        """
        Whether the supplied path is the root directory or contained by
        it. Symlinks are resolved, so a symlink inside the root pointing
        outside it is rejected, and the comparison is path based, so a
        sibling directory sharing a name prefix with the root does not
        pass.
        """
        root = self._root_directory
        if not root:
            return True
        if self._is_local:
            try:
                resolved = pathlib.Path(path).resolve()
                resolved_root = pathlib.Path(root).resolve()
            except OSError:
                return False
            return resolved.is_relative_to(resolved_root)
        stripped, stripped_root = self._strip(path), self._strip(root)
        if stripped == stripped_root:
            return True
        prefix = stripped_root if stripped_root.endswith(self._sep) else stripped_root + self._sep
        return stripped.startswith(prefix)

    def _at_root(self, path: str) -> bool:
        root = self._root_directory
        return bool(root) and self._same_path(path, root)

    #  ------------------------------------------------------------------
    #  Listing
    #  ------------------------------------------------------------------

    def _list_items(self, path: str) -> list[dict[str, t.Any]]:
        items: list[dict[str, t.Any]] = []
        if not self._at_root(path):
            items.append({
                "name": "..",
                "path": self._parent_path(path),
                "type": "directory",
                "parent": True,
            })
        dirs, files = self._provider.ls(path, self.file_pattern)
        for is_dir, paths in ((True, sorted(dirs)), (False, sorted(files))):
            for entry in paths:
                name = self._basename(entry)
                if not self.show_hidden and name.startswith("."):
                    continue
                canonical = self._normalize(entry)
                item: dict[str, t.Any] = {
                    "name": name,
                    "path": self._strip(canonical) if is_dir else canonical,
                    "type": "directory" if is_dir else "file",
                }
                if not is_dir and self._is_local:
                    try:
                        stat = os.stat(entry)
                    except OSError:
                        pass
                    else:
                        item["size"] = stat.st_size
                        item["modified"] = stat.st_mtime
                items.append(item)
        return items

    def _get_crumbs(self, path: str) -> list[dict[str, str]]:
        root = self._root_directory
        if not root:
            return [{"name": self._basename(path) or path, "path": path}]
        crumbs = [{"name": self._basename(root) or root, "path": root}]
        if self._same_path(path, root):
            return crumbs
        stripped, stripped_root = self._strip(path), root.rstrip(self._sep)
        if not stripped.startswith(stripped_root):
            # e.g. the directory was reached through a symlink
            return crumbs + [{"name": self._basename(path), "path": path}]
        current = stripped_root
        for part in stripped[len(stripped_root):].split(self._sep):
            if not part:
                continue
            current = f"{current}{self._sep}{part}"
            crumbs.append({"name": part, "path": current})
        return crumbs

    def _update_files(
        self, event: param.parameterized.Event | None = None, refresh: bool = False
    ):
        if self._updating:
            return
        self._updating = True
        try:
            self._relist(refresh)
        finally:
            self._updating = False

    def _relist(self, refresh: bool = False):
        if refresh:
            path = self._cwd or self._normalize(self.directory, self._root_directory)
        else:
            path = self._normalize(self.directory, self._root_directory)
        if not self._is_within_root(path) or not self._provider.isdir(path):
            self._items = []
            self._crumbs = self._get_crumbs(path)
            return
        if self._push and path != self._cwd:
            del self._stack[self._position+1:]
            self._stack.append(path)
            self._position = len(self._stack) - 1
        self._cwd = path
        self._items = self._list_items(path)
        self._crumbs = self._get_crumbs(path)
        self._can_back = self._position > 0
        self._can_forward = self._position < len(self._stack) - 1
        self._can_up = not self._at_root(path)
        # Settle the parameter on the canonical form, e.g. after a remote
        # path was handed in with the OS separator. The re-entrant
        # _update_files this triggers is dropped by the guard above.
        self.directory = path

    def _reload(self, event: param.parameterized.Event):
        if event.name == "only_files" and event.new:
            self.value = [v for v in self.value if not self._provider.isdir(str(v))]
        self._update_files(refresh=True)

    def _navigate(self, path: str, push: bool = True):
        self._push = push
        try:
            if self.directory == path:
                self._update_files()
            else:
                self.directory = path
        finally:
            self._push = True

    #  ------------------------------------------------------------------
    #  Frontend communication
    #  ------------------------------------------------------------------

    def _filter_value(self, value: list[str]) -> list[str]:
        listed = {
            item["path"] for item in self._items if not item.get("parent")
        }
        selected = {str(v) for v in self.value}
        filtered = []
        for path in value:
            if path not in listed and path not in selected:
                continue
            if self.only_files and self._provider.isdir(path):
                continue
            filtered.append(path)
        return filtered

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        if "value" in msg:
            msg["value"] = self._filter_value(msg["value"])
        if "directory" in msg:
            path = self._normalize(msg["directory"], self._root_directory)
            if self._is_within_root(path) and self._provider.isdir(path):
                msg["directory"] = path
            else:
                del msg["directory"]
                self._send_msg({
                    "type": "directory", "directory": self._cwd or self.directory
                })
        return msg

    def _handle_msg(self, msg):
        action = msg.get("type") if isinstance(msg, dict) else None
        if action == "back":
            if self._position > 0:
                self._position -= 1
                self._navigate(self._stack[self._position], push=False)
        elif action == "forward":
            if self._position < len(self._stack) - 1:
                self._position += 1
                self._navigate(self._stack[self._position], push=False)
        elif action == "up":
            if self._can_up:
                self._navigate(self._parent_path(self._cwd))
        elif action == "reload":
            self._update_files(refresh=True)


__all__ = ["FileSelector"]
