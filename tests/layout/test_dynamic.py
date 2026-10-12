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
