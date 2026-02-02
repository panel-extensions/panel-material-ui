import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import MultiPill, Pill
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_pill_basic_selection(page):
    widget = Pill(label="Pill test", options=["Option 1", "Option 2", "Option 3"])
    serve_component(page, widget)

    expect(page.locator(".MuiChip-root")).to_have_count(3)
    page.locator(".MuiChip-root").nth(1).click()
    wait_until(lambda: widget.value == "Option 2", page)


def test_pill_disabled_options(page):
    widget = Pill(
        label="Pill test",
        options=["Option 1", "Option 2", "Option 3"],
        disabled_options=["Option 2"],
    )
    serve_component(page, widget)

    expect(page.locator(".MuiChip-root.Mui-disabled")).to_have_count(1)
    expect(page.locator(".MuiChip-root.Mui-disabled .MuiChip-label")).to_have_text("Option 2")


def test_multipill_max_items(page):
    widget = MultiPill(
        label="MultiPill test",
        options=["Option 1", "Option 2", "Option 3"],
        max_items=2,
    )
    serve_component(page, widget)

    page.locator(".MuiChip-root").nth(0).click()
    page.locator(".MuiChip-root").nth(1).click()
    wait_until(lambda: widget.value == ["Option 1", "Option 2"], page)

    page.locator(".MuiChip-root").nth(2).click()
    wait_until(lambda: widget.value == ["Option 2", "Option 3"], page)
