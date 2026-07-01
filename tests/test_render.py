from datetime import date, datetime

import param
import pytest

from bokeh.document import Document

from panel_material_ui.base import MaterialComponent


SKIP = {'NumberInput'}

KWARGS = {
    'DateRangeSlider': dict(
        start=date(2025, 1, 1), end=date(2025, 12, 31),
        value=(date(2025, 1, 1), date(2025, 6, 1))
    ),
    'DatetimeRangeSlider': dict(
        start=datetime(2025, 1, 1), end=datetime(2025, 12, 31),
        value=(datetime(2025, 1, 1), datetime(2025, 6, 1))
    ),
    'DiscreteSlider': dict(options=[1, 2, 3], value=1),
}


def get_components():
    descendants = param.concrete_descendents(MaterialComponent)
    return [
        (name, cls)
        for name, cls in sorted(descendants.items())
        if not name.startswith('_') and name not in SKIP
    ]


@pytest.mark.parametrize("name,cls", get_components(), ids=[c[0] for c in get_components()])
def test_component_renders(name, cls):
    kwargs = KWARGS.get(name, {})
    instance = cls(**kwargs)
    root = instance.get_root(Document())
    assert root is not None
