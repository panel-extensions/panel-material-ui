from __future__ import annotations

import typing as t

import param

from .base import COLORS, ColorType, MaterialComponent


class Reveal(MaterialComponent):
    """
    The `Reveal` scrolls to the elements on the page carrying a CSS
    class and briefly outlines them, e.g. to point users at the cards
    that need their attention.

    It renders nothing itself; place it anywhere in the app and call
    `scroll_to` with a CSS class. Elements are found across Panel's
    shadow roots. Users who prefer reduced motion get an instant jump
    and an outline without a fade.

    :References:

    - https://panel-material-ui.holoviz.org/reference/global/Reveal.html

    :Example:

    >>> reveal = Reveal()
    >>> card = Card(..., css_classes=["needs-review"])
    >>> reveal.scroll_to("needs-review")
    """

    color: ColorType = param.Selector(default="primary", objects=COLORS, doc="""
        The theme color of the outline.""")  # type: ignore[assignment]

    duration = param.Integer(default=2200, bounds=(0, None), doc="""
        Milliseconds the outline is shown before it fades.""")

    _esm_base = "Reveal.jsx"

    def __init__(self, **params):
        params.setdefault("margin", 0)
        params.setdefault("width", 0)
        params.setdefault("height", 0)
        super().__init__(**params)

    def scroll_to(
        self,
        css_class: str,
        highlight: bool = True,
        focus: bool = False,
        block: t.Literal["start", "center", "end", "nearest"] = "center",
    ) -> None:
        """
        Scroll to the first element carrying `css_class` and outline every one.

        Parameters
        ----------
        css_class: str
            The CSS class marking the elements, e.g. set via `css_classes`.
        highlight: bool
            Whether to briefly outline the elements.
        focus: bool
            Whether to move keyboard focus to the first element, so screen
            reader users land on it too.
        block: str
            Where the first element is aligned in the scrolled area.
        """
        self._send_msg({"css_class": css_class, "highlight": highlight, "focus": focus, "block": block})


__all__ = ["Reveal"]
