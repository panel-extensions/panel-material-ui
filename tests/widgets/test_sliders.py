import pytest
from panel.widgets import FloatSlider as ClassicFloatSlider
from panel.widgets import IntRangeSlider as ClassicIntRangeSlider
from panel.widgets import IntSlider as ClassicIntSlider
from panel.widgets import RangeSlider as ClassicRangeSlider

from panel_material_ui import (
    DiscreteSlider,
    EditableRangeSlider,
    FloatSlider,
    IntRangeSlider,
    IntSlider,
    RangeSlider,
    Rating,
)


def test_numeric_slider_defaults_match_classic():
    """Migrating a slider without bounds should retain its numeric range."""
    assert (IntSlider().start, IntSlider().end) == (ClassicIntSlider().start, ClassicIntSlider().end)
    assert FloatSlider().end == ClassicFloatSlider().end
    assert RangeSlider().value == ClassicRangeSlider().value
    assert RangeSlider.param.step.default == ClassicRangeSlider.param.step.default
    assert IntRangeSlider().value == ClassicIntRangeSlider().value
    assert EditableRangeSlider().value == ClassicRangeSlider().value


@pytest.mark.parametrize(('options', 'formatter', 'expected'), [
    ([1000, 2000], None, ['1000', '2000']),
    ([1.234, 2.456], '%.1f', ['1.2', '2.5']),
    ({'one': 1, 'two': 2}, '%.1f', ['one', 'two']),
])
def test_discrete_slider_formatter(options, formatter, expected):
    """Formatting affects numeric labels but preserves the selected value."""
    kwargs = {} if formatter is None else {'formatter': formatter}
    slider = DiscreteSlider(options=options, **kwargs)
    assert slider._process_param_change({'options': options})['options'] == expected
    assert slider._process_property_change({'value': 1})['value'] == slider.values[1]
    slider.formatter = '%.2f'
    assert 'options' in slider._process_param_change({'formatter': slider.formatter})

def test_rating_initial_end():
    """Should not raise an exception when end is not set."""
    Rating(label='Max 10', end=10, value=7)
