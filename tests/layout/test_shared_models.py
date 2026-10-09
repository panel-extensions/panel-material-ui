import pytest
from panel.layout import Column as PnColumn, Row as PnRow
from panel.viewable import Viewable
from panel.widgets import TextInput

from panel_material_ui.layout import Accordion, Feed, Tabs

refcounted = pytest.mark.skipif(
    not hasattr(Viewable, "_acquire_model"),
    reason="Panel version does not reference count shared models"
)


@pytest.mark.parametrize("layout", [Accordion, Feed, Tabs])
def test_shared_child_reuses_model(layout, document, comm):
    widget = TextInput(value="A")
    row = PnRow(widget)
    container = PnColumn(row, layout(widget))
    root = container.get_root(document, comm)
    ref = root.ref["id"]

    model = widget._models[ref][0]
    assert row._models[ref][0].children[0] is model

    widget.value = "B"
    assert model.value == "B"


@refcounted
@pytest.mark.parametrize("layout", [Accordion, Feed, Tabs])
def test_shared_child_survives_removal_from_other_parent(layout, document, comm):
    widget = TextInput(value="A")
    row = PnRow(widget)
    container = PnColumn(row, layout(widget))
    root = container.get_root(document, comm)
    ref = root.ref["id"]
    model = widget._models[ref][0]

    row.objects = []

    assert widget._models[ref][0] is model
    widget.value = "B"
    assert model.value == "B"


@refcounted
@pytest.mark.parametrize("layout", [Accordion, Feed, Tabs])
def test_shared_child_cleaned_up_once_released_by_all(layout, document, comm):
    widget = TextInput(value="A")
    row = PnRow(widget)
    mui = layout(widget)
    container = PnColumn(row, mui)
    root = container.get_root(document, comm)
    ref = root.ref["id"]

    row.objects = []
    mui.objects = []

    assert ref not in widget._models
