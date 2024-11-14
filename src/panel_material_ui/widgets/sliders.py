import param
from panel.util import edit_readonly
from param.parameterized import resolve_value

from ..base import COLORS
from .base import MaterialWidget


class _ContinuousSlider(MaterialWidget):
    color = param.Selector(objects=COLORS, default="primary")

    start = param.Number(default=0)

    end = param.Number(default=100)

    step = param.Number(default=1)

    orientation = param.Selector(objects=["horizontal", "vertical"], default="horizontal")

    tooltips = param.Boolean(default=True)

    track = param.Selector(objects=["normal", "inverted", False], default="normal")

    value = param.Number(default=0)

    _esm = "Slider.jsx"

    __abstract = True


class IntSlider(_ContinuousSlider):
    """
    The IntSlider widget allows selecting an integer value within a
    set of bounds using a slider.

    Reference: https://panel.holoviz.org/reference/widgets/IntSlider.html

    :Example:

    >>> IntSlider(value=5, start=0, end=10, step=1, name="Integer Value")
    """

    end = param.Integer(default=1)

    start = param.Integer(default=1)

    step = param.Integer(default=1)


class FloatSlider(_ContinuousSlider):
    """
    The FloatSlider widget allows selecting a floating-point value
    within a set of bounds using a slider.

    :Example:

    >>> FloatSlider(value=0.5, start=0.0, end=1.0, step=0.1, name="Float value")
    """

    step = param.Number(default=0.1, doc="The step size.")


class _RangeSliderBase(_ContinuousSlider):
    value = param.Range(default=(0, 100))

    value_start = param.Parameter(readonly=True, doc="""The lower value of the selected range.""")

    value_end = param.Parameter(readonly=True, doc="""The upper value of the selected range.""")

    __abstract = True

    def __init__(self, **params):
        if "value" not in params:
            params["value"] = (params.get("start", self.start), params.get("end", self.end))
        if params["value"] is not None:
            v1, v2 = params["value"]
            params["value_start"], params["value_end"] = resolve_value(v1), resolve_value(v2)
        with edit_readonly(self):
            super().__init__(**params)

    @param.depends("value", watch=True)
    def _sync_values(self):
        vs, ve = self.value
        with edit_readonly(self):
            self.param.update(value_start=vs, value_end=ve)


class RangeSlider(_RangeSliderBase):
    """
    The RangeSlider widget allows selecting a floating-point range
    using a slider with two handles.

    :Example:

    >>> RangeSlider(
    ...     value=(1.0, 1.5), start=0.0, end=2.0, step=0.25, name="A tuple of floats"
    ... )
    """


class IntRangeSlider(_RangeSliderBase):
    """
    The IntRangeSlider widget allows selecting an integer range using
    a slider with two handles.

    :Example:

    >>> IntRangeSlider(
    ...     value=(2, 4), start=0, end=10, step=2, name="A tuple of integers"
    ... )
    """

    start = param.Integer(default=0)

    end = param.Integer(default=100)

    step = param.Integer(default=1)

    value_start = param.Integer(default=0, readonly=True, doc="""The lower value of the selected range.""")

    value_end = param.Integer(default=100, readonly=True, doc="""The upper value of the selected range.""")


class Rating(MaterialWidget):
    only_selected = param.Boolean(default=False, doc="Whether to highlight only the select value")

    precision = param.Number(default=1, doc="Use the precision prop to define the minimum increment value change allowed.")

    size = param.Selector(default="medium", objects=["small", "medium", "large"])

    start = param.Number(default=0)

    end = param.Number(default=100)

    value = param.Number(default=0, bounds=(0, 5))

    _esm = "Rating.jsx"
