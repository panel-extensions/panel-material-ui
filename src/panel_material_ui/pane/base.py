from __future__ import annotations

import typing as t

import param
from panel.pane import HoloViews, Markdown

from ..base import MaterialComponent
from ..widgets import DatetimeInput, DiscreteSlider, EditableFloatSlider, EditableIntSlider, FloatSlider, IntSlider, Select

HoloViews.default_widgets = dict(  # type: ignore[assignment]
    HoloViews.default_widgets,
    date=DatetimeInput,
    discrete=Select,
    discrete_numeric=DiscreteSlider,
    float=(FloatSlider, EditableFloatSlider),
    int=(IntSlider, EditableIntSlider)
)

class MaterialPaneBase(MaterialComponent):

    object = param.Parameter(doc="The object to be rendered by the pane.")

    _rerender_params: list[str] = []

    __abstract = True

    def __init__(self, object=None, **params):
        super().__init__(object=object, **params)


class Typography(MaterialPaneBase, Markdown):
    """
    The `Typography` component is used to display text with different styles and weights.

    :References:

    - https://mui.com/material-ui/react-typography/
    """

    color = param.String(
        default=None,
        doc="""
        Color of the text. Can be a Material UI theme color (e.g., 'primary', 'secondary',
        'error', 'warning', 'info', 'success') or any valid CSS color value."""
    )

    variant = param.String(
        default=None,
        doc="""
        Typography variant that defines the text styling. Common options include:
        - Headers: 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
        - Body text: 'body1', 'body2'
        - Other: 'subtitle1', 'subtitle2', 'caption', 'overline'"""
    )

    _esm_base = "Typography.jsx"
    _rename = {"object": "object"}

    @classmethod
    def applies(cls, obj: t.Any) -> float | bool | None:
        if hasattr(obj, '_repr_markdown_'):
            return 0.29
        elif isinstance(obj, str):
            return 0.09
        else:
            return False
