import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui import Reveal
from panel_material_ui.layout import Column, Paper
from panel_material_ui.pane import Typography
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def _app(duration=400):
    reveal = Reveal(color="error", duration=duration)
    cards = [
        Paper(Typography(f"Card {i}"), height=300, width=200, css_classes=["late"] if i in (6, 8) else [])
        for i in range(10)
    ]
    return Column(reveal, *cards), reveal


def _outline(page, text):
    return page.get_by_text(text).evaluate("""el => {
      let node = el;
      while (node) {
        if (node.classList?.contains("late")) return node.style.outline;
        node = node.parentNode ?? node.host;
      }
      return null;
    }""")


def test_reveal_scrolls_to_and_outlines_marked_elements(page):
    layout, reveal = _app()
    serve_component(page, layout)
    expect(page.get_by_text("Card 0")).to_be_in_viewport()

    reveal.scroll_to("late")
    expect(page.get_by_text("Card 6")).to_be_in_viewport()
    wait_until(lambda: "solid" in (_outline(page, "Card 6") or ""), page)
    assert "solid" in _outline(page, "Card 8")
    wait_until(lambda: _outline(page, "Card 6") == "", page)


def test_reveal_without_highlight(page):
    layout, reveal = _app()
    serve_component(page, layout)

    reveal.scroll_to("late", highlight=False)
    expect(page.get_by_text("Card 6")).to_be_in_viewport()
    assert _outline(page, "Card 6") == ""


def test_reveal_class_added_with_request(page):
    layout, reveal = _app()
    serve_component(page, layout)

    target = layout[3]
    target.css_classes = ["fresh"]
    reveal.scroll_to("fresh")
    expect(page.get_by_text("Card 2")).to_be_in_viewport()


def test_reveal_focus_moves_keyboard_focus(page):
    layout, reveal = _app()
    serve_component(page, layout)

    reveal.scroll_to("late", focus=True)
    wait_until(lambda: page.evaluate("""() => {
      let node = document.activeElement;
      while (node?.shadowRoot?.activeElement) node = node.shadowRoot.activeElement;
      return node?.classList.contains("late") ?? false;
    }"""), page)


def test_reveal_reduced_motion_jumps(page):
    page.emulate_media(reduced_motion="reduce")
    # The outline and its transition are removed after `duration`, so keep
    # them long enough to observe on a slow runner.
    layout, reveal = _app(duration=10_000)
    serve_component(page, layout)

    reveal.scroll_to("late")
    expect(page.get_by_text("Card 6")).to_be_in_viewport()
    wait_until(lambda: "solid" in (_outline(page, "Card 6") or ""), page)
    transition = page.get_by_text("Card 6").evaluate("""el => {
      let node = el;
      while (node && !node.classList?.contains("late")) node = node.parentNode ?? node.host;
      return node.style.transition;
    }""")
    assert transition.startswith("none")


def test_reveal_repeated_within_duration_restores_original_outline(page):
    layout, reveal = _app()
    serve_component(page, layout)

    reveal.scroll_to("late")
    wait_until(lambda: "solid" in (_outline(page, "Card 6") or ""), page)
    reveal.scroll_to("late")
    page.wait_for_timeout(100)
    assert "solid" in _outline(page, "Card 6")
    wait_until(lambda: _outline(page, "Card 6") == "", page)
    wait_until(lambda: _outline(page, "Card 8") == "", page)
