import pytest
from bokeh.models import Spacer as BkSpacer

from panel_material_ui.layout import Accordion, Column, Tabs
from panel_material_ui.pane import Typography


@pytest.mark.parametrize("layout, active", [(Accordion, [0]), (Tabs, 0)])
def test_dynamic_layout_renders_inactive_headers(layout, active, document, comm):
    obj = layout(
        (Typography("Title 1"), Column("Content 1")),
        (Typography("Title 2"), Column("Content 2")),
        active=active,
        dynamic=True,
    )
    model = obj.get_root(document, comm)

    assert not any(isinstance(header, BkSpacer) for header in model.data._headers)
    assert [isinstance(o, BkSpacer) for o in model.data.objects] == [False, True]


@pytest.mark.parametrize("layout, active, switch", [(Accordion, [0], [1]), (Tabs, 0, 1)])
def test_dynamic_layout_switch_reuses_placeholders(layout, active, switch, document, comm):
    obj = layout(*((f"Title {i}", Column(f"Content {i}")) for i in range(4)), active=active, dynamic=True)
    model = obj.get_root(document, comm)
    before = list(model.data.objects)

    events = []
    model.data.on_change('objects', lambda attr, old, new: events.append(new))
    model.data.on_change('_headers', lambda attr, old, new: events.append(new))
    obj.active = switch

    assert len(events) == 1
    after = model.data.objects
    assert isinstance(after[0], BkSpacer) and not isinstance(after[1], BkSpacer)
    assert after[2] is before[2]
    assert after[3] is before[3]


@pytest.mark.parametrize("layout", [Accordion, Tabs])
def test_dynamic_layout_cleanup_placeholders(layout, document, comm):
    obj = layout(("A", Column("a")), ("B", Column("b")), dynamic=True)
    model = obj.get_root(document, comm)
    assert model.ref['id'] in obj._placeholders
    obj._cleanup(model)
    assert model.ref['id'] not in obj._placeholders


def test_tabs_pop_shifts_active():
    tabs = Tabs(*((f"T{i}", f"c{i}") for i in range(5)), active=3)
    tabs.pop(1)
    assert tabs.active == 2
    tabs.pop(2)
    assert tabs.active == 2
    assert tabs._names == ["T0", "T2", "T4"]
    tabs.pop()
    assert tabs.active == 1
    tabs.remove(tabs[0])
    assert tabs.active == 0
    tabs.clear()
    assert tabs.active == 0


def test_tabs_objects_assignment_clamps_active():
    tabs = Tabs(*((f"T{i}", f"c{i}") for i in range(5)), active=4)
    tabs.objects = tabs.objects[:2]
    assert tabs.active == 1


@pytest.mark.parametrize("dynamic", [False, True])
def test_accordion_out_of_range_active_not_clamped_on_switch(dynamic):
    acc = Accordion(*((f"A{i}", f"c{i}") for i in range(3)), dynamic=dynamic)
    acc.active = [0, 5]
    assert acc.active == [0, 5]


def test_named_layout_objects_assignment_remaps_headers():
    header = Typography("Header")
    p1, p2 = Column("c1"), Column("c2")
    acc = Accordion((header, p1))
    acc.objects = [p2, p1]
    assert len(acc._headers) == 2
    assert acc._headers[0] is not header and acc._headers[1] is header
    assert acc._names[0] == p2.name and acc._names[1] is None


def test_tabs_pop_shifts_disabled():
    tabs = Tabs(*((f"T{i}", f"c{i}") for i in range(4)), disabled=[1, 3])
    tabs.pop(1)
    assert tabs.disabled == [2]


def test_accordion_pop_shifts_active():
    acc = Accordion(*((f"A{i}", f"c{i}") for i in range(5)), active=[1, 3, 4])
    acc.pop(0)
    assert acc.active == [0, 2, 3]
    acc.pop(2)
    assert acc.active == [0, 2]
    acc.pop()
    assert acc.active == [0]
    acc.clear()
    assert acc.active == []


def test_named_layout_mutation_syncs_names_once(document, comm):
    tabs = Tabs(("A", "a"), ("B", "b"))
    model = tabs.get_root(document, comm)
    events = []
    for prop in ('objects', '_names', '_headers'):
        model.data.on_change(prop, lambda attr, old, new: events.append(attr))
    tabs.append(("C", "c"))
    assert model.data._names == ["A", "B", "C"]
    assert len(model.data.objects) == 3
    assert sorted(events) == ['_headers', '_names', 'objects']


def test_tabs_close_msg_pops_duplicate_by_index(document, comm):
    shared = Column("shared")
    tabs = Tabs(("A", shared), ("B", "b"), ("C", shared), closable=True)
    model = tabs.get_root(document, comm)
    tabs._handle_msg({'type': 'close', 'id': model.data.objects[2].id, 'index': 2})
    assert tabs._names == ["A", "B"]
