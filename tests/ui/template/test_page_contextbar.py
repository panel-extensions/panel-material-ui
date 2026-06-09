import pytest

pytest.importorskip('playwright')

import panel as pn
from panel.tests.util import serve_component
from playwright.sync_api import expect

from panel_material_ui.template import Page

pytestmark = pytest.mark.ui


def test_page_contextbar_persistent_toggle_visible_when_open(page):
    """The TocIcon toggle button remains visible when contextbar is open."""
    pg = Page(
        main=[pn.pane.Markdown("# Main")],
        contextbar=[pn.pane.Markdown("# Context")],
        contextbar_variant="persistent",
        contextbar_open=True,
    )

    serve_component(page, pg)

    toggle = page.locator('[aria-label="Close contextbar"]')
    expect(toggle).to_be_visible()


def test_page_contextbar_persistent_toggle_closes(page):
    """Clicking the toggle when contextbar is open should close it."""
    pg = Page(
        main=[pn.pane.Markdown("# Main")],
        contextbar=[pn.pane.Markdown("# Context")],
        contextbar_variant="persistent",
        contextbar_open=True,
    )

    serve_component(page, pg)

    toggle = page.locator('[aria-label="Close contextbar"]')
    toggle.click()

    page.wait_for_timeout(300)

    assert pg.contextbar_open is False


def test_page_contextbar_persistent_main_shifts_on_open(page):
    """Main area should shift (gain negative marginRight) when contextbar closes."""
    pg = Page(
        main=[pn.pane.Markdown("# Main")],
        contextbar=[pn.pane.Markdown("# Context")],
        contextbar_variant="persistent",
        contextbar_width=300,
        contextbar_open=False,
    )

    serve_component(page, pg)

    main = page.locator("main.main")
    expect(main).to_have_css("margin-right", "-300px")

    pg.contextbar_open = True
    page.wait_for_timeout(500)

    expect(main).to_have_css("margin-right", "0px")


def test_page_contextbar_persistent_toolbar_offset(page):
    """Persistent contextbar should have a toolbar spacer so content isn't hidden by AppBar."""
    pg = Page(
        main=[pn.pane.Markdown("# Main")],
        contextbar=[pn.pane.Markdown("# Context")],
        contextbar_variant="persistent",
        contextbar_open=True,
    )

    serve_component(page, pg)

    contextbar_paper = page.locator(".MuiDrawer-paper.contextbar")
    expect(contextbar_paper).to_be_visible()

    toolbar = contextbar_paper.locator(".MuiToolbar-root")
    expect(toolbar).to_be_visible()


def test_page_contextbar_temporary_no_toolbar_offset(page):
    """Temporary contextbar should not have a toolbar spacer."""
    pg = Page(
        main=[pn.pane.Markdown("# Main")],
        contextbar=[pn.pane.Markdown("# Context")],
        contextbar_variant="temporary",
        contextbar_open=True,
    )

    serve_component(page, pg)

    contextbar_paper = page.locator(".MuiDrawer-paper.contextbar")
    expect(contextbar_paper).to_be_visible()

    toolbar = contextbar_paper.locator(".MuiToolbar-root")
    expect(toolbar).to_have_count(0)


def test_page_contextbar_temporary_main_full_width(page):
    """With temporary variant, main should not have negative margin."""
    pg = Page(
        main=[pn.pane.Markdown("# Main")],
        contextbar=[pn.pane.Markdown("# Context")],
        contextbar_variant="temporary",
        contextbar_open=False,
    )

    serve_component(page, pg)

    main = page.locator("main.main")
    expect(main).to_have_css("margin-right", "0px")


def test_page_contextbar_permanent_no_toggle(page):
    """Permanent variant should not show a toggle button."""
    pg = Page(
        main=[pn.pane.Markdown("# Main")],
        contextbar=[pn.pane.Markdown("# Context")],
        contextbar_variant="permanent",
        contextbar_open=True,
    )

    serve_component(page, pg)

    toggle = page.locator('[aria-label*="contextbar"]')
    expect(toggle).to_have_count(0)
