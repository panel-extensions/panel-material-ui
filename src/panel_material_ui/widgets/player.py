from __future__ import annotations

import typing as t

import param
from panel.util import indexOf, isIn
from panel.widgets.player import (
    DiscretePlayer as _PnDiscretePlayer,
)
from panel.widgets.player import (
    Player as _PnPlayer,
)
from panel.widgets.player import (
    PlayerBase as _PnPlayerBase,
)

from ..base import COLORS, ColorType
from .base import MaterialWidget


class _PlayerBase(MaterialWidget, _PnPlayerBase):

    color: ColorType = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the slider and the active transport button.""")  # type: ignore[assignment]

    height = param.Integer(default=None, allow_None=True, doc="Height of the widget.")

    size: t.Literal["small", "medium", "large"] = param.Selector(
        default="small", objects=["small", "medium", "large"],
        doc="The size of the slider and the transport buttons."
    )  # type: ignore[assignment]

    variant: t.Literal["full", "minimal"] = param.Selector(
        default="full", objects=["full", "minimal"], doc="""
        The layout of the player. The 'full' variant stacks the label, the
        slider, the transport buttons and the loop controls. The 'minimal'
        variant collapses everything into a single row consisting of a
        play/pause toggle, the slider and (if `show_value`) the value.""")  # type: ignore[assignment]

    width = param.Integer(default=300, bounds=(0, None), allow_None=True, doc="Width of the widget.")

    _esm_base = "Player.jsx"
    _stylesheets: t.ClassVar[list[str]] = []

    __abstract = True


class Player(_PlayerBase, _PnPlayer):
    """
    The `Player` provides controls to play and skip through a number of
    frames defined by explicit start and end values. The speed at which
    the widget plays is defined by the `interval` (in milliseconds), but it
    is also possible to skip frames using the `step` parameter.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Player.html
    - https://panel.holoviz.org/reference/widgets/Player.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> Player(label='Frame', start=0, end=100, value=32, loop_policy='loop')
    """

    # The embed machinery emits 'cb_obj.value' against the widget model,
    # which does not resolve on a ReactComponent, whose value lives on the
    # nested data model. pn.io.embed therefore skips the Material player.
    _supports_embed: bool = False


class DiscretePlayer(_PlayerBase, _PnDiscretePlayer):
    """
    The `DiscretePlayer` provides controls to iterate through a list of
    discrete options. The speed at which the widget plays is defined by the
    `interval` (in milliseconds), but it is also possible to skip items
    using the `step` parameter.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/DiscretePlayer.html
    - https://panel.holoviz.org/reference/widgets/DiscretePlayer.html
    - https://mui.com/material-ui/react-slider/

    :Example:

    >>> DiscretePlayer(
    ...     label='Discrete Player',
    ...     options=[2, 4, 8, 16, 32, 64, 128], value=32,
    ...     loop_policy='loop'
    ... )
    """

    options = param.ClassSelector(default=[], class_=(dict, list), doc="""
        A list or dictionary of valid options.""")

    _constants = {"discrete": True}

    def _process_param_change(self, params):
        props = super()._process_param_change(params)
        # The classic implementation declares start/end as model properties
        # and derives them from the options; the JSX derives the bounds from
        # the length of the options instead.
        props.pop('start', None)
        props.pop('end', None)
        if 'options' in props and 'value' not in props:
            # Selecting the first option when the current value is not in the
            # new options happens as a side-effect of the super() call, so the
            # index has to be re-derived here.
            values = self.values
            props['value'] = indexOf(self.value, values) if isIn(self.value, values) else 0
        return props


__all__ = [
    "DiscretePlayer",
    "Player",
]
