import pytest

pytest.importorskip('playwright')

from panel_material_ui.widgets import Button, ButtonIcon, Toggle

from playwright.sync_api import expect
from tests.util import serve_component, wait_until

pytestmark = pytest.mark.ui


@pytest.mark.xfail(reason='')
@pytest.mark.parametrize('button_style', ['contained', 'outlined', 'text'])
@pytest.mark.parametrize('button_type', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def _test_button_format(page, button_style, button_type):
    widget = Button(name='Click', button_style=button_style, button_type=button_type)
    serve_component(page, widget)
    # TODO: this check should pass
    button_format = page.locator(f'.MuiButton-{button_style}{button_type.capitalize()}')
    expect(button_format).to_have_count(1)


def test_button_on_click(page):
    events = []
    def cb(event):
        events.append(event)

    widget = Button(name='Click', on_click=cb)
    serve_component(page, widget)
    button = page.locator('.button')
    expect(button).to_have_count(1)
    button.click()
    wait_until(lambda: len(events) == 1, page)


def test_button_handle_click(page):
    widget = Button(name='Click')
    assert widget.clicks == 0
    serve_component(page, widget)
    button = page.locator('.button')
    button.click()
    assert widget.clicks == 1


def test_button_icon(page):
    widget = ButtonIcon(
        icon='favorite',
        active_icon='check',
        toggle_duration=3000,
    )
    serve_component(page, widget)
    button_icon = page.locator('.button-icon')
    icon = page.locator('.material-icons')
    wait_until(lambda: expect(button_icon).to_have_count(1), page=page)
    wait_until(lambda: expect(icon).to_have_text('favorite'), page=page)
    button_icon.click()
    wait_until(lambda: expect(icon).to_have_text('check'), page=page)


@pytest.mark.parametrize('button_type', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_button_icon_format(page, button_type):
    widget = ButtonIcon(
        icon='favorite',
        active_icon='check',
        button_type=button_type,
        toggle_duration=3000,
    )
    serve_component(page, widget)
    button_color = page.locator(f'.MuiIconButton-color{button_type.capitalize()}')
    expect(button_color).to_have_count(1)


def test_toggle(page):
    widget = Toggle()
    serve_component(page, widget)
    assert widget.value == False  # noqa
    toggle = page.locator('.toggle')
    expect(toggle).to_have_count(1)
    toggle_nonpressed = page.locator("button[aria-pressed='false']")
    expect(toggle_nonpressed).to_have_count(1)

    toggle.click()
    toggle_pressed = page.locator("button[aria-pressed='true']")
    wait_until(lambda: expect(toggle_pressed).to_have_count(1), page=page)
    wait_until(lambda: widget.value, page=page)


@pytest.mark.parametrize('button_type', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_toggle_format(page, button_type):
    widget = Toggle(button_type=button_type)
    serve_component(page, widget)
    if button_type == 'error':
        button_color = page.locator(f'.Mui-{button_type}')
    else:
        button_color = page.locator(f'.MuiToggleButton-{button_type}')
    expect(button_color).to_have_count(1)