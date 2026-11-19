"""Opt-in rendering of simple Material UI trees in a single React root."""

from __future__ import annotations

import re
import typing as t
import weakref
from functools import partial
from pathlib import Path
from types import SimpleNamespace

import panel
import param
from bokeh.models.css import ImportedStyleSheet, InlineStyleSheet
from panel.custom import ReactiveESM
from panel.io.resources import CDN_DIST
from panel.links import Callback, Link
from panel.models.reactive_html import DOMEvent
from panel.util import edit_readonly
from panel.viewable import Child, Children, Viewable

from .base import MaterialComponent, _align_rendered_explicit
from .template.base import Page


def _is_compilable(cls: type) -> bool:
    # Opting in is not inherited, a subclass may render differently.
    return bool(vars(cls).get("_compilable"))


_CHILD_PARAMS: dict[type, tuple[tuple[str, bool], ...]] = {}
_DATA_DEFAULTS: dict[type, dict] = {}

# Parameters that decide whether a component can be compiled at all.
_STRUCTURAL = frozenset((
    "loading", "theme_config", "attached", "description", "sizing_mode", "stylesheets",
    "scroll", "view_latest", "scroll_index", "auto_scroll_limit", "scroll_button_threshold",
    "scroll_position", "href",
))
_SCROLL = (
    "scroll", "view_latest", "scroll_index", "auto_scroll_limit",
    "scroll_button_threshold", "scroll_position", "href",
)
_LAYOUT = (
    "width", "height", "min_width", "max_width", "min_height", "max_height", "margin",
    "aspect_ratio", "sizing_mode", "width_policy", "height_policy", "align",
)
_MAX_ORPHANS = 32
_ROOT_SIZING = (
    "sizing_mode", "width", "height", "min_width", "min_height", "max_width", "max_height",
    "width_policy", "height_policy",
)


def _child_params(cls: type) -> tuple[tuple[str, bool], ...]:
    children = _CHILD_PARAMS.get(cls)
    if children is None:
        _CHILD_PARAMS[cls] = children = tuple(
            (name, isinstance(parameter, Children))
            for name, parameter in cls.param.objects(instance=False).items()
            if isinstance(parameter, (Child, Children))
        )
    return children


def _node_properties(obj: MaterialComponent) -> tuple[dict, dict]:
    """
    Returns the model properties of a component and the values of its data
    properties, without building the Bokeh data model if possible since a
    compiled node is never rendered as one.
    """
    cls = type(obj)
    spec = getattr(cls, "_esm_spec", None)
    if spec is None or cls._get_properties is not MaterialComponent._get_properties:
        properties = obj._get_properties(None)
        data = properties["data"]
        values = data.properties_with_values(include_defaults=False)
    else:
        properties = super(ReactiveESM, obj)._get_properties(None)
        values = {name: properties.pop(name) for name in spec().data if name in properties}
        values["esm_constants"] = obj._constants
        values["loading"] = obj.loading
    defaults = _DATA_DEFAULTS.get(cls)
    if defaults is None:
        _DATA_DEFAULTS[cls] = defaults = cls._data_model().properties_with_values()
    return properties, {**defaults, **values}


def _subtree(node: dict):
    yield node
    for children in node.get("children", {}).values():
        for child in children if isinstance(children, list) else [children]:
            if child is not None:
                yield from _subtree(child)


def _differs(value, default) -> bool:
    try:
        return bool(value != default)
    except Exception:
        return True


class _Context:
    """
    State of one compile. The fallbacks, stylesheets and kinds of the tree
    are only ever appended to, so that the nodes compiled before keep
    referring to the right entries.
    """

    def __init__(self, fallbacks: list[Viewable], tree: dict | None = None):
        self.fallbacks = fallbacks
        self.slots = {id(obj): slot for slot, obj in enumerate(fallbacks)}
        self.known_styles: dict[str, str] = tree["shared_styles"] if tree else {}
        self.shared_styles: dict[str, str] = {}
        self.known_kinds: dict[str, dict] = tree["kinds"] if tree else {}
        self.kinds: dict[str, dict] = {}
        self.known_sheets: int = len(tree["sheets"]) if tree else 0
        self.sheet_index: dict[tuple, int] = (
            {tuple(sheet.items()): index for index, sheet in enumerate(tree["sheets"])} if tree else {}
        )
        self.sheets: list[dict] = []
        self.layouts: dict[str, dict] = {}
        self.nodes: dict[str, Viewable] = {}
        self.active: set[Viewable] = set()
        self.dicts: dict[str, dict] = {}


class Compiled(MaterialComponent):
    """Render compilable PMUI components directly in one React root.

    Unsupported components retain their ordinary Panel models and rendering.
    """

    source = param.Parameter(allow_None=False, allow_refs=False)
    tree = param.Dict(default={})
    patch = param.Dict(default={})
    fallbacks = Children()
    _custom_theme = param.List(default=[])

    _esm_base = "Compiled.jsx"
    # The nodes of the tree are themed, each by its own component.
    _esm_transforms = []
    _rename = {"source": None}
    _source_transforms = {"fallbacks": None}

    @classmethod
    def _render_esm_base(cls):
        # The bundler renders Compiled before Page enters subclass discovery.
        components = (
            component for component in (Page, *param.concrete_descendents(MaterialComponent).values())
            if _is_compilable(component) and component._esm_base and
            component.__module__.startswith("panel_material_ui.")
        )
        modules: dict[str, str] = {}
        registry: dict[str, str] = {}
        for component in components:
            stem = component._esm_path(compiled="compiling").stem
            if stem not in modules:
                modules[stem] = f"Renderer{len(modules)}"
            registry[component.__name__] = modules[stem]
        imports = "\n".join(f'import {name} from "./{stem}"' for stem, name in modules.items())
        entries = ", ".join(f"{name}: {renderer}" for name, renderer in registry.items())
        return super()._render_esm_base().replace(
            'import pmui from "panel-material-ui"', f"{imports}\nconst pmui = {{{entries}}}"
        )

    def __init__(self, source: Viewable, **params):
        if not isinstance(source, Viewable):
            raise TypeError("Compiled requires a Panel Viewable")
        self._subscriptions: dict[Viewable, param.parameterized.Watcher] = {}
        self._nodes: dict[str, Viewable] = {}
        self._node_dicts: dict[str, dict] = {}
        self._active_nodes: set[Viewable] = set()
        self._failed_stylesheets: set[str] = set()
        self._model_docs = {}
        self._rev = 0
        self._held: list | None = None
        self._earlier: list[dict] = []
        self._orphans = 0
        self._stale = False
        self._echo: dict | None = None
        tree, ctx = self._compile(source)
        self._inherit_sizing = "sizing_mode" not in params
        self._inherit_theme = "dark_theme" not in params
        if self._inherit_sizing and tree["root"]["kind"] != "fallback":
            params["sizing_mode"] = tree["root"]["layout"].get("sizing_mode")
        if self._inherit_theme and isinstance(source, Page):
            params["dark_theme"] = source.dark_theme
        super().__init__(source=source, tree=tree, fallbacks=ctx.fallbacks, **params)
        owner = weakref.ref(self)

        def changed(*events):
            if instance := owner():
                instance._change_events(*events)

        self._change = changed
        weakref.finalize(self, self._unwatch, self._subscriptions)
        self._node_dicts = ctx.dicts
        self._watch_nodes(ctx.nodes, ctx.active)
        self.param.watch(self._rebuild, "source")

    @staticmethod
    def _unwatch(subscriptions):
        for obj, watcher in subscriptions.items():
            obj.param.unwatch(watcher)
        subscriptions.clear()

    def _compile(self, source: Viewable) -> tuple[dict, _Context]:
        ctx = _Context([])
        # Compiled before the source parameter is set on construction.
        self._root = source
        root = self._compile_node(source, ctx)
        self._rev += 1
        self._orphans = 0
        tree = {
            "root": root, "shared_styles": ctx.shared_styles, "kinds": ctx.kinds,
            "sheets": ctx.sheets, "state": {"rev": self._rev},
        }
        return tree, ctx

    def _fallback_node(self, obj: Viewable, ctx: _Context) -> dict:
        node_id = str(id(obj))
        # A fallback keeps its slot, its view is already mounted there.
        slot = ctx.slots.get(id(obj))
        if slot is None:
            ctx.slots[id(obj)] = slot = len(ctx.fallbacks)
            ctx.fallbacks.append(obj)
        node = {"id": node_id, "kind": "fallback", "slot": slot,
                "sizing_mode": getattr(obj, "sizing_mode", None)}
        ctx.dicts[node_id] = node
        return node

    def _compile_node(self, obj: Viewable, ctx: _Context) -> dict:
        node_id = str(id(obj))
        cls = type(obj)
        candidate = isinstance(obj, MaterialComponent) and _is_compilable(cls)
        if candidate:
            ctx.nodes[node_id] = obj
        compilable = (
            candidate and cls.__module__.startswith("panel_material_ui.") and obj._esm_base and
            node_id not in self._failed_stylesheets and
            (not isinstance(obj, Page) or obj is self._root) and
            not (
                obj.loading or (obj.theme_config and not isinstance(obj, Page)) or
                getattr(obj, "attached", None) or getattr(obj, "description", None) or
                Callback.registry.get(obj) or any(
                    isinstance(link, Link) and link.target is obj
                    for links in Callback.registry.values() for link in links
                ) or obj.sizing_mode == "inherit"
            ) and not any(getattr(obj, name, None) for name in _SCROLL)
        )
        if not compilable:
            return self._fallback_node(obj, ctx)
        properties, values = _node_properties(obj)
        stylesheets = []
        for stylesheet in properties["stylesheets"]:
            if isinstance(stylesheet, ImportedStyleSheet):
                url = stylesheet.url
                prefix = f"{CDN_DIST}css/"
                filename = url.partition("?")[0].removeprefix(prefix)
                local = Path(panel.__file__).parent / "dist" / "css" / filename
                if url.startswith(prefix) and filename == Path(filename).name and local.is_file():
                    css = ctx.known_styles.get(url) or ctx.shared_styles.get(url)
                    if css is None:
                        css = local.read_text()
                    if re.search(r"@import\b", css, re.IGNORECASE):
                        return self._fallback_node(obj, ctx)
                    if url not in ctx.known_styles:
                        ctx.shared_styles[url] = css
                    stylesheets.append({"base_url": url})
                else:
                    stylesheets.append({"url": url})
            else:
                css = stylesheet.css if isinstance(stylesheet, InlineStyleSheet) else stylesheet
                if re.search(r"@import\b", css, re.IGNORECASE):
                    return self._fallback_node(obj, ctx)
                stylesheets.append({"css": css})
        ctx.active.add(obj)
        # Whatever most nodes share is sent once: the defaults of a kind of
        # component and the stylesheets, which a node refers to by index.
        kind = ctx.known_kinds.get(cls.__name__) or ctx.kinds.get(cls.__name__)
        if kind is None:
            ctx.kinds[cls.__name__] = kind = {
                "props": {name: _DATA_DEFAULTS[cls][name] for name in obj._linked_properties},
                "constants": values["esm_constants"],
            }
        sheets = []
        for stylesheet in stylesheets:
            key = tuple(stylesheet.items())
            index = ctx.sheet_index.get(key)
            if index is None:
                ctx.sheet_index[key] = index = ctx.known_sheets + len(ctx.sheets)
                ctx.sheets.append(stylesheet)
            sheets.append(index)
        layout = ctx.layouts[node_id] = {name: properties.get(name) for name in _LAYOUT}
        node = {
            "id": node_id,
            "kind": cls.__name__,
            "layout": layout,
            "props": {
                name: values[name] for name in obj._linked_properties
                if _differs(values[name], kind["props"][name])
            },
        }
        if sheets:
            node["stylesheets"] = sheets
        if properties["css_classes"]:
            node["css_classes"] = properties["css_classes"]
        if properties["styles"]:
            node["styles"] = properties["styles"]
        if not obj.visible:
            node["visible"] = False
        if _differs(values["esm_constants"], kind["constants"]):
            node["constants"] = values["esm_constants"]
        ctx.dicts[node_id] = node
        children: dict = {}
        for name, multiple in _child_params(cls):
            value = getattr(obj, name)
            if multiple:
                children[name] = [self._compile_node(child, ctx) for child in value]
            else:
                children[name] = self._compile_node(value, ctx) if value is not None else None
        node["children"] = children
        if hasattr(obj, "_compute_sizing_mode") and "objects" in children:
            sizing_children = []
            for child in children["objects"]:
                child_layout = ctx.layouts.get(child["id"])
                if child_layout is None:
                    fallback = ctx.fallbacks[child["slot"]]
                    child_layout = {name: getattr(fallback, name, None) for name in (
                        "width", "height", "min_width", "min_height", "sizing_mode"
                    )}
                sizing_children.append(SimpleNamespace(**child_layout))
            layout.update(obj._compute_sizing_mode(sizing_children, properties))
        node["layout"] = {name: value for name, value in layout.items() if value is not None}
        return node

    def _watch_nodes(self, nodes: dict[str, Viewable], active: set[Viewable]) -> None:
        current = set(nodes.values())
        for obj, watcher in list(self._subscriptions.items()):
            if obj not in current:
                obj.param.unwatch(watcher)
                del self._subscriptions[obj]
        for obj in current - self._subscriptions.keys():
            self._subscriptions[obj] = obj.param.watch(
                self._change, list(obj.param), onlychanged=True
            )
        for obj in self._active_nodes - active:
            obj._compiled_roots.discard(self)
        for obj in active - self._active_nodes:
            if not hasattr(obj, "_compiled_roots"):
                obj._compiled_roots = weakref.WeakSet()
            obj._compiled_roots.add(self)
        self._active_nodes = active
        self._nodes = nodes
        self._stale = False

    def _change_events(self, *events) -> None:
        """
        Applies parameter changes on a node with the cheapest update that
        is still correct: a patch of the changed properties, a recompile of
        the node's subtree or, if its ancestors are affected, of the tree.
        """
        obj = events[0].obj
        names = {event.name for event in events}
        if obj not in self._active_nodes:
            if names & _STRUCTURAL:
                self._rebuild(*events)
            return
        children = {name for name, _ in _child_params(type(obj))}
        if names & _STRUCTURAL or obj is self.source and names & children:
            return self._rebuild(*events)
        if names & children:
            return self._patch_subtree(obj)
        try:
            msg = obj._process_param_change({event.name: event.new for event in events})
        except Exception:
            return self._rebuild(*events)
        linked = obj._linked_properties
        if any(name != "visible" and name not in linked for name in msg):
            if obj is self.source:
                return self._rebuild(*events)
            return self._patch_subtree(obj)
        self._patch_props(obj, msg)
        if obj is self.source and self._inherit_theme and "dark_theme" in names and isinstance(obj, Page):
            self.dark_theme = obj.dark_theme

    def _held_events(self) -> list | None:
        for model, _ in self._models.values():
            doc = model.document
            if doc is not None and doc.callbacks.hold_value:
                return doc.callbacks._held_events
        return None

    def _send_patch(self, ops: list[dict], **updates) -> None:
        self._rev += 1
        self.tree["state"]["rev"] = self._rev
        # While a document holds its events only the last value of the patch
        # is sent, so it carries the patches made earlier in the same hold.
        held = self._held_events()
        if held is None or held is not self._held:
            self._earlier = []
        self._held = held
        patch = {"rev": self._rev, "ops": ops}
        if self._earlier:
            patch["earlier"] = list(self._earlier)
        self._earlier.append({"rev": self._rev, "ops": ops})
        self.param.update(patch=patch, **updates)

    def _patch_props(self, obj: Viewable, msg: dict) -> None:
        node_id = str(id(obj))
        node = self._node_dicts[node_id]
        op: dict = {"id": node_id}
        props, acks = {}, {}
        echo = self._echo
        for name, value in msg.items():
            if name == "visible":
                node["visible"] = op["visible"] = value
                continue
            node["props"][name] = value
            if echo is not None and echo["obj"] is obj and echo["name"] == name:
                echo["handled"] = True
                try:
                    unchanged = bool(value == echo["value"])
                except Exception:
                    unchanged = False
                # The client that made the edit already shows this value.
                if unchanged and len(self._models) <= 1:
                    continue
                acks[name] = [echo["root"], echo["seq"]]
            props[name] = value
        if props:
            op["props"] = props
        if acks:
            op["acks"] = acks
        if len(op) > 1:
            self._send_patch([op])

    def _patch_subtree(self, obj: Viewable) -> None:
        node_id = str(id(obj))
        old = self._node_dicts.get(node_id)
        if old is None or old["kind"] == "fallback":
            return self._rebuild()
        removed = list(_subtree(old))
        ctx = _Context(list(self.fallbacks), self.tree)
        new = self._compile_node(obj, ctx)
        kept = {node["id"] for node in _subtree(new) if node["kind"] == "fallback"}
        orphans = sum(1 for node in removed if node["kind"] == "fallback" and node["id"] not in kept)
        # The sizing of the ancestors is computed from the layout of this node.
        if new["kind"] == "fallback" or new["layout"] != old["layout"] or self._orphans + orphans > _MAX_ORPHANS:
            return self._rebuild()
        self._orphans += orphans
        removed_ids = {node["id"] for node in removed}
        for removed_id in removed_ids:
            self._node_dicts.pop(removed_id, None)
        old.clear()
        old.update(new)
        ctx.dicts[node_id] = old
        self._node_dicts.update(ctx.dicts)
        nodes = {key: value for key, value in self._nodes.items() if key not in removed_ids}
        nodes.update(ctx.nodes)
        active = {node for node in self._active_nodes if str(id(node)) not in removed_ids} | ctx.active
        self._watch_nodes(nodes, active)
        op = {"id": node_id, "subtree": new}
        for name, added in (("shared_styles", ctx.shared_styles), ("kinds", ctx.kinds), ("sheets", ctx.sheets)):
            if added:
                op[name] = added
                if isinstance(added, list):
                    self.tree[name].extend(added)
                else:
                    self.tree[name].update(added)
        updates = {}
        if len(ctx.fallbacks) != len(self.fallbacks):
            updates["fallbacks"] = ctx.fallbacks
        self._send_patch([op], **updates)

    def _rebuild(self, *events) -> None:
        for event in events:
            if event.name == "stylesheets":
                self._failed_stylesheets.discard(str(id(event.obj)))
        tree, ctx = self._compile(self.source)
        self._node_dicts = ctx.dicts
        self._watch_nodes(ctx.nodes, ctx.active)
        updates = {"tree": tree, "fallbacks": ctx.fallbacks}
        root = tree["root"]
        if self._inherit_sizing and root["kind"] != "fallback":
            updates["sizing_mode"] = root["layout"].get("sizing_mode")
        if self._inherit_theme and isinstance(self.source, Page):
            updates["dark_theme"] = self.source.dark_theme
        self.param.update(**updates)
        for model, _ in self._models.values():
            self._sync_fallback_sizing(model)
        if isinstance(self.source, Page):
            for model, _ in self._models.values():
                if doc := self._model_docs.get(model.id):
                    self._sync_custom_theme(model, doc)

    def _sync_custom_theme(self, model, doc):
        custom = doc.theme is not self.source._design.theme.bokeh_theme
        model.data._custom_theme = list(doc.theme._json.get("attrs", {})) if custom else []

    def _handle_msg(self, msg) -> None:
        if msg.get("type") == "resync":
            return self._rebuild()
        obj = self._nodes.get(msg.get("id"))
        if obj is None or obj not in self._active_nodes:
            return
        if msg.get("type") == "stylesheet_failure":
            self._failed_stylesheets.add(msg["id"])
            self._rebuild()
        elif msg.get("type") == "msg":
            obj._handle_msg(msg["data"])
        elif msg.get("type") == "update":
            name = msg.get("name")
            if name not in obj._linked_properties:
                return
            echo = self._echo = {
                "obj": obj, "name": name, "value": msg["value"], "root": msg.get("root"),
                "seq": msg.get("seq"), "handled": False,
            }
            try:
                changes = obj._process_property_change({name: msg["value"]})
                if changes and not {child for child, _ in _child_params(type(obj))} & changes.keys():
                    with edit_readonly(obj):
                        obj.param.update(**changes)
                if not echo["handled"] and changes and obj in self._active_nodes:
                    # The edit was rejected or coerced without an event, so
                    # the client has to be told what the value really is.
                    current = obj._process_param_change({key: getattr(obj, key) for key in changes})
                    if name in current:
                        self._patch_props(obj, {name: current[name]})
            finally:
                self._echo = None
        elif msg.get("type") == "event":
            obj._process_event(DOMEvent(model=None, node=msg["name"], data=msg.get("data")))

    def select(self, selector=None):
        matches = selector is None or (
            isinstance(self, selector) if isinstance(selector, type) else selector(self)
        )
        return ([self] if matches else []) + self.source.select(selector)

    def _send_node_msg(self, obj: Viewable, data: t.Any) -> None:
        """
        Forwards a message a compiled component sends to its frontend.
        """
        if obj in self._active_nodes:
            self._send_msg({"type": "node_msg", "id": str(id(obj)), "data": data})

    def _sync_fallback_sizing(self, model) -> None:
        # A root that renders through its own model sizes the Compiled
        # model around it, as it would size itself as the root.
        root = self.tree["root"]
        if not self._inherit_sizing or root["kind"] != "fallback":
            return
        child = model.data.fallbacks[root["slot"]]
        model.update(**{name: getattr(child, name) for name in _ROOT_SIZING})

    def _get_model(self, doc, root=None, parent=None, comm=None):
        if self._stale:
            self._rebuild()
        model = super()._get_model(doc, root, parent, comm)
        self._sync_fallback_sizing(model)
        if comm is None and doc.session_context:
            for obj in self._active_nodes:
                if obj._dark_theme_explicit:
                    doc.add_next_tick_callback(partial(_align_rendered_explicit, obj, doc))
        if isinstance(self.source, Page):
            for existing, _ in self._models.values():
                if existing_doc := self._model_docs.get(existing.id):
                    self._sync_custom_theme(existing, existing_doc)
            if doc:
                self._model_docs[model.id] = doc
                self._sync_custom_theme(model, doc)
        return model

    def server_doc(self, doc=None, title=None, location=True):
        page = self.source if isinstance(self.source, Page) else None
        if page is not None and title in (None, "Panel Application"):
            title = page.title or page.meta.title or "Panel Application"
        doc = super().server_doc(doc, title, location)
        if page is not None:
            page._populate_template_variables(doc.template_variables)
            doc.template = page._template
        return doc

    def save(self, filename, title=None, resources=None, template=None, template_variables=None, **kwargs):
        page = self.source if isinstance(self.source, Page) else None
        if page is not None:
            title = title or page.title or page.meta.title
            template = template if template is not None else page._template
            template_variables = dict(template_variables or {})
            page._populate_template_variables(template_variables)
        return super().save(filename, title, resources, template, template_variables, **kwargs)

    def _cleanup(self, root=None) -> None:
        super()._cleanup(root)
        active = {model.id for model, _ in self._models.values()}
        self._model_docs = {
            model_id: doc for model_id, doc in self._model_docs.items()
            if model_id in active
        }
        if not self._models:
            self._unwatch(self._subscriptions)
            for obj in self._active_nodes:
                obj._compiled_roots.discard(self)
            self._active_nodes = set()
            self._stale = True
