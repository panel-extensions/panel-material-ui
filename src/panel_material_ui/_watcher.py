"""
Shared autoreload watching for the panel-material-ui bundle.

Every component renders from the same bundle, so rather than the per-instance
watcher Panel's ReactComponent sets up, a single watchfiles task serves all of
them. Components subscribe when they render and are notified when the bundle
changes.
"""
from __future__ import annotations

import asyncio
import os
import pathlib
import site
import sysconfig
import typing as t
import weakref

from panel.io.state import state

if t.TYPE_CHECKING:
    from .base import MaterialComponent

_STATE_ATTR = '_pmui_bundle_watcher'


def in_site_packages(path: pathlib.Path) -> bool:
    """
    Whether the given path lives inside one of the interpreter's
    site-packages directories, i.e. the library was installed normally
    rather than in editable/development mode.
    """
    candidates = [sysconfig.get_path(name) for name in ('purelib', 'platlib')]
    candidates += site.getsitepackages()
    try:
        candidates.append(site.getusersitepackages())
    except Exception:
        pass
    resolved = path.resolve()
    for candidate in candidates:
        if not candidate:
            continue
        try:
            if resolved.is_relative_to(pathlib.Path(candidate).resolve()):
                return True
        except OSError:
            continue
    return False


class BundleWatcher:
    """
    Watches the shared panel-material-ui bundle on behalf of every
    MaterialComponent instance.

    Subscribers are held weakly so a component going out of scope does not
    keep it alive.

    Note that in dev mode Panel's autoreload deletes panel_material_ui from
    sys.modules on every source change, so this module (and any module-level
    state) is recreated repeatedly. The instance therefore lives on
    panel.io.state, which is never reloaded, and is reused across reloads to
    avoid leaking a watcher task per reload. See get_bundle_watcher.
    """

    def __init__(self, path: pathlib.Path):
        self.path = path
        self._subscribers: weakref.WeakSet = weakref.WeakSet()
        self._stop_event: asyncio.Event | None = None
        self._task: asyncio.Task | None = None

    def subscribe(self, component: MaterialComponent) -> None:
        self._subscribers.add(component)
        self._ensure_running()

    def unsubscribe(self, component: MaterialComponent) -> None:
        self._subscribers.discard(component)

    def _ensure_running(self) -> None:
        if self._task is not None and not self._task.done():
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # Without a running loop there is nothing to schedule the
            # watcher on, e.g. when rendering to a static file.
            return
        self._stop_event = asyncio.Event()
        # Registering the event lets Panel's server stop the watcher on
        # shutdown alongside its own autoreload watchers.
        state._watch_events.append(self._stop_event)
        # Deliberately not scheduled via state.execute, which would bind the
        # task to whichever Document happens to be rendering; the watcher is
        # shared by all sessions and must outlive any one of them.
        self._task = loop.create_task(self._watch())

    async def _watch(self) -> None:
        import watchfiles
        stop_event = self._stop_event
        try:
            async for changes in watchfiles.awatch(self.path, stop_event=stop_event):
                if await self._is_complete_write(changes, watchfiles):
                    self._notify()
        finally:
            if stop_event in state._watch_events:
                state._watch_events.remove(stop_event)
            self._stop_event = None
            self._task = None

    async def _is_complete_write(self, changes, watchfiles) -> bool:
        """
        Whether any change represents a finished write. Bundlers write
        non-atomically, so a modification event may arrive while the file
        is still missing or only partially written.
        """
        updated = False
        for change, path in changes:
            if change != watchfiles.Change.modified:
                continue
            for _ in range(5):
                if os.path.exists(path):
                    updated = True
                    break
                await asyncio.sleep(0.1)
        return updated

    def _notify(self) -> None:
        for component in list(self._subscribers):
            try:
                component._update_esm()
            except Exception as e:
                state._handle_exception(e)


def get_bundle_watcher(path: pathlib.Path) -> BundleWatcher:
    """
    Returns the process-wide watcher for the given bundle, creating it on
    first use.

    Stashed on panel.io.state so that reloading this module in dev mode
    reuses the existing watcher instead of starting another one. The class
    is also reloaded, so an existing watcher is matched by attribute rather
    than isinstance.
    """
    watcher = getattr(state, _STATE_ATTR, None)
    if watcher is None or getattr(watcher, 'path', None) != path:
        watcher = BundleWatcher(path)
        setattr(state, _STATE_ATTR, watcher)
    return watcher


def current_bundle_watcher() -> BundleWatcher | None:
    """
    Returns the existing watcher, if any, without creating one.
    """
    return getattr(state, _STATE_ATTR, None)
