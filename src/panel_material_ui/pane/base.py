import param

from ..base import COLORS, MaterialComponent


class Avatar(MaterialComponent):
    alt_text = param.String(
        default=None,
        doc="""
        alt text to add to the image tag. The alt text is shown when a
        user cannot load or display the image.""",
    )

    color = param.Color()

    object = param.String(default="")

    size = param.Selector(objects=["small", "medium"], default="medium")

    variant = param.Selector(objects=["rounded", "square"], default="rounded")

    _esm_base = "Avatar.jsx"


class Chip(MaterialComponent):
    color = param.Selector(objects=COLORS, default="primary")

    icon = param.String(
        default=None,
        doc="""
        The name of the icon to display.""",
    )

    object = param.String(default="")

    size = param.Selector(objects=["small", "medium"], default="medium")

    variant = param.Selector(objects=["filled", "outlined"], default="filled")

    _esm_base = "Chip.jsx"

    def _handle_click(self, event):
        pass


class Skeleton(MaterialComponent):

    variant = param.Selector(objects=["circular", "rectangular", "rounded"], default="rounded")

    height = param.Integer(default=0)

    width = param.Integer(default=0)

    _esm_base = "Skeleton.jsx"


class Breadcrumbs(MaterialComponent):

    items = param.List(default=[], doc=(
        "List of breadcrumb items. Each item may be a string or an object with keys: "
        "'label' (required) and 'href' (optional)."
    ))

    separator = param.String(default=None, doc="The separator displayed between breadcrumb items.")

    _esm_base = "Breadcrumbs.jsx"


class List(MaterialComponent):

    items = param.List(default=[], doc=(
        "List of items to display. Each item may be a string or an object with properties: "
        "'label' (required), 'icon' (optional), 'avatar' (optional), and 'secondary' (optional)."
    ))

    _esm_base = "List.jsx"

    def _handle_click(self, event):
        pass
