import param

from ..base import COLORS
from .base import MaterialWidget


class LoadingSpinner(MaterialWidget):
    """
    The `LoadingSpinner` provides a visual representation as a spinner of the loading status.

    References:
    - https://panel.holoviz.org/reference/indicators/LoadingSpinner.html
    - https://mui.com/material-ui/react-progress/#circular

    :Example:

    >>> LoadingSpinner(color='success')
    """

    color = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the loading indicator.""")

    size = param.Integer(default=40, doc="""
        The size of the loading spinner.""")

    value = param.Number(default=0, bounds=(0, 100), doc="""
        The value of the loading indicator.""")

    variant = param.Selector(default="indeterminate", objects=["determinate", "indeterminate"], doc="""
        The variant of the loading indicator.""")

    width = param.Integer(default=None)

    _esm_base = "CircularProgress.jsx"


class Progress(MaterialWidget):
    """
    The `Progress` widget displays the progress towards some target
    based on the current `value` and the `max` value.

    References:
    - https://panel.holoviz.org/reference/indicators/Progress.html
    - https://mui.com/material-ui/react-progress/#linear

    :Example:

    >>> Progress(value=20, color="primary")
    """

    color = param.Selector(objects=COLORS, default="primary", doc="""
        The color of the progress bar.""")

    value = param.Number(default=0, bounds=(0, 100), doc="""
        The value of the progress bar.""")

    variant = param.Selector(default="determinate", objects=["determinate", "indeterminate", "buffer", "query"], doc="""
        The variant of the progress bar.""")

    _esm_base = "LinearProgress.jsx"


__all__ = [
    "LoadingSpinner",
    "Progress"
]
