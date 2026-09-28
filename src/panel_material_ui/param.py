import panel.widgets as _classic_widgets
import param
from panel.param import Param
from panel.widgets import WidgetBase

from . import widgets as _widgets
from .theme import PANEL_DESIGN_HOOKS, MaterialDesign
from .widgets import (
    Button,
    Checkbox,
    ColorPicker,
    DatePicker,
    DatetimeInput,
    DictInput,
    FileInput,
    FloatInput,
    FloatSlider,
    IntInput,
    IntSlider,
    ListInput,
    LiteralInput,
    MultiSelect,
    RangeSlider,
    Select,
    TextInput,
    TupleInput,
)


def SingleFileSelector(pobj: param.Parameter) -> type[WidgetBase]:
    """
    Determines whether to use a TextInput or Select widget for FileSelector
    """
    if pobj.path:
        return Select
    else:
        return TextInput


def LiteralInputTyped(pobj: param.Parameter) -> type[WidgetBase]:
    if isinstance(pobj, (param.Tuple, param.Range)):
        return TupleInput
    elif isinstance(pobj, param.Number):
        return type('NumberInput', (LiteralInput,), {'type': (int, float)})
    elif isinstance(pobj, param.Dict):
        return DictInput
    elif isinstance(pobj, param.List):
        return ListInput
    return LiteralInput


def _tuple_widget(pobj: param.Parameter) -> type[WidgetBase] | None:
    if isinstance(pobj, param.Range) and all(bound is not None for bound in pobj.get_soft_bounds()):
        return None
    return TupleInput


def _material_equivalents() -> dict[type, type]:
    """
    Maps each classic widget to the Material widget of the same name.
    """
    mapping = {}
    for name in dir(_widgets):
        material = getattr(_widgets, name)
        classic = getattr(_classic_widgets, name, None)
        if (
            isinstance(material, type) and issubclass(material, WidgetBase)
            and material.__module__.startswith('panel_material_ui')
            and isinstance(classic, type) and material is not classic
        ):
            mapping[classic] = material
    return mapping


if PANEL_DESIGN_HOOKS:
    MaterialDesign.component_mapping = _material_equivalents()
    # The classic LiteralInputTyped builds untyped LiteralInput subclasses,
    # which the component_mapping cannot match.
    MaterialDesign.widget_mapping = {
        param.Dict: DictInput,
        param.List: ListInput,
        param.Tuple: _tuple_widget,
    }
else:
    Param.mapping.update({
        param.Action:            Button,
        param.Boolean:           Checkbox,
        param.Bytes:             FileInput,
        param.CalendarDate:      DatePicker,
        param.Color:             ColorPicker,
        param.Date:              DatetimeInput,
        param.Dict:              LiteralInputTyped,
        param.Event:             Button,
        param.FileSelector:      SingleFileSelector,
        param.Filename:          TextInput,
        param.Foldername:        TextInput,
        param.Integer:           IntSlider,
        param.List:              LiteralInputTyped,
        param.ListSelector:      MultiSelect,
        param.Number:            FloatSlider,
        param.ObjectSelector:    Select,
        param.Parameter:         LiteralInputTyped,
        param.Range:             RangeSlider,
        param.Selector:          Select,
        param.String:            TextInput,
    })

    Param.input_widgets.update({
        float: FloatInput,
        int: IntInput,
        "literal": LiteralInputTyped,
    })
