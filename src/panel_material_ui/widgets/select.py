from __future__ import annotations

import param
from panel.util import isIn
from panel.widgets.base import Widget
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
    The `AutocompleteInput` widget allows searching and selecting a single value
    from a list of `options`.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `Select`,
    `RadioBoxGroup` and `RadioButtonGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel AutocompleteInput widget [panel.widgets.AutocompleteInput](https://panel.holoviz.org/reference/widgets/AutocompleteInput.html):
    - Missing features: case_sensitive, min_characters, placeholder, restrict, search_strategy, value_input
    - Extra features: label, on_event, on_msg, theme, variant

    :Example:

    >>> AutocompleteInput(
    ...     label='Study', options=['Biology', 'Chemistry', 'Physics'],
    ... )
    """

    case_sensitive = param.Boolean(default=True, doc="""
        Enable or disable case sensitivity.""")

    min_characters = param.Integer(default=2, doc="""
        The number of characters a user must type before
        completions are presented.""")

    restrict = param.Boolean(default=True, doc="""
        Set to False in order to allow users to enter text that is not
        present in the list of completion strings.""")

    search_strategy = param.Selector(default='starts_with',
        objects=['starts_with', 'includes'], doc="""
        Define how to search the list of completion strings. The default option
        `"starts_with"` means that the user's text must match the start of a
        completion string. Using `"includes"` means that the user's text can
        match any substring of a completion string.""")

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _allows_none = True

    _esm_base = "Autocomplete.jsx"

    _rename = {"name": "name"}

    def _process_property_change(self, msg):
        if 'value' in msg and msg['value'] is None:
            return msg
        if not self.restrict and 'value' in msg:
            try:
                return super()._process_property_change(msg)
            except Exception:
                return Widget._process_property_change(self, msg)
        return super()._process_property_change(msg)

    def _process_param_change(self, msg):
        if 'value' in msg and not self.restrict and not isIn(msg['value'], self.values):
            with param.parameterized.discard_events(self):
                props = super()._process_param_change(msg)
                self.value = props['value'] = msg['value']
        else:
            props = super()._process_param_change(msg)
        return props


class Select(MaterialSingleSelectBase):
    """
    The `Select` widget allows selecting a value from a list.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `AutocompleteInput`,
    `RadioBoxGroup` and `RadioButtonGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel Select widget [panel.widgets.Select](https://panel.holoviz.org/reference/widgets/Select.html):
    - Missing features: disabled_options, groups, size
    - Extra features: label, on_event, on_msg, theme, variant

    :Example:

    >>> Select(label='Study', options=['Biology', 'Chemistry', 'Physics'])
    """

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm_base = "Select.jsx"

    _rename = {"name": "name"}


class RadioGroup(MaterialWidget):
    color = param.Selector(default="primary", objects=COLORS)

    orientation = param.Selector(
        default="horizontal",
        objects=["horizontal", "vertical"],
        doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""",
    )

    _esm_base = "RadioGroup.jsx"

    _rename = {"name": "name"}

    __abstract = True


class RadioBoxGroup(RadioGroup, MaterialSingleSelectBase):
    """
    The `RadioBoxGroup` widget allows selecting a value from a list of options.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `AutocompleteInput`,
    `Select` and `RadioButtonGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel RadioBoxGroup widget [panel.widgets.RadioBoxGroup](https://panel.holoviz.org/reference/widgets/RadioBoxGroup.html):
    - Missing features: inline
    - Extra features: color, description, label, on_event, on_msg, orientation, theme

    :Example:

    >>> RadioBoxGroup(
    ...     label='Study', options=['Biology', 'Chemistry', 'Physics'],
    ... )
    """

    value = param.String(default=None, allow_None=True)

    _constants = {"exclusive": True}


class CheckBoxGroup(RadioGroup, MaterialMultiSelectBase):
    """
    The `CheckBoxGroup` widget allows selecting between a list of options by
    ticking the corresponding checkboxes.

    It falls into the broad category of multi-option selection widgets that
    provide a compatible API that also include the `CheckButtonGroup` widget.

    Some missing and extra features (if any) when comparing with the corresponding
    panel CheckBoxGroup widget [panel.widgets.CheckBoxGroup](https://panel.holoviz.org/reference/widgets/CheckBoxGroup.html):
    - Missing features: inline
    - Extra features: color, description, label, on_event, on_msg, orientation, theme

    :Example:

    >>> CheckBoxGroup(
    ...     name='Fruits', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'],
    ... )
    """

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

    width = param.Integer(default=None, doc="""""")

    _esm_base = "ButtonGroup.jsx"

    _rename = {"name": "name"}

    __abstract = True


class RadioButtonGroup(ButtonGroup, MaterialSingleSelectBase):
    """
    The `RadioButtonGroup` widget allows selecting from a list or dictionary
    of values using a set of toggle buttons.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the `AutocompleteInput`, `Select`,
    and `RadioBoxGroup` widgets.

    Some missing and extra features (if any) when comparing with the corresponding
    panel RadioButtonGroup widget [panel.widgets.RadioButtonGroup](https://panel.holoviz.org/reference/widgets/RadioButtonGroup.html):
    - Missing features: button_style, button_type, description_delay
    - Extra features: color, disableElevation, exclusive, fullWidth, label, on_event, on_msg, size, theme, variant

    :Example:

    >>> RadioButtonGroup(
    ...     label='Plotting library', options=['Matplotlib', 'Bokeh', 'Plotly'],
    ... )
    """

    value = param.Parameter()

    _constants = {"exclusive": True}


class CheckButtonGroup(ButtonGroup, MaterialMultiSelectBase):
    """
    The `CheckButtonGroup` widget allows selecting from a list or dictionary
    of values using a set of toggle buttons.

    It falls into the broad category of multi-option selection widgets that
    provide a compatible API that also include the `CheckBoxGroup` widget.

    Some missing and extra features (if any) when comparing with the corresponding
    panel CheckButtonGroup widget [panel.widgets.CheckButtonGroup](https://panel.holoviz.org/reference/widgets/CheckButtonGroup.html):
    - Missing features: button_style, button_type, description_delay
    - Extra features: color, disableElevation, exclusive, fullWidth, label, on_event, on_msg, size, theme, variant

    :Example:

    >>> CheckButtonGroup(
    ...     name='Regression Models', value=['Lasso', 'Ridge'],
    ...     options=['Lasso', 'Linear', 'Ridge', 'Polynomial']
    ... )

    """
    _constants = {"exclusive": False}


class MultiChoice(MaterialMultiSelectBase):
    """
    The `MultiChoice` widget allows selecting multiple values from a list of
    `options`.

    It falls into the broad category of multi-value, option-selection widgets
    that provide a compatible API and include the `MultiSelect`,
    `CrossSelector`, `CheckBoxGroup` and `CheckButtonGroup` widgets.

    The `MultiChoice` widget provides a much more compact UI than
    `MultiSelect`.

    Reference: https://panel.holoviz.org/reference/widgets/MultiChoice.html

    :Example:

    >>> MultiChoice(
    ...     name='Favourites', value=['Panel', 'hvPlot'],
    ...     options=['Panel', 'hvPlot', 'HoloViews', 'GeoViews', 'Datashader', 'Param', 'Colorcet'],
    ...     max_items=2
    ... )
    """

    delete_button = param.Boolean(default=True, doc="""
        Whether to display a button to delete a selected option.""")

    max_items = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum number of options that can be selected.""")

    option_limit = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum number of options to display at once.""")

    search_option_limit = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum number of options to display at once if search string is entered.""")

    placeholder = param.String(default='', doc="""
        String displayed when no selection has been made.""")

    solid = param.Boolean(default=True, doc="""
        Whether to display widget with solid or light style.""")

    width = param.Integer(default=300, allow_None=True, doc="""
      Width of this component. If sizing_mode is set to stretch
      or scale mode this will merely be used as a suggestion.""")

    value = param.List(default=[])

    _rename = {"name": None}

    _esm_base = "MultiChoice.jsx"
