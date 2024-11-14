from __future__ import annotations

import param
from panel.widgets.select import (
    SingleSelectBase as _PnSingleSelectBase,
)
from panel.widgets.select import (
    _MultiSelectBase as _PnMultiSelectBase,
)

from ..base import COLORS
from .base import MaterialWidget


class MaterialSingleSelectBase(MaterialWidget, _PnSingleSelectBase):
    value = param.String(default=None, allow_None=True)

    __abstract = True


class MaterialMultiSelectBase(MaterialWidget, _PnMultiSelectBase):
    value = param.List(default=None, allow_None=True)

    __abstract = True


class AutocompleteInput(MaterialSingleSelectBase):
    """
    The `AutocompleteInput` widget allows selecting multiple values from a list of
    `options`.

    It falls into the broad category of multi-value, option-selection widgets
    that provide a compatible API and include the `MultiSelect`,
    `CrossSelector`, `CheckBoxGroup` and `CheckButtonGroup` widgets.

    The `MultiChoice` widget provides a much more compact UI than
    `MultiSelect`.

    :Example:

    >>> AutocompleteInput(
    ...     name='Study', options=['Biology', 'Chemistry', 'Physics'],
    ...     placeholder='Write your study here ...'
    ... )
    """

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm = "Autocomplete.jsx"

    _rename = {"name": "name"}


class Select(MaterialSingleSelectBase):
    """
    The `Select` widget allows selecting a value from a list or dictionary of
    `options` by selecting it from a dropdown menu or selection area.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the `RadioBoxGroup`,
    `AutocompleteInput` and `DiscreteSlider` widgets.

    :Example:

    >>> Select(name='Study', options=['Biology', 'Chemistry', 'Physics'])
    """

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm = "Select.jsx"

    _rename = {"name": "name"}


class RadioGroup(MaterialWidget):
    color = param.Selector(default="primary", objects=COLORS)

    orientation = param.Selector(
        default="horizontal",
        objects=["horizontal", "vertical"],
        doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""",
    )

    _esm = "RadioGroup.jsx"

    _rename = {"name": "name"}

    __abstract = True


class RadioBoxGroup(RadioGroup, MaterialSingleSelectBase):
    value = param.String(default=None, allow_None=True)

    _constants = {"exclusive": True}


class CheckBoxGroup(RadioGroup, MaterialMultiSelectBase):
    value = param.List(default=None, allow_None=True)

    _constants = {"exclusive": False}


class ButtonGroup(MaterialWidget):
    color = param.Selector(default="primary", objects=COLORS)

    disableElevation = param.Boolean(default=False)

    exclusive = param.Boolean(default=False)

    fullWidth = param.Boolean(default=False)

    orientation = param.Selector(
        default="horizontal",
        objects=["horizontal", "vertical"],
        doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""",
    )

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    variant = param.Selector(objects=["text", "outlined", "contained"], default="outlined")

    width = param.Integer(default=None, doc="""""")

    _esm = "ButtonGroup.jsx"

    _rename = {"name": "name"}

    __abstract = True


class RadioButtonGroup(ButtonGroup, MaterialSingleSelectBase):
    """
    The `RadioButtonGroup` widget allows selecting from a list or dictionary
    of values using a set of toggle buttons.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the `RadioBoxGroup`, `Select`,
    and `DiscreteSlider` widgets.

    :Example:

    >>> RadioButtonGroup(
    ...     name='Plotting library', options=['Matplotlib', 'Bokeh', 'Plotly'],
    ...     button_type='success'
    ... )
    """

    value = param.Parameter()

    _constants = {"exclusive": True}


class CheckButtonGroup(ButtonGroup, MaterialMultiSelectBase):
    _constants = {"exclusive": False}
