import re

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.template import AppBar
from panel_material_ui.widgets import Button

pytestmark = pytest.mark.ui


def test_appbar_title(page):
    appbar = AppBar(title="My App")

    serve_component(page, appbar)

    title = page.locator(".MuiTypography-root")
    expect(title).to_have_text("My App")


def test_appbar_title_update(page):
    appbar = AppBar(title="Original")

    serve_component(page, appbar)

    title = page.locator(".MuiTypography-root")
    expect(title).to_have_text("Original")

    appbar.title = "Updated"
    expect(title).to_have_text("Updated")


def test_appbar_no_title(page):
    appbar = AppBar()

    serve_component(page, appbar)

    title = page.locator(".MuiTypography-root")
    expect(title).to_have_count(0)


def test_appbar_icon(page):
    appbar = AppBar(icon="menu")

    serve_component(page, appbar)

    icon_button = page.locator(".MuiIconButton-root")
    expect(icon_button).to_be_visible()


def test_appbar_objects(page):
    btn = Button(label="Click Me")
    appbar = AppBar(title="App", objects=[btn])

    serve_component(page, appbar)

    button = page.locator(".MuiButton-root")
    expect(button).to_be_visible()
    expect(button).to_have_text("Click Me")


def test_appbar_objects_click(page):
    btn = Button(label="Action")
    appbar = AppBar(objects=[btn])

    serve_component(page, appbar)

    button = page.locator(".MuiButton-root")
    button.click()
    wait_until(lambda: btn.clicks == 1, page)


@pytest.mark.parametrize("color", ["primary", "secondary", "default", "transparent"])
def test_appbar_color(page, color):
    appbar = AppBar(title="App", color=color)

    serve_component(page, appbar)

    bar = page.locator(".MuiAppBar-root")
    expect(bar).to_have_class(re.compile(f"MuiAppBar-color{color.capitalize()}"))


@pytest.mark.parametrize("position", ["static", "fixed", "sticky", "relative", "absolute"])
def test_appbar_position(page, position):
    appbar = AppBar(title="App", position=position)

    serve_component(page, appbar)

    bar = page.locator(".MuiAppBar-root")
    expect(bar).to_have_class(re.compile(f"MuiAppBar-position{position.capitalize()}"))


@pytest.mark.parametrize("variant", ["dense", "regular"])
def test_appbar_variant(page, variant):
    appbar = AppBar(title="App", variant=variant)

    serve_component(page, appbar)

    toolbar = page.locator(".MuiToolbar-root")
    expect(toolbar).to_have_class(re.compile(f"MuiToolbar-{variant}"))
