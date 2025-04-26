import param
from panel.param import Param
from panel.widgets import WidgetBase

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


Param.mapping.update({
    param.Action:            Button,
    param.Boolean:           Checkbox,
    param.Bytes:             FileInput,
    param.CalendarDate:      DatePicker,
    param.Color:             ColorPicker,
    param.Date:              DatetimeInput,
    param.Dict:              LiteralInputTyped,
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
