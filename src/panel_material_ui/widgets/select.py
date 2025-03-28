from __future__ import annotations

import param
from panel.util import edit_readonly, isIn
from panel.widgets.base import Widget
from panel.widgets.select import NestedSelect as _PnNestedSelect
from panel.widgets.select import Select as _PnSelect
from panel.widgets.select import SingleSelectBase as _PnSingleSelectBase
from panel.widgets.select import _MultiSelectBase as _PnMultiSelectBase

from ..base import COLORS
from .base import MaterialWidget


class MaterialSingleSelectBase(MaterialWidget, _PnSingleSelectBase):
    """
    Base class for Material UI single-select widgets.

    This class combines Material UI styling with Panel's single select functionality.
    It provides the foundation for widgets that allow selecting a single value from
    a list of options, such as dropdown selects and autocomplete inputs.

    This is an abstract base class and should not be used directly.
    """

    value = param.Parameter(default=None, allow_None=True)

    _allows_values = False

    __abstract = True


class MaterialMultiSelectBase(MaterialWidget, _PnMultiSelectBase):
    """
    Base class for Material UI multi-select widgets.

    This class combines Material UI styling with Panel's multi-select functionality.
    It provides the foundation for widgets that allow selecting multiple values from
    a list of options, such as multi-select dropdowns and autocomplete inputs.

    This is an abstract base class and should not be used directly.
    """

    value = param.List(default=[], allow_None=True)

    _rename = {"name": "name"}

    _allows_values = False

    __abstract = True


class AutocompleteInput(MaterialSingleSelectBase):
    """
    The `AutocompleteInput` widget allows searching and selecting a single value
    from a list of `options`.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `Select`,
    `RadioBoxGroup` and `RadioButtonGroup` widgets.

    References:
    - https://panel.holoviz.org/reference/widgets/AutocompleteInput.html
    - https://mui.com/material-ui/react-autocomplete/

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

    placeholder = param.String(
        default="",
        doc="""
        Placeholder for empty input field.""",
    )

    restrict = param.Boolean(default=True, doc="""
        Set to False in order to allow users to enter text that is not
        present in the list of completion strings.""")

    search_strategy = param.Selector(default='starts_with',
        objects=['starts_with', 'includes'], doc="""
        Define how to search the list of completion strings. The default option
        `"starts_with"` means that the user's text must match the start of a
        completion string. Using `"includes"` means that the user's text can
        match any substring of a completion string.""")

    value_input = param.Parameter(
        default="",
        readonly=True,
        doc="""
        Initial or entered text value updated on every key press.""",
    )

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

    @param.depends('value', watch=True, on_init=True)
    def _sync_value_input(self):
        with edit_readonly(self):
            self.value_input = self.value


class Select(MaterialSingleSelectBase, _PnSelect):
    """
    The `Select` widget allows selecting a value from a list.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `AutocompleteInput`,
    `RadioBoxGroup` and `RadioButtonGroup` widgets.

    References:
    - https://panel.holoviz.org/reference/widgets/Select.html
    - https://mui.com/material-ui/react-select/

    :Example:

    >>> Select(label='Study', options=['Biology', 'Chemistry', 'Physics'])
    """

    color = param.Selector(objects=COLORS, default="primary")

    disabled_options = param.List(default=[], nested_refs=True, doc="""
        Optional list of ``options`` that are disabled, i.e. unusable and
        un-clickable. If ``options`` is a dictionary the list items have to
        correspond to the values in the options dictionary..""")

    groups = param.Dict(default=None, nested_refs=True, doc="""
        Dictionary whose keys are used to visually group the options
        and whose values are either a list or a dictionary of options
        to select from. Mutually exclusive with ``options``  and valid only
        if ``size`` is 1.""")

    size = param.Integer(default=1, bounds=(1, None), doc="""
        Declares how many options are displayed at the same time.
        If set to 1 displays options as dropdown otherwise displays
        scrollable area.""")

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm_base = "Select.jsx"
    _rename = {"name": "name", "groups": None}


class RadioGroup(MaterialWidget):
    """
    Base class for Material UI radio groups.

    This class combines Material UI styling with Panel's radio group functionality.
    It provides the foundation for widgets that allow selecting a single value from
    a list of options, such as radio buttons and checkboxes.
    """

    color = param.Selector(default="primary", objects=COLORS)

    inline = param.Boolean(default=False, doc="""
        Whether the items be arrange vertically (``False``) or
        horizontally in-line (``True``).""")

    width = param.Integer(default=None)

    _esm_base = "RadioGroup.jsx"

    _rename = {"name": "name"}

    __abstract = True


class RadioBoxGroup(RadioGroup, MaterialSingleSelectBase):
    """
    The `RadioBoxGroup` widget allows selecting a value from a list of options.

    It falls into the broad category of single-value, option-selection widgets
    that provide a compatible API and include the  `AutocompleteInput`,
    `Select` and `RadioButtonGroup` widgets.

    References:
    - https://panel.holoviz.org/reference/widgets/RadioBoxGroup.html
    - https://mui.com/material-ui/react-radio-button/

    :Example:

    >>> RadioBoxGroup(
    ...     label='Study', options=['Biology', 'Chemistry', 'Physics'],
    ... )
    """

    orientation = param.Selector(default="horizontal", objects=["horizontal", "vertical"], doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""")

    value = param.String(default=None, allow_None=True)

    _constants = {"exclusive": True}


class CheckBoxGroup(RadioGroup, MaterialMultiSelectBase):
    """
    The `CheckBoxGroup` widget allows selecting between a list of options by
    ticking the corresponding checkboxes.

    It falls into the broad category of multi-option selection widgets that
    provide a compatible API that also include the `CheckButtonGroup` widget.

    References:
    - https://panel.holoviz.org/reference/widgets/CheckBoxGroup.html
    - https://mui.com/material-ui/react-radio-button/

    :Example:

    >>> CheckBoxGroup(
    ...     name='Fruits', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'],
    ... )
    """

    orientation = param.Selector(
        default="horizontal",
        objects=["horizontal", "vertical"],
        doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""",
    )

    value = param.List(default=None, allow_None=True)

    _constants = {"exclusive": False}


class ButtonGroup(MaterialWidget):
    """
    Base class for Material UI button groups.

    This class combines Material UI styling with Panel's button group functionality.
    It provides the foundation for widgets that allow selecting a single or multiple
    values from a list of options, such as toggle buttons and checkboxes.

    This is an abstract base class and should not be used directly.
    """

    button_style = param.Selector(objects=["contained", "outlined", "text"], default="contained")

    button_type = param.Selector(objects=COLORS+["standard"], default="standard")

    description_delay = param.Integer(default=5000, doc="""
        Delay (in milliseconds) to display the tooltip after the cursor has
        hovered over the Button, default is 500ms.""")

    exclusive = param.Boolean(default=False)

    orientation = param.Selector(
        default="horizontal",
        objects=["horizontal", "vertical"],
        doc="""
        Button group orientation, either 'horizontal' (default) or 'vertical'.""",
    )

    size = param.Selector(objects=["small", "medium", "large"], default="medium")

    width = param.Integer(default=None)

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

    References:
    - https://panel.holoviz.org/reference/widgets/RadioButtonGroup.html
    - https://mui.com/material-ui/react-toggle-button/

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

    References:
    - https://panel.holoviz.org/reference/widgets/CheckButtonGroup.html
    - https://mui.com/material-ui/react-toggle-button/

    :Example:

    >>> CheckButtonGroup(
    ...     name='Regression Models', value=['Lasso', 'Ridge'],
    ...     options=['Lasso', 'Linear', 'Ridge', 'Polynomial']
    ... )

    """
    _constants = {"exclusive": False}


class MultiSelect(MaterialMultiSelectBase):
    """
    The `MultiSelect` widget allows selecting multiple values from a list of
    `options`.

    It falls into the broad category of multi-value, option-selection widgets
    that provide a compatible API and include the `MultiSelect`,
    `CrossSelector`, `CheckBoxGroup` and `CheckButtonGroup` widgets.

    References:
    - https://panel.holoviz.org/reference/widgets/MultiSelect.html
    - https://mui.com/material-ui/react-select/#multiple-select
    """

    color = param.Selector(objects=COLORS, default="primary")

    max_items = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum number of options that can be selected.""")

    size = param.Integer(default=None, doc="""
        The number of options to display at once (not currently supported).""")

    value = param.List(default=[], allow_None=True)

    variant = param.Selector(objects=["filled", "outlined", "standard"], default="outlined")

    _esm_base = "MultiSelect.jsx"


class MultiChoice(MultiSelect):
    """
    The `MultiChoice` widget allows selecting multiple values from a list of
    `options`.

    It falls into the broad category of multi-value, option-selection widgets
    that provide a compatible API and include the `MultiSelect`,
    `CrossSelector`, `CheckBoxGroup` and `CheckButtonGroup` widgets.

    The `MultiChoice` widget provides a much more compact UI than
    `MultiSelect`.

    References:
    - https://panel.holoviz.org/reference/widgets/MultiChoice.html
    - https://mui.com/material-ui/react-select/#multiple-select

    :Example:

    >>> MultiChoice(
    ...     name='Favourites', value=['Panel', 'hvPlot'],
    ...     options=['Panel', 'hvPlot', 'HoloViews', 'GeoViews', 'Datashader', 'Param', 'Colorcet'],
    ...     max_items=2
    ... )
    """

    delete_button = param.Boolean(default=True, doc="""
        Whether to display a button to delete a selected option.""")

    option_limit = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum number of options to display at once.""")

    search_option_limit = param.Integer(default=None, bounds=(1, None), doc="""
        Maximum number of options to display at once if search string is entered.""")

    placeholder = param.String(default='', doc="""
        String displayed when no selection has been made.""")

    solid = param.Boolean(default=True, doc="""
       π Whether to display widget with solid or light style.""")

    _rename = {"name": None}

    _esm_base = "MultiChoice.jsx"


class NestedSelect(_PnNestedSelect):
    """
    The `NestedSelect` widget is composed of multiple widgets, where subsequent select options
    depend on the parent's value.

    Reference: https://panel.holoviz.org/reference/widgets/NestedSelect.html

    :Example:

    >>> NestedSelect(
    ...     options={
    ...         "gfs": {"tmp": [1000, 500], "pcp": [1000]},
    ...         "name": {"tmp": [1000, 925, 850, 700, 500], "pcp": [1000]},
    ...     },
    ...     levels=["model", "var", "level"],
    ... )
    """

    def _extract_level_metadata(self, i):
        """
        Extract the widget type and keyword arguments from the level metadata.
        """
        level = self._levels[i]
        if isinstance(level, int):
            return Select, {}
        elif isinstance(level, str):
            return Select, {"name": level}
        widget_type = level.get("type", Select)
        widget_kwargs = {k: v for k, v in level.items() if k != "type"}
        return widget_type, widget_kwargs

__all__ = [
    "AutocompleteInput",
    "Select",
    "RadioBoxGroup",
    "CheckBoxGroup",
    "RadioButtonGroup",
    "CheckButtonGroup",
    "MultiSelect",
    "MultiChoice",
    "NestedSelect"
]
