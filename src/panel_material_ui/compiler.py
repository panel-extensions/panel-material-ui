"""Opt-in rendering of simple Material UI trees in a single React root."""

from __future__ import annotations

import re
import weakref
from pathlib import Path
from types import SimpleNamespace

import panel
import param
from bokeh.models.css import ImportedStyleSheet, InlineStyleSheet
from panel.io.resources import CDN_DIST
from panel.links import Callback, Link
from panel.util import edit_readonly
from panel.viewable import Child, Children, Viewable

from .base import MaterialComponent
from .template.base import Page


class Compiled(MaterialComponent):
    """Render compilable PMUI components directly in one React root.

    Unsupported components retain their ordinary Panel models and rendering.
    """

    source = param.Parameter(allow_None=False, allow_refs=False)
    tree = param.Dict(default={})
    fallbacks = Children()
    _custom_theme = param.List(default=[])

    _esm_base = "Compiled.jsx"
    _rename = {"source": None}
    _source_transforms = {"fallbacks": None}

    @classmethod
    def _render_esm_base(cls):
        # The bundler renders Compiled before Page enters subclass discovery.
        components = (
            component for component in (Page, *param.concrete_descendents(MaterialComponent).values())
            if component._compilable and component._esm_base and
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
        self._active_nodes: set[Viewable] = set()
        self._failed_stylesheets: set[str] = set()
        self._acks: dict[str, dict[str, dict[str, int]]] = {}
        self._model_docs = {}
        self._theme_revision = 0
        tree, fallbacks, nodes, active = self._compile(source)
        self._inherit_sizing = "sizing_mode" not in params
        self._inherit_theme = "dark_theme" not in params
        if self._inherit_sizing and tree["kind"] != "fallback":
            params["sizing_mode"] = tree["layout"]["sizing_mode"]
        if self._inherit_theme and isinstance(source, Page):
            params["dark_theme"] = source.dark_theme
        super().__init__(source=source, tree=tree, fallbacks=fallbacks, **params)
        owner = weakref.ref(self)

        def changed(*events):
            if instance := owner():
                instance._rebuild(*events)

        self._change = changed
        weakref.finalize(self, self._unwatch, self._subscriptions)
        self._watch_nodes(nodes, active)
        self.param.watch(self._rebuild, "source")

    @staticmethod
    def _unwatch(subscriptions):
        for obj, watcher in subscriptions.items():
            obj.param.unwatch(watcher)
        subscriptions.clear()

    def _compile(self, source: Viewable) -> tuple[dict, list[Viewable], dict[str, Viewable], set[Viewable]]:
        fallbacks: list[Viewable] = []
        nodes: dict[str, Viewable] = {}
        active: set[Viewable] = set()
        shared_styles: dict[str, str] = {}

        def walk(obj: Viewable) -> dict:
            node_id = str(id(obj))
            compilable = (
                isinstance(obj, MaterialComponent) and type(obj)._compilable and
                type(obj).__module__.startswith("panel_material_ui.") and obj._esm_base and
                node_id not in self._failed_stylesheets and
                (not isinstance(obj, Page) or obj is source) and
                not (
                    obj.loading or (obj.theme_config and not isinstance(obj, Page)) or
                    getattr(obj, "attached", None) or getattr(obj, "description", None) or
                    Callback.registry.get(obj) or any(
                        isinstance(link, Link) and link.target is obj
                        for links in Callback.registry.values() for link in links
                    ) or obj.sizing_mode == "inherit"
                )
            )
            if isinstance(obj, MaterialComponent) and type(obj)._compilable:
                nodes[node_id] = obj
            if any(getattr(obj, name, None) for name in (
                "scroll", "view_latest", "scroll_index", "auto_scroll_limit",
                "scroll_button_threshold", "scroll_position", "href",
            )):
                compilable = False
            if compilable:
                properties = obj._get_properties(None)
                if any(
                    re.search(r"@import\b", sheet if isinstance(sheet, str) else sheet.css, re.IGNORECASE)
                    for sheet in properties["stylesheets"]
                    if isinstance(sheet, (str, InlineStyleSheet))
                ):
                    compilable = False
            if compilable:
                data = properties["data"]
                values = data.properties_with_values()
                props = {name: values[name] for name in obj._linked_properties}
                stylesheets = []
                for stylesheet in properties["stylesheets"]:
                    if isinstance(stylesheet, ImportedStyleSheet):
                        url = stylesheet.url
                        prefix = f"{CDN_DIST}css/"
                        filename = url.partition("?")[0].removeprefix(prefix)
                        local = Path(panel.__file__).parent / "dist" / "css" / filename
                        if url.startswith(prefix) and filename == Path(filename).name and local.is_file():
                            if url not in shared_styles:
                                shared_styles[url] = local.read_text()
                            if re.search(r"@import\b", shared_styles[url], re.IGNORECASE):
                                compilable = False
                                break
                            stylesheets.append({"base_url": url})
                        else:
                            stylesheets.append({"url": url})
                    elif isinstance(stylesheet, InlineStyleSheet):
                        stylesheets.append({"css": stylesheet.css})
                    else:
                        stylesheets.append({"css": stylesheet})
                if not compilable:
                    slot = len(fallbacks)
                    fallbacks.append(obj)
                    return {"id": node_id, "kind": "fallback", "slot": slot,
                            "sizing_mode": getattr(obj, "sizing_mode", None)}
                active.add(obj)
                node = {
                    "id": node_id,
                    "kind": type(obj).__name__,
                    "css_classes": properties["css_classes"],
                    "stylesheets": stylesheets,
                    "styles": properties["styles"],
                    "visible": obj.visible,
                    "layout": {
                        name: properties.get(name) for name in (
                            "width", "height", "min_width", "max_width", "min_height",
                            "max_height", "margin", "aspect_ratio", "sizing_mode",
                            "width_policy", "height_policy", "align",
                        )
                    },
                    "constants": values["esm_constants"],
                    "props": props,
                    "theme_revision": self._theme_revision,
                    "acks": {
                        root: entries.copy() for root, entries in self._acks.get(node_id, {}).items()
                    },
                }
                children = {}
                for name in obj.param:
                    parameter = obj.param[name]
                    if isinstance(parameter, Child):
                        child = getattr(obj, name)
                        children[name] = walk(child) if child is not None else None
                    elif isinstance(parameter, Children):
                        children[name] = [walk(child) for child in getattr(obj, name)]
                    if name in children:
                        props[name] = children[name]
                node["children"] = children
                if hasattr(obj, "_compute_sizing_mode") and "objects" in children:
                    sizing_children = []
                    for child in children["objects"]:
                        layout = child.get("layout")
                        if layout is None:
                            fallback = fallbacks[child["slot"]]
                            layout = {name: getattr(fallback, name, None) for name in (
                                "width", "height", "min_width", "min_height", "sizing_mode"
                            )}
                        sizing_children.append(SimpleNamespace(**layout))
                    node["layout"].update(obj._compute_sizing_mode(sizing_children, properties))
                return node
            slot = len(fallbacks)
            fallbacks.append(obj)
            return {"id": node_id, "kind": "fallback", "slot": slot,
                    "sizing_mode": getattr(obj, "sizing_mode", None)}

        tree = walk(source)
        tree["shared_styles"] = shared_styles
        return tree, fallbacks, nodes, active

    def _watch_nodes(self, nodes: dict[str, Viewable], active: set[Viewable]) -> None:
        current = set(nodes.values())
        for obj, watcher in list(self._subscriptions.items()):
            if obj not in current:
                obj.param.unwatch(watcher)
                del self._subscriptions[obj]
                self._acks.pop(str(id(obj)), None)
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

    def _rebuild(self, *events) -> None:
        for event in events:
            if event.name == "stylesheets":
                self._failed_stylesheets.discard(str(id(event.obj)))
            elif event.name == "theme_config":
                self._theme_revision += 1
        tree, fallbacks, nodes, active = self._compile(self.source)
        self._watch_nodes(nodes, active)
        updates = {"tree": tree, "fallbacks": fallbacks}
        if self._inherit_sizing:
            updates["sizing_mode"] = tree["layout"]["sizing_mode"] if tree["kind"] != "fallback" else None
        if self._inherit_theme and isinstance(self.source, Page):
            updates["dark_theme"] = self.source.dark_theme
        self.param.update(**updates)
        if isinstance(self.source, Page):
            for model, _ in self._models.values():
                if doc := self._model_docs.get(model.id):
                    self._sync_custom_theme(model, doc)

    def _sync_custom_theme(self, model, doc):
        custom = doc.theme is not self.source._design.theme.bokeh_theme
        model.data._custom_theme = list(doc.theme._json.get("attrs", {})) if custom else []

    def _handle_msg(self, msg) -> None:
        obj = self._nodes.get(msg.get("id"))
        if obj is None or obj in self.fallbacks:
            return
        if msg.get("type") == "stylesheet_failure":
            self._failed_stylesheets.add(msg["id"])
            self._rebuild()
        elif msg.get("type") == "msg":
            obj._handle_msg(msg["data"])
        elif msg.get("type") == "update":
            if msg.get("name") not in obj._linked_properties:
                return
            acks = self._acks.setdefault(msg["id"], {}).setdefault(msg["root"], {})
            sequence = msg["seq"]
            if sequence <= acks.get(msg["name"], 0):
                return
            acks[msg["name"]] = sequence
            previous_tree = self.tree
            changes = obj._process_property_change({msg["name"]: msg["value"]})
            if changes and not any(isinstance(obj.param[name], (Child, Children)) for name in changes):
                with edit_readonly(obj):
                    obj.param.update(**changes)
            if self.tree is previous_tree:
                self._rebuild()
        elif (handler := getattr(obj, f"_handle_{msg.get('type')}", None)) is not None:
            handler(None)

    def _get_model(self, doc, root=None, parent=None, comm=None):
        self._rebuild()
        model = super()._get_model(doc, root, parent, comm)
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
        for acks in self._acks.values():
            for origin in acks.keys() - self._models.keys():
                del acks[origin]
        if not self._models:
            self._unwatch(self._subscriptions)
            for obj in self._active_nodes:
                obj._compiled_roots.discard(self)
            self._active_nodes.clear()
