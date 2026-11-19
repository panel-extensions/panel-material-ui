"""
Components reach their model and host only through the component interface
(see utils.js), so they render the same through a Panel view and inside a
Compiled tree. Only the two hosts may touch what lies behind it.
"""
import pathlib
import re

import pytest

import panel_material_ui

SOURCES = pathlib.Path(panel_material_ui.__file__).parent
HOSTS = {"utils.js", "Compiled.jsx"}
FORBIDDEN = {
    r"\bview\b": "use the host instead of the Panel view",
    r"\bapply_flex\b|\bget_child_view\b": "size children with model.render_children(name, {direction})",
    r"\bget_child\(": "render children with model.render_children",
    r"msg:custom|lifecycle:|\.off\(": "subscribe with model.on(event, callback), which returns an unsubscribe",
    r"\besm_constants\b": "read constants from model.constants",
    r"\bmodel\.\w+ = ": "write with model.set({name: value}) or the setter of model.useState",
    r"\bshadow_el\b|\bmodel_proxy\b|\.data\.setv\b": "private to the Panel view",
}
# Keeps what a Panel view passes besides the interface off the DOM.
ALLOWED = re.compile(r"const \{model, host, view, el, data, \.\.\.other\} = props")


def _sources():
    for path in sorted(SOURCES.rglob("*.js*")):
        if "dist" in path.parts or path.name in HOSTS or path.suffix not in (".js", ".jsx"):
            continue
        yield path


@pytest.mark.parametrize("path", list(_sources()), ids=lambda path: str(path.relative_to(SOURCES)))
def test_component_only_uses_the_interface(path):
    problems = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(("import ", "//", "*", "/*")) or " from \"" in line or ALLOWED.search(line):
            continue
        for pattern, hint in FORBIDDEN.items():
            if re.search(pattern, line):
                problems.append(f"{path.name}:{number}: {stripped} ({hint})")
    assert not problems, "\n".join(problems)
