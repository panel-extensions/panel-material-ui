import json

import panel as pn
import pytest
from bokeh.document import Document

from panel_material_ui import (
    Button,
    Column,
    Compiled,
    Page,
    Row,
    TextInput,
    Typography,
)


def _nodes(node):
    yield node
    for children in node.get("children", {}).values():
        for child in children if isinstance(children, list) else [children]:
            if child is not None:
                yield from _nodes(child)


@pytest.fixture
def tree():
    button = Button(label="Run")
    text = TextInput(value="a")
    inner = Column(text, button)
    layout = Column(Typography("Title"), Row(inner))
    return Compiled(layout), layout, inner, text, button


def test_compiled_serializes_children_once(tree):
    compiled, *_ = tree
    for node in _nodes(compiled.tree["root"]):
        if node["kind"] != "fallback":
            assert not set(node["children"]) & set(node["props"])


def test_compiled_renders_a_single_component_model(tree):
    compiled, *_ = tree
    doc = Document()
    doc.add_root(compiled.get_root(doc))
    assert sum(type(model).__name__ == "ReactComponent" for model in doc.models) == 1


def test_compiled_does_not_recompile_on_render(tree):
    compiled, *_ = tree
    before = compiled.tree
    compiled.get_root(Document())
    assert compiled.tree is before


def test_compiled_property_change_sends_a_patch(tree):
    compiled, _, _, _, button = tree
    before = compiled.tree
    button.label = "Stop"
    assert compiled.tree is before
    assert compiled.patch["ops"] == [{"id": str(id(button)), "props": {"label": "Stop"}}]
    assert compiled.patch["rev"] == compiled.tree["state"]["rev"]
    node = next(node for node in _nodes(compiled.tree["root"]) if node["id"] == str(id(button)))
    assert node["props"]["label"] == "Stop"


def test_compiled_visible_change_sends_a_patch(tree):
    compiled, _, _, _, button = tree
    before = compiled.tree
    button.visible = False
    assert compiled.tree is before
    assert compiled.patch["ops"] == [{"id": str(id(button)), "visible": False}]


def test_compiled_child_change_recompiles_the_subtree(tree):
    compiled, _, inner, _, button = tree
    before = compiled.tree
    added = Button(label="New")
    inner.append(added)
    assert compiled.tree is before
    (op,) = compiled.patch["ops"]
    assert op["id"] == str(id(inner))
    assert [child["id"] for child in op["subtree"]["children"]["objects"]][-1] == str(id(added))
    added.label = "Renamed"
    assert compiled.patch["ops"] == [{"id": str(id(added)), "props": {"label": "Renamed"}}]
    inner.remove(added)
    added.label = "Ignored"
    assert compiled.patch["ops"][0]["id"] == str(id(inner))


def test_compiled_subtree_change_appends_fallbacks(tree):
    compiled, _, inner, *_ = tree
    markdown = pn.pane.Markdown("classic")
    inner.append(markdown)
    assert compiled.fallbacks[-1] is markdown
    (op,) = compiled.patch["ops"]
    assert op["subtree"]["children"]["objects"][-1] == {
        "id": str(id(markdown)), "kind": "fallback", "slot": len(compiled.fallbacks) - 1,
        "sizing_mode": markdown.sizing_mode,
    }


def test_compiled_layout_change_recompiles_the_tree(tree):
    compiled, _, _, _, button = tree
    before = compiled.tree
    button.width = 300
    assert compiled.tree is not before
    assert compiled.tree["state"]["rev"] > before["state"]["rev"]


def test_compiled_structural_change_falls_back(tree):
    compiled, _, _, _, button = tree
    button.loading = True
    assert button in compiled.fallbacks
    button.loading = False
    assert button not in compiled.fallbacks


def test_compiled_client_update_is_not_echoed(tree):
    compiled, _, _, text, _ = tree
    compiled.get_root(Document())
    compiled._handle_msg({"type": "update", "id": str(id(text)), "name": "value", "value": "b", "root": "r", "seq": 1})
    assert text.value == "b"
    # Only the value_input that Python derived from the edit is sent back.
    assert compiled.patch["ops"] == [{"id": str(id(text)), "props": {"value_input": "b"}}]


def test_compiled_tree_is_json_serializable(tree):
    compiled, *_ = tree
    json.dumps(compiled.tree)


def test_compiled_page_is_the_compiled_root():
    button = Button(label="Run")
    compiled = Compiled(Page(main=[button], title="Title"))
    assert compiled.tree["root"]["kind"] == "Page"
    assert button not in compiled.fallbacks


def test_compiled_patches_in_one_hold_travel_together():
    first, second = Button(label="A"), Button(label="B")
    compiled = Compiled(Column(first, second))
    doc = Document()
    doc.add_root(compiled.get_root(doc))

    doc.hold()
    first.label = "A2"
    second.label = "B2"
    doc.unhold()

    patch = compiled.patch
    assert patch["ops"] == [{"id": str(id(second)), "props": {"label": "B2"}}]
    assert patch["earlier"] == [
        {"rev": patch["rev"] - 1, "ops": [{"id": str(id(first)), "props": {"label": "A2"}}]}
    ]

    first.label = "A3"
    assert "earlier" not in compiled.patch


def test_compiled_forwards_messages_to_nodes():
    button = Button(label="Run")
    compiled = Compiled(Column(button))
    sent = []
    compiled._send_msg = sent.append

    button.focus()

    assert sent == [{"type": "node_msg", "id": str(id(button)), "data": {"action": "focus"}}]


def test_compiled_fallback_root_sizes_the_model():
    compiled = Compiled(pn.Row(pn.Spacer(sizing_mode="stretch_width", height=50)))
    root = compiled.get_root(Document())
    assert root.sizing_mode == "stretch_width"


def test_compiled_substitutes_panel_layouts():
    button = Button(label="Run")
    layout = pn.Column(pn.Row(button, width=300), margin=7)
    compiled = Compiled(layout)

    root = compiled.tree["root"]
    assert root["kind"] == "Column"
    assert root["layout"]["margin"] == 7
    (row,) = root["children"]["objects"]
    assert row["kind"] == "Row"
    assert row["layout"]["width"] == 300
    assert [child["kind"] for child in row["children"]["objects"]] == ["Button"]
    assert compiled.fallbacks == []
    assert compiled.select(Button) == [button]


def test_compiled_substituted_layout_follows_the_original():
    row = pn.Row(Button(label="A"))
    compiled = Compiled(Column(row))
    added = Button(label="B")

    row.append(added)

    (op,) = compiled.patch["ops"]
    assert [child["kind"] for child in op["subtree"]["children"]["objects"]] == ["Button", "Button"]

    row.width = 250
    (node,) = compiled.tree["root"]["children"]["objects"]
    assert node["layout"]["width"] == 250


def test_compiled_keeps_panel_layouts_it_cannot_compile():
    layout = pn.Column(Button(label="Run"), scroll=True)
    compiled = Compiled(layout)

    assert compiled.tree["root"]["kind"] == "fallback"
    assert compiled.fallbacks == [layout]
