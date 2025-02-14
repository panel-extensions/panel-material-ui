import param

from ..base import COLORS
from .base import MaterialWidget


class LoadingIndicator(MaterialWidget):
    """
    The `LoadingIndicator` provides a visual representation as a spinner of the loading status.

    References:
    - https://panel.holoviz.org/reference/indicators/LoadingSpinner.html
    - https://mui.com/material-ui/react-progress/#circular

    :Example:

    >>> LoadingIndicator(color='success')
    """

    color = param.Selector(objects=COLORS, default="primary")

    value = param.Number(default=0, bounds=(0, 100))

    variant = param.Selector(default="indeterminate", objects=["determinate", "indeterminate"])

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

    color = param.Selector(objects=COLORS, default="primary")

    value = param.Number(default=0, bounds=(0, 100))

    variant = param.Selector(default="determinate", objects=["determinate", "indeterminate", "buffer", "query"])

    _esm_base = "LinearProgress.jsx"
