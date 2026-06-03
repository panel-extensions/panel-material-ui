from .base import *  # noqa


def __getattr__(name):
    if name == "Chip":
        import warnings
        warnings.warn(
            "Importing Chip from panel_material_ui.pane is deprecated. "
            "Use panel_material_ui.widgets.Chip instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from ..widgets import Chip
        return Chip
    raise AttributeError(f"module 'panel_material_ui.pane' has no attribute {name!r}")
