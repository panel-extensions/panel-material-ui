import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Paper
from panel_material_ui.widgets import Button
from panel_material_ui.wrappers import Skeleton
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def _page_width(page):
    return page.evaluate("() => document.body.clientWidth")


def _width(locator):
    box = locator.bounding_box()
    return box["width"] if box else 0


def test_skeleton_renders_placeholder_when_inactive(page):
    widget = Skeleton(Button(label="Hi"), active=False)
    serve_component(page, widget)

    expect(page.locator('.MuiSkeleton-root')).to_have_count(1)
    expect(page.locator('.MuiButton-root')).to_have_count(0)


def test_skeleton_reveals_child_when_active(page):
    widget = Skeleton(Button(label="Hi"), active=True)
    serve_component(page, widget)

    expect(page.locator('.MuiSkeleton-root')).to_have_count(0)
    expect(page.locator('.MuiButton-root')).to_have_count(1)


def test_skeleton_active_toggle(page):
    widget = Skeleton(Button(label="Hi"), active=False)
    serve_component(page, widget)

    expect(page.locator('.MuiSkeleton-root')).to_have_count(1)
    widget.active = True
    expect(page.locator('.MuiButton-root')).to_have_count(1)
    expect(page.locator('.MuiSkeleton-root')).to_have_count(0)


def test_skeleton_placeholder_fills_responsive_child(page):
    # A stretch_width child should make the placeholder fill its container,
    # not collapse to a narrow sliver. Regression test for the inline-flex bug.
    widget = Skeleton(
        Paper(sizing_mode="stretch_width", height=80),
        active=False, sizing_mode="stretch_width",
    )
    serve_component(page, widget)

    skeleton = page.locator('.MuiSkeleton-root')
    expect(skeleton).to_have_count(1)
    wait_until(lambda: _width(skeleton) > _page_width(page) * 0.8, page)


def test_skeleton_revealed_fills_responsive_child(page):
    widget = Skeleton(
        Paper(sizing_mode="stretch_width", height=80),
        active=True, sizing_mode="stretch_width",
    )
    serve_component(page, widget)

    paper = page.locator('.MuiPaper-root')
    expect(paper).to_have_count(1)
    wait_until(lambda: _width(paper) > _page_width(page) * 0.8, page)


def test_skeleton_placeholder_hugs_fixed_child(page):
    # A non-responsive child must NOT be stretched to full width.
    widget = Skeleton(Button(label="Hi"), active=False)
    serve_component(page, widget)

    skeleton = page.locator('.MuiSkeleton-root')
    expect(skeleton).to_have_count(1)
    wait_until(lambda: 0 < _width(skeleton) < _page_width(page) * 0.5, page)


def test_skeleton_revealed_hugs_fixed_child(page):
    widget = Skeleton(Button(label="Hi"), active=True)
    serve_component(page, widget)

    button = page.locator('.MuiButton-root')
    expect(button).to_have_count(1)
    wait_until(lambda: 0 < _width(button) < _page_width(page) * 0.5, page)
