import param

from .base import MaterialWidget


class SelectPicker(MaterialWidget):

    # these params will be reflected in the UI
    title = param.String(default="")

    # a callback called everytime the value changes, to update the label
    # params: widget, number of selected values, number of options
    # returns: the new label
    label_callback: callable = None

    # updated everytime the value changes, using label_callback
    label = param.String(default="")

    options = param.List(doc="List of possible values to be selected", default=[])
    options_labels = param.List(
        doc="List of Labels to show for the option."
        "Must contain the same number of values than `options`."
        "If None, the values in `options` are used a labels. ",
        default=None,
        allow_None=True,
    )

    width = param.Integer(default=300)
    dropdown_height = param.Integer(default=300)

    defaults_to_all = param.Boolean(
        default=True,
        doc="If True, `value` will be set to all options if no checkbox is selected.",
    )

    # the values of these params are built by the UI
    filter_str = param.String(default="")
    value = param.List(doc="The actual list of selected values", default=[])

    _esm_base = "SelectPicker.jsx"

    def __init__(self, label_callback, **params):
        self.label_callback = label_callback
        super().__init__(**{k: v for (k, v) in params.items() if v is not None})
        self.update_label()

    @classmethod
    def from_param(cls, parameter: param.Parameter, **params):

        result = SelectPicker(
            title=params.get("title", parameter.name),
            options=parameter.objects,
            options_labels=params.get("options_labels", None),
            value=getattr(parameter.owner, parameter.name),
            defaults_to_all=params.get("defaults_to_all", True),
            dropdown_height=params.get("dropdown_height", None),
            label_callback=params.get("label_callback", None),
        )

        def update_picker(
            param_name,
            picker_param_name,
        ):
            if param_name is None:
                param_value = getattr(parameter.owner, parameter.name)
            else:
                param_value = getattr(parameter, param_name)
            setattr(result, picker_param_name, param_value)

        def update_parameter_value(_):
            if result.value == [] and result.defaults_to_all:
                setattr(parameter.owner, parameter.name, result.options)
            else:
                setattr(parameter.owner, parameter.name, result.value)

        parameter.owner.param.watch(
            lambda _: update_picker("objects", "options"),
            parameter.name,
            what="objects",
        )
        parameter.owner.param.watch(
            lambda _: update_picker(None, "value"),
            parameter.name,
        )
        result.param.watch(update_parameter_value, "value")

        return result

    @param.depends(
        "value",
        "options",
        watch=True,
    )
    def update_label(self):
        if self.label_callback:
            self.label = self.label_callback(self, len(self.value), len(self.options))


    
