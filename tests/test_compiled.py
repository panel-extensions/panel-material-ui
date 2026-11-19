import gc
import json

import panel as pn
import param
import pytest
from bokeh.document import Document
from panel.custom import Children, JSComponent

from panel_material_ui import (
    Button,
    Column,
    Compiled,
    Page,
    Row,
    TextInput,
    Typography,
)


@pytest.fixture(autouse=True)
def collect_trees():
    yield
    # A tree releases its components when it is finalized, so a component
    # is only collected by the pass after the one that collects its tree.
    gc.collect()
    gc.collect()


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
    compiled, layout, *_ = tree
    before = compiled.tree
    layout.width = 300
    assert compiled.tree is not before
    assert compiled.tree["state"]["rev"] > before["state"]["rev"]


def test_compiled_layout_change_recompiles_the_closest_unaffected_ancestor(tree):
    compiled, _, inner, _, button = tree
    before = compiled.tree
    button.width = 300
    assert compiled.tree is before
    (op,) = compiled.patch["ops"]
    assert op["id"] == str(id(inner))
    assert op["subtree"]["children"]["objects"][-1]["layout"]["width"] == 300


def test_compiled_layout_change_below_a_page_recompiles_the_node():
    column = Column(Button(label="Run"))
    compiled = Compiled(Page(main=[column]))
    before = compiled.tree
    column.sizing_mode = "stretch_width"
    assert compiled.tree is before
    (op,) = compiled.patch["ops"]
    assert op["id"] == str(id(column))
    assert op["subtree"]["layout"]["sizing_mode"] == "stretch_width"


def test_compiled_patches_classes_and_styles(tree):
    compiled, _, _, _, button = tree
    button.param.update(css_classes=["wide"], styles={"color": "red"})
    (op,) = compiled.patch["ops"]
    assert op["id"] == str(id(button))
    assert "wide" in op["css_classes"]
    assert op["styles"] == {"color": "red"}
    assert "subtree" not in op


def test_compiled_structural_change_falls_back(tree):
    compiled, _, _, _, button = tree
    button.href = "https://panel.holoviz.org"
    assert button in compiled.fallbacks
    button.href = None
    assert button not in compiled.fallbacks


def test_compiled_description_compiles(tree):
    compiled, _, _, _, button = tree
    button.description = "Help"
    assert compiled.fallbacks == []
    assert compiled.patch["ops"] == [{"id": str(id(button)), "props": {"description": "Help"}}]


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
    layout = pn.Column(Button(label="Run"), view_latest=True)
    compiled = Compiled(layout)

    assert compiled.tree["root"]["kind"] == "fallback"
    assert compiled.fallbacks == [layout]


def test_compiled_scrolling_layout_compiles():
    compiled = Compiled(pn.Column(Button(label="Run"), scroll="y-auto", height=100))

    root = compiled.tree["root"]
    assert root["kind"] == "Column"
    assert root["css_classes"] == ["scrollable-vertical"]


def test_compiled_renders_function_panes_as_their_layout():
    button = Button(label="Run")
    text = TextInput(value="a")
    layout = Column(text, pn.bind(lambda value: Button(label=value), text), button)
    compiled = Compiled(layout)

    kinds = [child["kind"] for child in compiled.tree["root"]["children"]["objects"]]
    assert kinds == ["TextInput", "Column", "Button"]
    inner = compiled.tree["root"]["children"]["objects"][1]
    assert [(child["kind"], child["props"]["label"]) for child in inner["children"]["objects"]] == [("Button", "a")]
    assert compiled.fallbacks == []

    text.value = "b"

    inner = compiled.tree["root"]["children"]["objects"][1]
    assert [(child["kind"], child["props"]["label"]) for child in inner["children"]["objects"]] == [("Button", "b")]


def test_compiled_patches_loading():
    button = Button(label="Run")
    compiled = Compiled(Column(button))

    button.loading = True

    assert compiled.patch["ops"] == [{"id": str(id(button)), "props": {"loading": True}}]


class Shelf(JSComponent):

    label = param.String(default="shelf")
    objects = Children()

    _compilable = True
    _esm = """
    export function render({model, el}) {
      el.append(...model.get_child("objects"))
    }
    """


class Frame(pn.Column):
    """A Panel layout that only adds behavior in Python."""

    def __init__(self, *objects, **params):
        super().__init__(*objects, **params)
        self.note = "kept"


class Custom(pn.Column):

    _stylesheets = [":host { color: red; }"]


def test_compiled_renders_a_js_component_as_a_node():
    button = Button(label="Run")
    markdown = pn.pane.Markdown("classic")
    shelf = Shelf(objects=[button, markdown], label="top")
    compiled = Compiled(Column(shelf))

    (node,) = compiled.tree["root"]["children"]["objects"]
    assert node["kind"] == f"{Shelf.__module__}.Shelf"
    assert node["props"]["label"] == "top"
    assert [child["kind"] for child in node["children"]["objects"]] == ["Button", "fallback"]
    kind = compiled.tree["kinds"][node["kind"]]
    assert kind["esm"] is True
    assert kind["render_policy"] == "children"
    assert compiled.fallbacks == [markdown]


def test_compiled_ships_one_prototype_per_js_component():
    compiled = Compiled(Column(Shelf(), Shelf()))
    doc = Document()
    model = compiled.get_root(doc)

    (kind,) = model.data._prototypes
    prototype = model.data._prototypes[kind]
    assert prototype.class_name == "Shelf"
    assert prototype.esm == Shelf()._render_esm(True, server=False)


def test_compiled_ships_the_prototype_of_a_js_component_added_later():
    layout = Column(Button(label="Run"))
    compiled = Compiled(Column(layout))
    model = compiled.get_root(Document())
    assert model.data._prototypes == {}

    layout.append(Shelf())

    assert list(model.data._prototypes) == [f"{Shelf.__module__}.Shelf"]


def test_compiled_forwards_the_messages_of_a_js_component():
    shelf = Shelf()
    compiled = Compiled(Column(shelf))
    sent = []
    compiled._send_msg = sent.append

    shelf._send_msg({"text": "hello"})

    assert sent == [{"type": "node_msg", "id": str(id(shelf)), "data": {"text": "hello"}}]


def test_compiled_updates_a_js_component():
    shelf = Shelf()
    compiled = Compiled(Column(shelf))

    shelf.label = "renamed"
    assert compiled.patch["ops"] == [{"id": str(id(shelf)), "props": {"label": "renamed"}}]

    compiled.get_root(Document())
    compiled._handle_msg({"type": "update", "id": str(id(shelf)), "name": "label", "value": "typed", "root": "r", "seq": 1})
    assert shelf.label == "typed"


def test_compiled_js_component_that_is_not_opted_in_falls_back():
    class Plain(JSComponent):
        _esm = "export function render() {}"

    plain = Plain()
    compiled = Compiled(Column(plain))

    assert compiled.fallbacks == [plain]


def test_compiled_js_component_falls_back_when_the_client_cannot_render_it():
    shelf = Shelf()
    compiled = Compiled(Column(shelf))

    compiled._handle_msg({"type": "esm_unsupported", "id": str(id(shelf)), "reason": "view.render_children"})

    assert compiled.fallbacks == [shelf]


def test_compiled_substitutes_plain_subclasses_of_panel_layouts():
    button = Button(label="Run")
    frame = Frame(button, width=300)
    compiled = Compiled(Column(frame))

    (node,) = compiled.tree["root"]["children"]["objects"]
    assert node["kind"] == "Column"
    assert node["layout"]["width"] == 300
    assert compiled.fallbacks == []


def test_compiled_keeps_subclasses_of_panel_layouts_that_render_differently():
    custom = Custom(Button(label="Run"))
    compiled = Compiled(Column(custom))

    assert compiled.fallbacks == [custom]

    card = pn.Card(Button(label="Run"))
    assert Compiled(Column(card)).fallbacks == [card]
