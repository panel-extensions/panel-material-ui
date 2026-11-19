"""
Writes two launchers per example app into a directory, one that serves the
app as it is and one that wraps whatever the app marks servable in Compiled.

    python make_apps.py <out_dir>
    panel serve <out_dir>/*.py --port 5111
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).parents[3]
APPS = {
    "branding": ROOT / "examples/apps/branding/app.py",
    "plotly": ROOT / "examples/apps/plotly_plots/app.py",
    "holoviz": ROOT / "examples/apps/styling/holoviz.py",
    "components": ROOT / "examples/components.py",
}

LAUNCHER = '''
import collections, json, os, sys, time

APP, MODE, NAME = {app!r}, {mode!r}, {name!r}
sys.path.insert(0, os.path.dirname(APP))

import panel as pn
from panel.viewable import ServableMixin, Viewable

import panel_material_ui as pmui
from panel_material_ui.template.base import Page

_info = {{"app": NAME, "mode": MODE, "compiled": {{}}, "fallbacks": {{}}}}

def _count(node, compiled, fallbacks, source):
    if node["kind"] == "fallback":
        name = type(source.fallbacks[node["slot"]]).__name__
        fallbacks[name] = fallbacks.get(name, 0) + 1
        return
    compiled[node["kind"]] = compiled.get(node["kind"], 0) + 1
    for value in node.get("children", {{}}).values():
        for child in (value if isinstance(value, list) else [value]):
            if isinstance(child, dict):
                _count(child, compiled, fallbacks, source)

def _reason(obj):
    from panel.links import Callback, Link
    from panel_material_ui.base import MaterialComponent
    from panel_material_ui.compiler import _SCROLL, _is_compilable
    if not isinstance(obj, MaterialComponent):
        return "not a pmui component"
    if not _is_compilable(type(obj)):
        return "not opted in"
    if obj.loading:
        return "loading"
    if obj.theme_config:
        return "theme_config"
    if getattr(obj, "attached", None):
        return "attached"
    if getattr(obj, "description", None):
        return "description"
    if Callback.registry.get(obj) or any(
        isinstance(link, Link) and link.target is obj for links in Callback.registry.values() for link in links
    ):
        return "jslink or jscallback"
    if obj.sizing_mode == "inherit":
        return "sizing_mode inherit"
    if any(getattr(obj, name, None) for name in _SCROLL):
        return "scroll options"
    return "stylesheet with @import or nested Page"

def _survey(source, compiled):
    from panel_material_ui.base import MaterialComponent
    from panel_material_ui.compiler import _is_compilable
    everything = source.select()
    material = [obj for obj in everything if isinstance(obj, MaterialComponent)]
    _info["viewables"] = len(everything)
    _info["pmui"] = len(material)
    _info["pmui_opted_in"] = sum(_is_compilable(type(obj)) for obj in material)
    _info["pmui_classes"] = dict(collections.Counter(type(obj).__name__ for obj in material).most_common())
    _info["other_classes"] = dict(collections.Counter(
        type(obj).__name__ for obj in everything if not isinstance(obj, MaterialComponent)
    ).most_common())
    _info["fallback_reasons"] = [
        [type(obj).__name__, _reason(obj), len(obj.select())] for obj in compiled.fallbacks
    ]

def _patched(original):
    def servable(self, *args, **kwargs):
        if isinstance(self, pmui.Compiled) or not isinstance(self, Viewable):
            return original(self, *args, **kwargs)
        compiled = pmui.Compiled(self)
        _count(compiled.tree["root"], _info["compiled"], _info["fallbacks"], compiled)
        _survey(self, compiled)
        original(compiled, *args, **kwargs)
        return self
    return servable

# The branding example configures the Page through a module that this
# branch does not have.
if not hasattr(pmui, "page"):
    pmui.page = Page

_classes = [cls for cls in (ServableMixin, Viewable, Page) if "servable" in vars(cls)]
_originals = {{cls: cls.servable for cls in _classes}}
_start = time.perf_counter()
try:
    if MODE == "compiled":
        for cls in _classes:
            cls.servable = _patched(_originals[cls])
    exec(compile(open(APP).read(), APP, "exec"), {{**globals(), "__file__": APP}})
finally:
    for cls, original in _originals.items():
        cls.servable = original
_info["python_ms"] = 1e3 * (time.perf_counter() - _start)
with open(os.path.join(os.path.dirname(__file__), "sessions.jsonl"), "a") as f:
    f.write(json.dumps(_info) + "\\n")
'''

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for name, app in APPS.items():
        for mode in ("classic", "compiled"):
            (out / f"{name}_{mode}.py").write_text(LAUNCHER.format(app=str(app), mode=mode, name=name))
