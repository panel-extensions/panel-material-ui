import param
from bokeh.models.formatters import NumeralTickFormatter, TickFormatter
from panel.util import edit_readonly
from panel.widgets.slider import _SliderBase
from param.parameterized import resolve_value

from ..base import COLORS
from .base import MaterialWidget


class _ContinuousSlider(MaterialWidget, _SliderBase):

    bar_color = param.Color(default=None, doc="Color of the bar")

    color = param.Selector(objects=COLORS, default="primary")

    direction = param.Selector(default='ltr', objects=['ltr', 'rtl'], doc="""
        Whether the slider should go from left-to-right ('ltr') or
        right-to-left ('rtl').""")

    start = param.Number(default=0)

    end = param.Number(default=100)

    format = param.ClassSelector(class_=(str, TickFormatter,), doc="""
        A custom format string or Bokeh TickFormatter.""")

    step = param.Number(default=1)

    track = param.Selector(objects=["normal", "inverted", False], default="normal")

    value = param.Number(default=0)

    value_throttled = param.Number(default=0, constant=True)

    _esm_base = "Slider.jsx"

    _rename = {"name": "name"}

    __abstract = True

    def _process_param_change(self, params):
        if self.orientation == 'vertical' and ('width' in params or 'height' in params):
            params['width'] = self.height
            params['height'] = self.width
        if 'format' in params and isinstance(params['format'], str):
            params['format'] = NumeralTickFormatter(format=params['format'])
        return super()._process_param_change(params)


class IntSlider(_ContinuousSlider):
    """
    The IntSlider widget allows selecting an integer value within a
    set of bounds using a slider.

    :Example:

    >>> IntSlider(value=5, start=0, end=10, step=1, name="Integer Value")
    """

    end = param.Integer(default=1)

    start = param.Integer(default=1)

    step = param.Integer(default=1, readonly=True)

    value = param.Integer(default=0)

    value_throttled = param.Integer(default=0, constant=True)


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

    value_throttled = param.Range(default=(0, 100), readonly=True)

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
    """
    The Rating slider widget allows users to select a rating value of their own.

    :Example:

    >>> Rating(value=3, size="large", name="Rate the product")
    """

    end = param.Integer(default=5, bounds=(1, None), doc="The maximum value for the rating.")

    only_selected = param.Boolean(default=False, doc="Whether to highlight only the select value")

    size = param.Selector(default="medium", objects=["small", "medium", "large"])

    value = param.Number(default=0, allow_None=True, bounds=(0, 5))

    _esm_base = "Rating.jsx"

    @param.depends("end", watch=True, on_init=True)
    def _update_value_bounds(self):
        self.param.value.bounds = (0, self.end)

    def _process_property_change(self, msg):
        if 'value' in msg and msg['value'] is None:
            msg['value'] = 0
        return super()._process_property_change(msg)
