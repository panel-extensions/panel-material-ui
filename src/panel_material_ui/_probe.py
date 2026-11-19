from __future__ import annotations

import param
from panel.viewable import Children

from .base import MaterialComponent


class Probe(MaterialComponent):
    """
    Exposes the model and host it is rendered with to the browser, so the
    conformance tests can exercise the component interface on every host
    that implements it. Not part of the public API.
    """

    direction = param.Selector(default="column", objects=["row", "column"])

    key = param.String(default="probe")

    objects = Children()

    value = param.Integer(default=0)

    _compilable = True

    _esm_base = "Probe.jsx"

    def __init__(self, **params):
        super().__init__(**params)
        self.received: list = []
        self.events: list = []

    def _handle_msg(self, msg):
        self.received.append(msg)

    def _handle_click(self, event):
        self.events.append(event)
