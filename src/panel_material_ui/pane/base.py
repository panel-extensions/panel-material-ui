import param

from ..base import COLORS, MaterialComponent


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

    _esm = "Chip.jsx"

    _stylesheets = ["https://fonts.googleapis.com/icon?family=Material+Icons"]

    def _handle_click(self, event):
        pass


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

    _esm = "Avatar.jsx"


class Skeleton(MaterialComponent):
    variant = param.Selector(objects=["circular", "rectangular", "rounded"], default="rounded")

    height = param.Integer(default=0)

    width = param.Integer(default=0)

    _esm = "Skeleton.jsx"
