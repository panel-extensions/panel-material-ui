import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Button, IconButton, Toggle
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('button_style', ['contained', 'outlined', 'text'])
def test_button_style(page, button_style):
    widget = Button(name='Click', button_style=button_style, button_type='primary')
    serve_component(page, widget)
    button_format = page.locator(f'.MuiButton-{button_style}Primary')
    expect(button_format).to_have_count(1)


@pytest.mark.parametrize('button_type', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_button_type(page, button_type):
    widget = Button(name='Click', button_style='contained', button_type=button_type)
    serve_component(page, widget)
    button_format = page.locator(f'.MuiButton-contained{button_type.capitalize()}')
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


def test_icon_button(page):
    widget = IconButton(
        icon='favorite',
        active_icon='check',
        toggle_duration=3000,
    )
    serve_component(page, widget)
    button_icon = page.locator('.icon-button')
    icon = page.locator('.material-icons')

    expect(button_icon).to_have_count(1)
    expect(icon).to_have_text('favorite')

    button_icon.click(force=True)
    expect(icon).to_have_text('check')


@pytest.mark.parametrize('button_type', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_icon_button_format(page, button_type):
    widget = IconButton(
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
    expect(toggle_pressed).to_have_count(1)
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
