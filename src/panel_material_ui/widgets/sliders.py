from __future__ import annotations

import datetime as dt

import param
from bokeh.models.formatters import NumeralTickFormatter, TickFormatter
from panel.util import datetime_as_utctimestamp, edit_readonly, value_as_date, value_as_datetime
from panel.widgets.slider import DiscreteSlider as _PnDiscreteSlider
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

    ticks = param.List(default=[])

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

    Reference: https://panel.holoviz.org/reference/widgets/IntSlider.html

    :Example:

    >>> IntSlider(value=5, start=0, end=10, step=1, label="Integer Value")
    """

    end = param.Integer(default=1)

    start = param.Integer(default=1)

    step = param.Integer(default=1, bounds=(1, None))

    value = param.Integer(default=0)

    value_throttled = param.Integer(default=0, constant=True)


class FloatSlider(_ContinuousSlider):
    """
    The FloatSlider widget allows selecting a floating-point value
    within a set of bounds using a slider.

    Reference: https://panel.holoviz.org/reference/widgets/FloatSlider.html

    :Example:

    >>> FloatSlider(value=0.5, start=0.0, end=1.0, step=0.1, label="Float value")
    """

    step = param.Number(default=0.1, doc="The step size.")


class DateSlider(_ContinuousSlider):
    """
    The DateSlider widget allows selecting a value within a set of
    bounds using a slider.  Supports datetime.datetime, datetime.date
    and np.datetime64 values. The step size is fixed at 1 day.

    Reference: https://panel.holoviz.org/reference/widgets/DateSlider.html

    :Example:

    >>> import datetime as dt
    >>> DateSlider(
    ...     value=dt.datetime(2025, 1, 1),
    ...     start=dt.datetime(2025, 1, 1),
    ...     end=dt.datetime(2025, 1, 7),
    ...     name="A datetime value"
    ... )
    """

    value = param.Date(default=None, doc="""
        The selected date value of the slider. Updated when the slider
        handle is dragged. Supports datetime.datetime, datetime.date
        or np.datetime64 types.""")

    value_throttled = param.Date(default=None, constant=True, doc="""
        The value of the slider. Updated when the slider handle is released.""")

    start = param.Date(default=None, doc="""
        The lower bound.""")

    end = param.Date(default=None, doc="""
        The upper bound.""")

    as_datetime = param.Boolean(default=False, doc="""
        Whether to store the date as a datetime.""")

    step = param.Integer(default=1, bounds=(1, None), doc="""
        The step parameter in days.""")

    format = param.String(default=None, doc="""
        Datetime format used for parsing and formatting the date.""")

    _constants = {"date": True}

    def _process_param_change(self, msg):
        msg = super()._process_param_change(msg)
        if 'value' in msg:
            value = msg['value']
            if isinstance(value, dt.datetime):
                value = datetime_as_utctimestamp(value)
            msg['value'] = value
        return msg

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        transform = value_as_datetime if self.as_datetime else value_as_date
        if 'value' in msg:
            msg['value'] = transform(msg['value'])
        if 'value_throttled' in msg:
            msg['value_throttled'] = transform(msg['value_throttled'])
        return msg


class DatetimeSlider(DateSlider):
    """
    The DatetimeSlider widget allows selecting a value within a set of
    bounds using a slider. Supports datetime.date, datetime.datetime
    and np.datetime64 values. The step size is fixed at 1 minute.

    Reference: https://panel.holoviz.org/reference/widgets/DatetimeSlider.html

    :Example:

    >>> import datetime as dt
    >>> DatetimeSlider(
    ...     value=dt.datetime(2025, 1, 1),
    ...     start=dt.datetime(2025, 1, 1),
    ...     end=dt.datetime(2025, 1, 7),
    ...     name="A datetime value"
    ... )
    """

    as_datetime = param.Boolean(default=True, readonly=True, doc="""
        Whether to store the date as a datetime.""")

    step = param.Number(default=60, bounds=(1, None), doc="""
        The step size in seconds. Default is 1 minute, i.e 60 seconds.""")

    _property_conversion = staticmethod(value_as_datetime)

    _constants = {"datetime": True}


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

    Reference: https://panel.holoviz.org/reference/widgets/RangeSlider.html

    :Example:

    >>> RangeSlider(
    ...     value=(1.0, 1.5), start=0.0, end=2.0, step=0.25, label="A tuple of floats"
    ... )
    """


class IntRangeSlider(_RangeSliderBase):
    """
    The IntRangeSlider widget allows selecting an integer range using
    a slider with two handles.

    Reference: https://panel.holoviz.org/reference/widgets/IntRangeSlider.html

    :Example:

    >>> IntRangeSlider(
    ...     value=(2, 4), start=0, end=10, step=2, label="A tuple of integers"
    ... )
    """

    start = param.Integer(default=0)

    end = param.Integer(default=100)

    step = param.Integer(default=1)

    value_start = param.Integer(default=0, readonly=True, doc="""The lower value of the selected range.""")

    value_end = param.Integer(default=100, readonly=True, doc="""The upper value of the selected range.""")


class DateRangeSlider(_RangeSliderBase):
    """
    The DateRangeSlider widget allows selecting a date range using a
    slider with two handles. Supports datetime.datetime, datetime.date
    and np.datetime64 ranges.

    Reference: https://panel.holoviz.org/reference/widgets/DateRangeSlider.html

    :Example:

    >>> import datetime as dt
    >>> DateRangeSlider(
    ...     value=(dt.datetime(2025, 1, 9), dt.datetime(2025, 1, 16)),
    ...     start=dt.datetime(2025, 1, 1),
    ...     end=dt.datetime(2025, 1, 31),
    ...     step=2,
    ...     name="A tuple of datetimes"
    ... )
    """

    value = param.DateRange(default=None, allow_None=False, doc="""
        The selected range as a tuple of values. Updated when one of the handles is
        dragged. Supports datetime.datetime, datetime.date, and np.datetime64 ranges.""")

    value_start = param.Date(default=None, readonly=True, doc="""
        The lower value of the selected range.""")

    value_end = param.Date(default=None, readonly=True, doc="""
        The upper value of the selected range.""")

    value_throttled = param.DateRange(default=None, constant=True, nested_refs=True, doc="""
        The selected range as a tuple of values. Updated one of the handles is released. Supports
        datetime.datetime, datetime.date and np.datetime64 ranges""")

    start = param.Date(default=None, doc="""
        The lower bound.""")

    end = param.Date(default=None, doc="""
        The upper bound.""")

    step = param.Number(default=1, doc="""
        The step size in days. Default is 1 day.""")

    format = param.String(default=None, doc="""
        Datetime format used for parsing and formatting the date.""")

    _constants = {"date": True}


class DatetimeRangeSlider(DateRangeSlider):

    """
    The DatetimeRangeSlider widget allows selecting a datetime range
    using a slider with two handles. Supports datetime.datetime and
    np.datetime64 ranges.

    Reference: https://panel.holoviz.org/reference/widgets/DatetimeRangeSlider.html

    :Example:

    >>> import datetime as dt
    >>> DatetimeRangeSlider(
    ...     value=(dt.datetime(2025, 1, 9), dt.datetime(2025, 1, 16)),
    ...     start=dt.datetime(2025, 1, 1),
    ...     end=dt.datetime(2025, 1, 31),
    ...     step=60*60,
    ...     name="A tuple of datetimes"
    ... )
    """

    step = param.Number(default=60, doc="""
        The step size in seconds. Default is 1 minute, i.e 60 seconds.""")

    _property_conversion = staticmethod(value_as_datetime)

    _constants = {"datetime": True}


class DiscreteSlider(_PnDiscreteSlider):
    """
    The DiscreteSlider widget allows selecting a discrete value using a slider.

    Reference: https://panel.holoviz.org/reference/widgets/DiscreteSlider.html
    """

    value = param.Parameter(doc="""
        The selected value of the slider. Updated when the handle is
        dragged. Must be one of the options.""")

    value_throttled = param.Parameter(constant=True, doc="""
        The value of the slider. Updated when the handle is released.""")

    options = param.ClassSelector(default=[], class_=(dict, list), doc="""
        A list or dictionary of valid options.""")

    def _update_options(self, *events):
        values, labels = self.values, self.labels
        if not self.options and self.value is None:
            value = 0
            label = (f'{self.name}: ' if self.name else '') + '<b>-</b>'
        elif self.value not in values:
            value = 0
            self.value = values[0]
            label = labels[value]
        else:
            value = values.index(self.value)
            label = labels[value]
        disabled = True if len(values) in (0, 1) else self.disabled
        end = 1 if disabled else len(self.options)-1

        self._slider = IntSlider(
            start=0, end=end, value=value, tooltips=False,
            show_value=False, margin=(0, 5, 5, 5),
            _supports_embed=False, disabled=disabled,
            **{p: getattr(self, p) for p in self._slider_style_params if p != 'disabled'}
        )
        self._update_style()
        js_code = self._text_link.format(
            labels='['+', '.join([repr(lbl) for lbl in labels])+']'
        )
        self._jslink = self._slider.jslink(self._text, code={'value': js_code})
        self._slider.param.watch(self._sync_value, 'value')
        self._slider.param.watch(self._sync_value, 'value_throttled')
        self.param.watch(self._update_slider_params, self._slider_style_params)
        self._text.value = label
        self._composite[1] = self._slider



class Rating(MaterialWidget):
    """
    The Rating slider widget allows users to select a rating value of their own.

    Reference: https://mui.com/material-ui/react-rating/

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
