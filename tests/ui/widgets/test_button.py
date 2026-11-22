import re

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Row
from panel_material_ui.widgets import Button, Fab, IconButton, Toggle, ToggleIcon

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('button_style', ['contained', 'outlined', 'text'])
def test_button_style(page, button_style):
    widget = Button(label='Click', variant=button_style, color='primary')
    serve_component(page, widget)
    button_format = page.locator(f'.MuiButton-{button_style}')
    expect(button_format).to_have_count(1)


@pytest.mark.parametrize('button_type', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_button_type(page, button_type):
    widget = Button(label='Click', variant='contained', color=button_type)
    serve_component(page, widget)
    button_format = page.locator(f'.MuiButton-color{button_type.capitalize()}')
    expect(button_format).to_have_count(1)

def test_button_focus(page):
    widget = Button(label='Click')
    serve_component(page, widget)
    button = page.locator('.MuiButton-root')
    expect(button).to_have_count(1)
    widget.focus()
    expect(button).to_be_focused()

def test_button_with_description_keeps_dom_node_on_update(page):
    widget = Button(label='Click', description='Help')
    serve_component(page, widget)
    button = page.locator('.MuiButton-root')
    expect(button).to_have_count(1)
    handle = button.element_handle()

    widget.description = 'More help'
    widget.label = 'Updated'

    expect(button).to_contain_text('Updated')
    assert handle.evaluate('el => el.isConnected')

def test_button_on_click(page):
    events = []
    def cb(event):
        events.append(event)

    widget = Button(label='Click', on_click=cb)
    serve_component(page, widget)
    button = page.locator('.button')
    expect(button).to_have_count(1)
    button.click()
    wait_until(lambda: len(events) == 1, page)

def test_button_handle_click(page):
    widget = Button(label='Click')
    assert widget.clicks == 0
    serve_component(page, widget)
    button = page.locator('.button')
    button.click()
    wait_until(lambda: widget.clicks == 1, page)

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
        color=button_type,
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
    widget = Toggle(color=button_type)
    serve_component(page, widget)
    if button_type == 'error':
        button_color = page.locator(f'.Mui-{button_type}')
    else:
        button_color = page.locator(f'.MuiToggleButton-{button_type}')
    expect(button_color).to_have_count(1)


@pytest.mark.parametrize('widget_type', [Button, IconButton, Fab, Toggle])
def test_button_aria_attributes(page, widget_type):
    widget = widget_type(
        icon='menu', aria_label='Assistant, 2 pending', aria_expanded=False,
        aria={'controls': 'assistant-drawer', 'aria_haspopup': 'true'},
    )
    serve_component(page, widget)

    button = page.get_by_role('button', name='Assistant, 2 pending')
    expect(button).to_have_attribute('aria-expanded', 'false')
    expect(button).to_have_attribute('aria-controls', 'assistant-drawer')
    expect(button).to_have_attribute('aria-haspopup', 'true')

    widget.aria_expanded = True
    expect(button).to_have_attribute('aria-expanded', 'true')
    widget.aria_expanded = None
    expect(button).not_to_have_attribute('aria-expanded', re.compile('.*'))


def test_toggle_icon_aria_label(page):
    widget = ToggleIcon(icon='star', aria_label='Favorite')
    serve_component(page, widget)

    expect(page.get_by_role('checkbox', name='Favorite')).to_have_count(1)


@pytest.mark.parametrize('widget_type', [Button, IconButton])
def test_button_badge(page, widget_type):
    widget = widget_type(icon='mail', label='Inbox', badge=3)
    serve_component(page, widget)

    badge = page.locator('.MuiBadge-badge')
    expect(badge).to_have_text('3')
    expect(page.locator('button .MuiBadge-badge')).to_have_count(1)

    widget.badge = 120
    expect(badge).to_have_text('99+')
    widget.badge = 0
    expect(page.locator('.MuiBadge-root')).to_have_count(0)
    widget.badge = 'new'
    expect(badge).to_have_text('new')
    widget.badge = None
    expect(page.locator('.MuiBadge-root')).to_have_count(0)


def test_button_badge_without_icon(page):
    widget = Button(label='Approvals', badge=1)
    serve_component(page, widget)

    expect(page.locator('button .MuiBadge-badge')).to_have_text('1')
    expect(page.locator('button')).to_contain_text('Approvals')


def test_fab_badge_sits_on_the_button_edge(page):
    widget = Fab(icon='add', label='New', badge=7)
    serve_component(page, widget)

    button = page.get_by_role('button', name='New')
    badge = page.locator('.MuiBadge-badge')
    expect(badge).to_have_text('7')
    expect(page.locator('button .MuiBadge-badge')).to_have_count(0)
    icon = button.locator('.material-icons, .material-icons-outlined, svg').first
    badge_box, icon_box = badge.bounding_box(), icon.bounding_box()
    # The badge does not cover the middle of the icon.
    cx, cy = icon_box['x'] + icon_box['width'] / 2, icon_box['y'] + icon_box['height'] / 2
    assert not (badge_box['x'] < cx < badge_box['x'] + badge_box['width'] and badge_box['y'] < cy < badge_box['y'] + badge_box['height'])


def test_fab_label_names_circular_and_shows_extended(page):
    circular = Fab(icon='add', label='New')
    extended = Fab(icon='add', label='Create', variant='extended')
    serve_component(page, Row(circular, extended))

    expect(page.get_by_role('button', name='New')).not_to_contain_text('New')
    expect(page.get_by_role('button', name='Create')).to_contain_text('Create')
