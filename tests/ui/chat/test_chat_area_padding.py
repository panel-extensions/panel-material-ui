import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.chat import ChatAreaInput

pytestmark = pytest.mark.ui

# The insets, from the outline's outer edge, of the text and of the icons on either side.
_INSETS = """
(textarea) => {
  const root = textarea.closest(".MuiInputBase-root")
  const outline = root.querySelector("fieldset").getBoundingClientRect()
  const text = textarea.getBoundingClientRect().left + parseFloat(getComputedStyle(textarea).paddingLeft)
  const icons = [...root.querySelectorAll("button svg")].map((svg) => svg.getBoundingClientRect())
  return {
    text: text - outline.left,
    start: icons.length > 1 ? icons[0].left - outline.left : null,
    end: outline.right - icons[icons.length - 1].right,
  }
}
"""


def _insets(page):
    textarea = page.locator("textarea:visible").first
    textarea.wait_for()
    return textarea.evaluate(_INSETS)


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_chat_area_text_inset_without_start_button(page, theme):
    page.emulate_media(color_scheme=theme)
    widget = ChatAreaInput(enable_upload=False, placeholder="Ask the agent…")
    serve_component(page, widget)

    insets = _insets(page)
    # As far in as an outlined input's text, and as the send icon is from the right.
    assert insets["text"] >= 14
    assert abs(insets["text"] - insets["end"]) <= 1


def test_chat_area_start_button_inset_matches_send_button(page):
    widget = ChatAreaInput(enable_upload=True)
    serve_component(page, widget)

    insets = _insets(page)
    assert abs(insets["start"] - insets["end"]) <= 1
