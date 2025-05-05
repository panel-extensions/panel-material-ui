import param

from ..base import COLORS, ThemedTransform
from .base import MaterialWidget


class LoadingSpinner(MaterialWidget):
    """
    The `LoadingSpinner` provides a visual representation as a spinner of the loading status.

    :References:

    - https://panel-material-ui.holoviz.org/reference/indicators/LoadingSpinner.html
    - https://panel.holoviz.org/reference/indicators/LoadingSpinner.html
    - https://mui.com/material-ui/react-progress/#circular

    :Example:

    >>> LoadingSpinner(color='success')
    """

    bgcolor = param.Selector(default=None, objects=[None, "light", "dark"], doc="""
        The background color of the loading spinner.""")

    color = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the loading indicator.""")

    size = param.Integer(default=40, doc="""
        The size of the loading spinner.""")

    thickness = param.Number(default=3.6, doc="""
        The thickness of the loading spinner.""")

    value = param.Number(default=0, bounds=(0, 100), doc="""
        The value of the loading indicator.""")

    variant = param.Selector(default="indeterminate", objects=["determinate", "indeterminate"], doc="""
        The variant of the loading indicator.""")

    width = param.Integer(default=None)

    with_label = param.Boolean(default=False, doc="""
        Whether to show a label indicating the progress.""")

    _esm_base = "CircularProgress.jsx"
    _esm_transforms = [ThemedTransform]


class Progress(MaterialWidget):
    """
    The `Progress` widget displays the progress towards some target
    based on the current `value` and the `max` value.

    :References:

    - https://panel-material-ui.holoviz.org/reference/indicators/Progress.html
    - https://panel.holoviz.org/reference/indicators/Progress.html
    - https://mui.com/material-ui/react-progress/#linear

    :Example:

    >>> Progress(value=20, color="primary")
    """

    active = param.Boolean(default=True, doc="""
        Whether to animate the bar when in indeterminate mode.""")

    color = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the progress bar.""")

    value = param.Number(default=-1, bounds=(-1, 100), doc="""
        The value of the progress bar.""")

    value_buffer = param.Number(default=-1, bounds=(-1, 100), doc="""
        The buffer of the progress bar (if variant="buffer").""")

    variant = param.Selector(default="determinate", objects=["determinate", "indeterminate", "buffer", "query"], doc="""
        The variant of the progress bar.""")

    _esm_base = "LinearProgress.jsx"
    _esm_transforms = [ThemedTransform]

    @param.depends("value", watch=True, on_init=True)
    def _update_value(self, *_, **__):
        if self.value == -1 and self.variant == "determinate":
            self.variant = "indeterminate"

# Generalize or move to dashboard example
# Could not get icon from ReactComponent so included it here

class ChangeIndicator(MaterialWidget):
    value = param.String(default="")
    title = param.String()
    icon = param.String()
    change_percent = param.Number()
    since = param.String()

    _esm_base = "ChangeIndicator.jsx"

    _importmap = {
        "imports": {
            "@mui/material": "https://esm.sh/@mui/material@6.4.9",
        }
    }

class Icon(MaterialWidget):
    """The Icon component will display an icon from the Material UI Icon set.

    References:

    - https://mui.com/material-ui/icons/#icon-font-icons
    - https://mui.com/material-ui/api/icon/
    """
    value = param.String(default="", doc="The snake cased name of the icon font ligature.")
    color = param.String(default="inherit", doc="""The color of the component.
    It supports both default and custom theme colors""")
    font_size= param.String(default="medium", doc="""The fontSize applied to the icon.
    Defaults to medium, but can be configured to inherit font size.""")

    _esm_base="Icon.jsx"

__all__ = [
    "ChangeIndicator",
    "Icon",
    "LoadingSpinner",
    "Progress",
]
