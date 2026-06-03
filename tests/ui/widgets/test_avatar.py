import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Avatar
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_avatar_text(page):
    widget = Avatar(content="JD")
    serve_component(page, widget)
    expect(page.locator('.MuiAvatar-root')).to_have_count(1)
    expect(page.locator('.MuiAvatar-root')).to_have_text("JD")


def test_avatar_image(page):
    widget = Avatar(
        content="https://mui.com/static/images/avatar/1.jpg",
        alt_text="User",
    )
    serve_component(page, widget)
    img = page.locator('.MuiAvatar-img')
    expect(img).to_have_count(1)
    expect(img).to_have_attribute('alt', 'User')


@pytest.mark.parametrize('variant', ['rounded', 'square'])
def test_avatar_variant(page, variant):
    widget = Avatar(content="AB", variant=variant)
    serve_component(page, widget)
    expect(page.locator(f'.MuiAvatar-{variant}')).to_have_count(1)


@pytest.mark.parametrize('size', ['small', 'medium', 'large'])
def test_avatar_size(page, size):
    widget = Avatar(content="AB", size=size)
    serve_component(page, widget)
    expect(page.locator('.MuiAvatar-root')).to_have_count(1)


def test_avatar_on_click(page):
    events = []
    def cb(event):
        events.append(event)

    widget = Avatar(content="JD", on_click=cb)
    serve_component(page, widget)
    page.locator('.MuiAvatar-root').click()
    wait_until(lambda: len(events) == 1, page)


def test_avatar_clicks(page):
    widget = Avatar(content="JD")
    serve_component(page, widget)
    page.locator('.MuiAvatar-root').click()
    wait_until(lambda: widget.clicks == 1, page)


def test_avatar_content_update(page):
    widget = Avatar(content="AB")
    serve_component(page, widget)
    expect(page.locator('.MuiAvatar-root')).to_have_text("AB")
    widget.content = "CD"
    expect(page.locator('.MuiAvatar-root')).to_have_text("CD")
