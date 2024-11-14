import param

from ..base import COLORS
from .base import MaterialWidget


class LoadingIndicator(MaterialWidget):
    color = param.Selector(objects=COLORS, default="primary")

    size = param.Integer(default=None, bounds=(0, None))

    thickness = param.Number(default=3.6)

    value = param.Number(default=0, bounds=(0, 100))

    variant = param.Selector(default="indeterminate", objects=["determinate", "indeterminate"])

    with_label = param.Boolean(default=False)

    width = param.Integer(default=None)

    _esm = "CircularProgress.jsx"


class Progress(MaterialWidget):
    color = param.Selector(objects=COLORS, default="primary")

    value = param.Number(default=0, bounds=(0, 100))

    variant = param.Selector(default="determinate", objects=["determinate", "indeterminate", "buffer", "query"])

    _esm = "LinearProgress.jsx"
