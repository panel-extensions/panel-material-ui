from __future__ import annotations

import datetime as dt

import param
from bokeh.models.formatters import NumeralTickFormatter, TickFormatter
from panel.util import datetime_as_utctimestamp, edit_readonly, value_as_date, value_as_datetime
from panel.widgets.select import SingleSelectBase as _PnSingleSelectBase
from panel.widgets.slider import _SliderBase
from param.parameterized import resolve_value

from ..base import COLORS
from .base import MaterialWidget


class _ContinuousSlider(MaterialWidget, _SliderBase):

    bar_color = param.Color(default=None, allow_None=True, doc="Color of the bar")

    color = param.Selector(objects=COLORS, default="primary")

    direction = param.Selector(default='ltr', objects=['ltr', 'rtl'], doc="""
        Whether the slider should go from left-to-right ('ltr') or
        right-to-left ('rtl').""")

    start = param.Number(default=0)

    end = param.Number(default=100)

    format = param.ClassSelector(default='0[.]00', class_=(str, TickFormatter,), doc="""
        A custom format string or Bokeh TickFormatter.""")

    marks = param.ClassSelector(class_=(bool, list), default=False, doc="""
        Marks indicate predetermined values to which the user can move the slider.
        If True the `options` are shown as marks. If a list, it should contain dicts with 'value'
        and an optional 'label' keys.""")

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    step = param.Number(default=1)

    tooltips = param.Selector(objects=[True, False, "auto"], default="auto", doc="""
        Whether the slider handle should display tooltips (if auto will render on hover).""")

    track = param.Selector(objects=["normal", "inverted", False], default="normal")

    value = param.Number(default=0)

    value_label = param.String(default=None)

    value_throttled = param.Number(default=0, constant=True)

    _esm_base = "Slider.jsx"
    _rename = {"name": "name"}

    __abstract = True

    def _process_param_change(self, params):
        if self.orientation == 'vertical' and ('width' in params or 'height' in params):
            params['width'] = self.height
            params['height'] = self.width
        return super()._process_param_change(params)


class IntSlider(_ContinuousSlider):
    """
    The IntSlider widget allows selecting an integer value within a
    set of bounds using a slider.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/IntSlider.html
    - https://panel.holoviz.org/reference/widgets/IntSlider.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> IntSlider(value=5, start=0, end=10, step=1, label="Integer Value")
    """

    end = param.Integer(default=1)

    format = param.ClassSelector(default='0,0', class_=(str, TickFormatter,), doc="""
        A custom format string or Bokeh TickFormatter.""")

    start = param.Integer(default=1)

    step = param.Integer(default=1, bounds=(1, None))

    value = param.Integer(default=0)

    value_throttled = param.Integer(default=0, constant=True)

    _constants = {"int": True}


class FloatSlider(_ContinuousSlider):
    """
    The FloatSlider widget allows selecting a floating-point value
    within a set of bounds using a slider.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/FloatSlider.html
    - https://panel.holoviz.org/reference/widgets/FloatSlider.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> FloatSlider(value=0.5, start=0.0, end=1.0, step=0.1, label="Float value")
    """

    step = param.Number(default=0.1, doc="The step size.")


class DateSlider(_ContinuousSlider):
    """
    The DateSlider widget allows selecting a value within a set of
    bounds using a slider.  Supports datetime.datetime, datetime.date
    and np.datetime64 values. The step size is fixed at 1 day.

    :References:

    - https://panel.holoviz.org/reference/widgets/DateSlider.html

    :Example:

    >>> import datetime as dt
    >>> DateSlider(
    ...     value=dt.datetime(2025, 1, 1),
    ...     start=dt.datetime(2025, 1, 1),
    ...     end=dt.datetime(2025, 1, 7),
    ...     name="A datetime value"
    ... )
    """

    as_datetime = param.Boolean(default=False, doc="""
        Whether to store the date as a datetime.""")

    end = param.Date(default=None, doc="""
        The upper bound.""")

    format = param.String(default=None, doc="""
        Datetime format used for parsing and formatting the date.""")

    start = param.Date(default=None, doc="""
        The lower bound.""")

    step = param.Integer(default=1, bounds=(1, None), doc="""
        The step parameter in days.""")

    value = param.Date(default=None, doc="""
        The selected date value of the slider. Updated when the slider
        handle is dragged. Supports datetime.datetime, datetime.date
        or np.datetime64 types.""")

    value_throttled = param.Date(default=None, constant=True, doc="""
        The value of the slider. Updated when the slider handle is released.""")

    _constants = {"date": True}
    _rename = {"as_datetime": None}
    _source_transforms = {
        "value": None, "value_throttled": None, "value_start": None,
        "value_end": None, "start": None, "end": None
    }

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

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/DatetimeSlider.html
    - https://panel.holoviz.org/reference/widgets/DatetimeSlider.html
    - https://mui.com/material-ui/react-slider/

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
        if 'format' in params and isinstance(params['format'], str):
            params['format'] = NumeralTickFormatter(format=params['format'])
        with edit_readonly(self):
            super().__init__(**params)

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        if 'value' in msg:
            msg['value'] = tuple(msg['value'])
        if 'value_throttled' in msg:
            msg['value_throttled'] = tuple(msg['value_throttled'])
        return msg

    @param.depends("value", watch=True)
    def _sync_values(self):
        vs, ve = self.value
        with edit_readonly(self):
            self.param.update(value_start=vs, value_end=ve)


class RangeSlider(_RangeSliderBase):
    """
    The RangeSlider widget allows selecting a floating-point range
    using a slider with two handles.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/RangeSlider.html
    - https://panel.holoviz.org/reference/widgets/RangeSlider.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> RangeSlider(
    ...     value=(1.0, 1.5), start=0.0, end=2.0, step=0.25, label="A tuple of floats"
    ... )
    """


class IntRangeSlider(_RangeSliderBase):
    """
    The IntRangeSlider widget allows selecting an integer range using
    a slider with two handles.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/IntRangeSlider.html
    - https://panel.holoviz.org/reference/widgets/IntRangeSlider.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> IntRangeSlider(
    ...     value=(2, 4), start=0, end=10, step=2, label="A tuple of integers"
    ... )
    """

    start = param.Integer(default=0)

    format = param.ClassSelector(default='0,0', class_=(str, TickFormatter,), doc="""
        A custom format string or Bokeh TickFormatter.""")

    end = param.Integer(default=100)

    step = param.Integer(default=1)

    value_start = param.Integer(default=0, readonly=True, doc="""The lower value of the selected range.""")

    value_end = param.Integer(default=100, readonly=True, doc="""The upper value of the selected range.""")

    _constants = {"int": True}


class DateRangeSlider(_RangeSliderBase):
    """
    The DateRangeSlider widget allows selecting a date range using a
    slider with two handles. Supports datetime.datetime, datetime.date
    and np.datetime64 ranges.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/DateRangeSlider.html
    - https://panel.holoviz.org/reference/widgets/DateRangeSlider.html
    - https://mui.com/material-ui/react-slider/

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

    _property_conversion = staticmethod(value_as_date)

    _rename = {'value_start': None, 'value_end': None}
    _source_transforms = {
        "value": None, "value_throttled": None, "value_start": None,
        "value_end": None, "start": None, "end": None
    }

    def _process_param_change(self, msg):
        msg = super()._process_param_change(msg)
        if msg.get('value', 'unchanged') is None:
            del msg['value']
        elif 'value' in msg:
            v1, v2 = msg['value']
            if isinstance(v1, dt.datetime):
                v1 = datetime_as_utctimestamp(v1)
            if isinstance(v2, dt.datetime):
                v2 = datetime_as_utctimestamp(v2)
            msg['value'] = (v1, v2)
        if msg.get('value_throttled', 'unchanged') is None:
            del msg['value_throttled']
        return msg

    def _process_property_change(self, msg):
        msg = super()._process_property_change(msg)
        if 'value' in msg:
            v1, v2 = msg['value']
            msg['value'] = (self._property_conversion(v1), self._property_conversion(v2))
        if 'value_throttled' in msg:
            v1, v2 = msg['value_throttled']
            msg['value_throttled'] = (self._property_conversion(v1), self._property_conversion(v2))
        return msg


class DatetimeRangeSlider(DateRangeSlider):

    """
    The DatetimeRangeSlider widget allows selecting a datetime range
    using a slider with two handles. Supports datetime.datetime and
    np.datetime64 ranges.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/DatetimeRangeSlider.html
    - https://panel.holoviz.org/reference/widgets/DatetimeRangeSlider.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> import datetime as dt
    >>> DatetimeRangeSlider(
    ...     value=(dt.datetime(2025, 1, 9), dt.datetime(2025, 1, 16)),
    ...     start=dt.datetime(2025, 1, 1),
    ...     end=dt.datetime(2025, 1, 31),
    ...     step=60*60,
    ...     label="A tuple of datetimes"
    ... )
    """

    step = param.Number(default=60, doc="""
        The step size in seconds. Default is 1 minute, i.e 60 seconds.""")

    _property_conversion = staticmethod(value_as_datetime)

    _constants = {"datetime": True}


class DiscreteSlider(IntSlider, _PnSingleSelectBase):
    """
    The DiscreteSlider widget allows selecting a discrete value using a slider.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/DiscreteSlider.html
    - https://panel.holoviz.org/reference/widgets/DiscreteSlider.html
    - https://mui.com/material-ui/react-slider/
    """

    options = param.ClassSelector(default=[], class_=(dict, list), doc="""
        A list or dictionary of valid options.""")

    value = param.Parameter(doc="""
        The selected value of the slider. Updated when the handle is
        dragged. Must be one of the options.""")

    value_throttled = param.Parameter(constant=True, doc="""
        The value of the slider. Updated when the handle is released.""")

    start = param.Integer(default=0, readonly=True)
    end = param.Integer(default=100, readonly=True)
    step = param.Integer(default=1, readonly=True)

    _allows_values = False
    _constants = {"discrete": True}

    @param.depends("options", watch=True)
    def _update_bounds(self):
        self.param.update(start=0, end=len(self.options)-1)

    def _process_param_change(self, msg):
        msg = super()._process_param_change(msg)
        if 'options' in msg:
            msg['options'] = self.labels
        if 'value' in msg:
            msg['value'] = self.labels.index(msg['value'])
        return msg

    def _process_property_change(self, msg):
        if 'value' in msg:
            msg['value'] = self.labels[msg['value']]
        msg = super()._process_property_change(msg)
        return msg


class Rating(MaterialWidget):
    """
    The Rating slider widget allows users to select a rating value of their own.

    :References:

    - https://mui.com/material-ui/react-rating/

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


class _EditableContinuousSliderBase(_ContinuousSlider):

    _constants = {"editable": True}


class EditableFloatSlider(_EditableContinuousSliderBase, FloatSlider):
    """
    The EditableFloatSlider widget allows selecting a
    numeric floating-point value within a set of bounds using a slider
    and for more precise control offers an editable number input box.

    :References:
    - https://panel-material-ui.holoviz.org/reference/widgets/EditableFloatSlider.html
    - https://panel.holoviz.org/reference/widgets/EditableFloatSlider.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> EditableFloatSlider(
    ...     value=1.0, start=0.0, end=2.0, step=0.25, label="A float value"
    ... )
    """

    fixed_start = param.Number(default=None, doc="""
        A fixed lower bound for the slider and input.""")

    fixed_end = param.Number(default=None, doc="""
        A fixed upper bound for the slider and input.""")


class EditableIntSlider(_EditableContinuousSliderBase, IntSlider):
    """
    The EditableIntSlider widget allows selecting an integer
    value within a set of bounds using a slider and for more precise
    control offers an editable integer input box.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/EditableIntSlider.html
    - https://panel.holoviz.org/reference/widgets/EditableIntSlider.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> EditableIntSlider(
    ...     value=2, start=0, end=5, step=1, label="An integer value"
    ... )
    """

    fixed_start = param.Integer(default=None, doc="""
        A fixed lower bound for the slider and input.""")

    fixed_end = param.Integer(default=None, doc="""
       A fixed upper bound for the slider and input.""")

    _constants = {"editable": True, "int": True}


class _EditableRangeSliderBase(_RangeSliderBase):

    value = param.Range(default=(0, 100))

    _constants = {"editable": True}


class EditableRangeSlider(_EditableRangeSliderBase, RangeSlider):
    """
    The EditableRangeSlider widget allows selecting a floating-point range
    using a slider with two handles and for more precise control offers an editable
    number input box.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/EditableFloatRangeSlider.html
    """

    fixed_start = param.Number(default=None, doc="""
        A fixed lower bound for the slider and input.""")

    fixed_end = param.Number(default=None, doc="""
        A fixed upper bound for the slider and input.""")


class EditableIntRangeSlider(_EditableRangeSliderBase, IntRangeSlider):
    """
    The EditableIntRangeSlider widget allows selecting an integer range using
    a slider with two handles and for more precise control offers an editable
    integer input box.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/EditableIntRangeSlider.html
    """

    fixed_start = param.Integer(default=None, doc="""
        A fixed lower bound for the slider and input.""")

    fixed_end = param.Integer(default=None, doc="""
        A fixed upper bound for the slider and input.""")

    _constants = {"editable": True, "int": True}


__all__ = [
    "DateSlider",
    "DatetimeSlider",
    "DateRangeSlider",
    "DatetimeRangeSlider",
    "DiscreteSlider",
    "EditableRangeSlider",
    "EditableFloatSlider",
    "EditableIntRangeSlider",
    "EditableIntSlider",
    "FloatSlider",
    "IntRangeSlider",
    "IntSlider",
    "RangeSlider",
    "Rating"
]
