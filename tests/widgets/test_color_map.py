import pytest

from panel_material_ui.widgets import ColorMap


def test_color_map_value_name_sync():
    options = {"A": ["#ff0", "#0ff"], "B": ["#00f", "#f00"]}
    color_map = ColorMap(options=options, value=options["B"])

    assert color_map.value_name == "B"
    color_map.value_name = "A"
    assert color_map.value == options["A"]


def test_color_map_serializes_names_and_items(document, comm):
    options = {"A": ["#ff0", "#0ff"], "B": ["#00f", "#f00"]}
    color_map = ColorMap(options=options, value_name="B")
    model = color_map.get_root(document, comm=comm)

    assert "items" not in model.properties()
    assert model.data.items == {"A": options["A"], "B": options["B"]}
    assert model.data.value == "B"
    assert color_map.value == options["B"]

def test_color_map_initial_model_contains_options_and_value(document, comm):
    options = {"Warm": ["#fff", "#f00"], "Cool": ["#fff", "#00f"]}
    model = ColorMap(options=options, value_name="Warm").get_root(document, comm=comm)

    assert "items" not in model.properties()
    assert model.data.items == options
    assert model.data.value == "Warm"



def test_color_map_processes_frontend_value_change():
    options = {"A": ["#ff0", "#0ff"], "B": ["#00f", "#f00"]}
    color_map = ColorMap(options=options, value_name="A")

    assert color_map._process_property_change({"value": "B"}) == {"value": options["B"]}
    assert color_map._process_property_change({"value": ""}) == {"value": None}
    assert color_map._process_param_change({"options": {}}) == {"items": {}}



def test_color_map_processes_frontend_value_name_change():
    options = {"A": ["#ff0", "#0ff"], "B": ["#00f", "#f00"]}
    color_map = ColorMap(options=options, value=options["A"])

    assert color_map._process_property_change({"value": "B"}) == {"value": options["B"]}
    assert color_map.value_name == "A"
    color_map.value = options["B"]
    assert color_map.value_name == "B"


def test_color_map_serializes_option_and_value_changes_together():
    options = {"A": ["#fff"], "B": ["#000"]}
    color_map = ColorMap(options={"old": ["#aaa"]})

    props = color_map._process_param_change({"options": options, "value": options["B"]})

    assert props == {"value": "B", "items": options}



def test_color_map_updates_nested_items_on_options_change(document, comm):
    color_map = ColorMap(options={"old": ["#aaa"]}, value_name="old")
    model = color_map.get_root(document, comm=comm)

    options = {"new": ["#fff", "#000"]}
    props = color_map._process_param_change({"options": options})
    assert "items" not in model.properties()
    assert props["items"] == options
    model.data.update(**props)
    assert model.data.items == options


def test_color_map_empty_options_and_value_change():
    color_map = ColorMap(options={})

    assert color_map._process_property_change({"value": ""}) == {"value": None}
    assert color_map._process_param_change({"options": {}}) == {"items": {}}



def test_color_map_processes_frontend_value_name_change():
    options = {"A": ["#ff0", "#0ff"], "B": ["#00f", "#f00"]}
    color_map = ColorMap(options=options, value=options["A"])

    assert color_map._process_property_change({"value": "B"}) == {"value": options["B"]}
    assert color_map.value_name == "A"
    color_map.value = options["B"]
    assert color_map.value_name == "B"


def test_color_map_matplotlib_is_optional(document, comm):
    pytest.importorskip("matplotlib")
    from matplotlib.cm import viridis

    color_map = ColorMap(options={"viridis": viridis}, value_name="viridis")
    model = color_map.get_root(document, comm=comm)

    assert list(model.data.items)[0] == "viridis"
    assert model.data.items["viridis"][0].startswith("rgba(")
