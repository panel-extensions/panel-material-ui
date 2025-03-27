import param

from .base import MaterialWidget

class SelectSearch(MaterialWidget):
    options = param.List(default=[], doc="List of possible values to be selected")
    options_labels = param.List(
        default=None, allow_None=True, doc="Labels for each option"
    )
    bookmarks = param.List(default=[], doc="List of bookmarked options")
    title = param.String(
        default="Select an option", doc="Title displayed in the input label"
    )
    placeholder = param.String(
        default="Select an option", doc="Placeholder text when no option is selected"
    )

    width = param.Integer(default=300)
    dropdown_height = param.Integer(default=300)
    dropdown_open = param.Boolean(default=False, doc="Whether the dropdown is open")

    filter_str = param.String(default="")
    value = param.Parameter(default=None, allow_None=True, doc="The selected value")

    _esm_base = "SelectSearch.jsx"

    def __init__(self, **params):
        super().__init__(**{k: v for (k, v) in params.items() if v is not None})

    @classmethod
    def from_param(cls, parameter: param.Parameter, **params):

        result = SelectSearch(
            title=params.get("title", parameter.name),
            options=parameter.objects,
            options_labels=params.get("options_labels", None),
            value=getattr(parameter.owner, parameter.name),
            placeholder=params.get("placeholder", "Select an option"),
            width=params.get("width", 300),
            dropdown_height=params.get("dropdown_height", None),
            bookmarks=params.get("bookmarks", []),
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

    