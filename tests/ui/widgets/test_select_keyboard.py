import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Dialog, Drawer
from panel_material_ui.widgets import MultiChoice, Select

pytestmark = pytest.mark.ui

OPEN_KEYS = ['Enter', 'Space', 'ArrowDown']


def _focus_select(page):
    combobox = page.get_by_role('combobox')
    expect(combobox).to_be_visible()
    combobox.focus()
    expect(combobox).to_be_focused()
    return combobox


@pytest.mark.parametrize('label', ['Pick', ''])
@pytest.mark.parametrize('key', OPEN_KEYS)
def test_select_opens_with_keyboard(page, key, label):
    widget = Select(label=label, options=['A', 'B', 'C'], value='A')
    serve_component(page, widget)

    combobox = _focus_select(page)
    page.keyboard.press(key)

    expect(page.get_by_role('listbox')).to_be_visible()
    expect(combobox).to_have_attribute('aria-expanded', 'true')
    wait_until(lambda: widget.dropdown_open, page)


def test_select_keyboard_navigation_selects_option(page):
    widget = Select(label='Pick', options=['A', 'B', 'C'], value='A')
    serve_component(page, widget)

    combobox = _focus_select(page)
    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('option', name='A')).to_be_focused()

    page.keyboard.press('ArrowDown')
    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('option', name='C')).to_be_focused()
    page.keyboard.press('ArrowUp')
    expect(page.get_by_role('option', name='B')).to_be_focused()

    page.keyboard.press('Enter')
    expect(page.get_by_role('listbox')).to_have_count(0)
    wait_until(lambda: widget.value == 'B', page)
    expect(combobox).to_have_text('B')
    expect(combobox).to_be_focused()


def test_select_escape_closes_and_returns_focus(page):
    widget = Select(label='Pick', options=['A', 'B'], value='A')
    serve_component(page, widget)

    combobox = _focus_select(page)
    page.keyboard.press('Enter')
    expect(page.get_by_role('listbox')).to_be_visible()

    page.keyboard.press('Escape')
    expect(page.get_by_role('listbox')).to_have_count(0)
    expect(combobox).to_be_focused()
    expect(combobox).to_have_attribute('aria-expanded', 'false')
    wait_until(lambda: not widget.dropdown_open, page)
    assert widget.value == 'A'

    # Reopening works after the keyboard closed the menu.
    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('listbox')).to_be_visible()


def test_select_tab_moves_focus_past_closed_select(page):
    first = Select(label='First', options=['A', 'B'], value='A')
    second = Select(label='Second', options=['C', 'D'], value='C')
    serve_component(page, Dialog(first, second, open=True))

    boxes = page.get_by_role('combobox')
    expect(boxes).to_have_count(2)
    boxes.nth(0).focus()
    page.keyboard.press('Tab')
    expect(boxes.nth(1)).to_be_focused()


def test_select_click_still_opens(page):
    widget = Select(label='Pick', options=['A', 'B'], value='A')
    serve_component(page, widget)

    page.get_by_role('combobox').click()
    expect(page.get_by_role('listbox')).to_be_visible()
    page.get_by_role('option', name='B').click()
    expect(page.get_by_role('listbox')).to_have_count(0)
    wait_until(lambda: widget.value == 'B', page)


def test_select_disabled_does_not_open_with_keyboard(page):
    widget = Select(label='Pick', options=['A', 'B'], value='A', disabled=True)
    serve_component(page, widget)

    combobox = page.get_by_role('combobox')
    expect(combobox).to_be_visible()
    combobox.focus()
    for key in OPEN_KEYS:
        page.keyboard.press(key)
    page.wait_for_timeout(300)
    expect(page.get_by_role('listbox')).to_have_count(0)
    assert not widget.dropdown_open


@pytest.mark.parametrize('container', [Dialog, Drawer])
@pytest.mark.parametrize('key', OPEN_KEYS)
def test_select_in_modal_opens_with_keyboard(page, container, key):
    widget = Select(label='Pick', options=['A', 'B', 'C'], value='A')
    serve_component(page, container(widget, open=True))

    combobox = _focus_select(page)
    page.keyboard.press(key)
    expect(page.get_by_role('listbox')).to_be_visible()

    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('option', name='B')).to_be_focused()
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == 'B', page)

    page.keyboard.press('Enter')
    expect(page.get_by_role('listbox')).to_be_visible()
    page.keyboard.press('Escape')
    expect(page.get_by_role('listbox')).to_have_count(0)
    expect(combobox).to_be_focused()
    # Escape closed only the menu, not the surrounding Dialog or Drawer.
    expect(combobox).to_be_visible()


@pytest.mark.parametrize('label', ['Pick', ''])
@pytest.mark.parametrize('key', OPEN_KEYS)
def test_multi_choice_opens_with_keyboard(page, key, label):
    widget = MultiChoice(label=label, options=['A', 'B', 'C'], value=['A'])
    serve_component(page, widget)

    combobox = _focus_select(page)
    page.keyboard.press(key)
    expect(page.get_by_role('listbox')).to_be_visible()

    expect(page.get_by_role('option', name='B')).to_be_focused()
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == ['A', 'B'], page)
    # A multi select stays open so several options can be picked.
    expect(page.get_by_role('listbox')).to_be_visible()

    page.keyboard.press('Escape')
    expect(page.get_by_role('listbox')).to_have_count(0)
    expect(combobox).to_be_focused()


@pytest.mark.parametrize('container', [Dialog, Drawer])
def test_multi_choice_in_modal_opens_with_keyboard(page, container):
    widget = MultiChoice(label='Pick', options=['A', 'B', 'C'], value=[])
    serve_component(page, container(widget, open=True))

    combobox = _focus_select(page)
    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('listbox')).to_be_visible()
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == ['A'], page)
    page.keyboard.press('Escape')
    expect(page.get_by_role('listbox')).to_have_count(0)
    expect(combobox).to_be_focused()


def test_multi_choice_disabled_does_not_open_with_keyboard(page):
    widget = MultiChoice(label='Pick', options=['A', 'B'], value=['A'], disabled=True)
    serve_component(page, widget)

    combobox = page.get_by_role('combobox')
    expect(combobox).to_be_visible()
    combobox.focus()
    for key in OPEN_KEYS:
        page.keyboard.press(key)
    page.wait_for_timeout(300)
    expect(page.get_by_role('listbox')).to_have_count(0)


def test_select_options_are_listbox_options(page):
    widget = Select(label='Pick', options=['A', 'B', 'C'], value='B')
    serve_component(page, widget)

    _focus_select(page)
    page.keyboard.press('Enter')
    listbox = page.get_by_role('listbox')
    expect(listbox.get_by_role('option')).to_have_count(3)
    expect(page.get_by_role('option', name='B')).to_have_attribute('aria-selected', 'true')
    expect(page.get_by_role('option', name='A')).to_have_attribute('aria-selected', 'false')


def test_multi_choice_options_announce_selection(page):
    widget = MultiChoice(label='Pick', options=['A', 'B', 'C'], value=['A'], searchable=True)
    serve_component(page, widget)

    _focus_select(page)
    page.keyboard.press('Enter')
    expect(page.get_by_role('option', name='A')).to_have_attribute('aria-selected', 'true')
    expect(page.get_by_role('option', name='B')).to_have_attribute('aria-selected', 'false')


@pytest.mark.parametrize('key', OPEN_KEYS)
def test_searchable_select_focuses_search_on_open(page, key):
    widget = Select(label='Pick', options=['Apple', 'Banana', 'Cherry'], value='Apple', searchable=True)
    serve_component(page, widget)

    _focus_select(page)
    page.keyboard.press(key)
    search = page.get_by_placeholder('Search...')
    expect(search).to_be_focused()

    page.keyboard.type('an')
    wait_until(lambda: widget.filter_str == 'an', page)
    expect(page.get_by_role('option')).to_have_count(1)
    expect(page.get_by_role('option', name='Banana')).to_be_visible()


def test_searchable_select_keyboard_flow(page):
    widget = Select(label='Pick', options=['Apple', 'Banana', 'Cherry'], value='Apple', searchable=True)
    serve_component(page, widget)

    combobox = _focus_select(page)
    page.keyboard.press('ArrowDown')
    search = page.get_by_placeholder('Search...')
    expect(search).to_be_focused()

    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('option', name='Apple')).to_be_focused()
    page.keyboard.press('ArrowUp')
    expect(search).to_be_focused()

    page.keyboard.press('ArrowDown')
    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('option', name='Banana')).to_be_focused()
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == 'Banana', page)
    expect(page.get_by_role('listbox')).to_have_count(0)
    expect(combobox).to_be_focused()

    page.keyboard.press('Enter')
    expect(search).to_be_focused()
    page.keyboard.press('Escape')
    expect(page.get_by_role('listbox')).to_have_count(0)
    expect(combobox).to_be_focused()
    assert widget.value == 'Banana'


@pytest.mark.parametrize('container', [Dialog, Drawer])
def test_searchable_select_in_modal_keyboard_flow(page, container):
    widget = Select(label='Pick', options=['Apple', 'Banana'], value='Apple', searchable=True)
    serve_component(page, container(widget, open=True))

    combobox = _focus_select(page)
    page.keyboard.press('Enter')
    search = page.get_by_placeholder('Search...')
    expect(search).to_be_focused()
    page.keyboard.type('ban')
    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('option', name='Banana')).to_be_focused()
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == 'Banana', page)
    expect(combobox).to_be_focused()


def test_searchable_multi_choice_keyboard_flow(page):
    widget = MultiChoice(label='Pick', options=['Apple', 'Banana', 'Cherry'], value=[], searchable=True)
    serve_component(page, widget)

    combobox = _focus_select(page)
    page.keyboard.press('Enter')
    search = page.get_by_placeholder('Search...')
    expect(search).to_be_focused()
    page.keyboard.type('ch')
    page.keyboard.press('ArrowDown')
    expect(page.get_by_role('option', name='Cherry')).to_be_focused()
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == ['Cherry'], page)
    expect(page.get_by_role('option', name='Cherry')).to_have_attribute('aria-selected', 'true')

    page.keyboard.press('Escape')
    expect(page.get_by_role('listbox')).to_have_count(0)
    expect(combobox).to_be_focused()


@pytest.mark.parametrize('container', [Dialog, Drawer])
def test_searchable_select_in_modal_escape_returns_focus(page, container):
    widget = Select(label='Pick', options=['Apple', 'Banana'], value='Apple', searchable=True)
    serve_component(page, container(widget, open=True))

    combobox = _focus_select(page)
    for _ in range(3):
        page.keyboard.press('Enter')
        expect(page.get_by_placeholder('Search...')).to_be_focused()
        page.keyboard.press('Escape')
        expect(page.get_by_role('listbox')).to_have_count(0)
        expect(combobox).to_be_focused()


def test_searchable_select_clear_button_is_labelled(page):
    widget = Select(label='Pick', options=['Apple', 'Banana'], value='Apple', searchable=True)
    serve_component(page, widget)

    _focus_select(page)
    page.keyboard.press('Enter')
    expect(page.get_by_role('button', name='Clear search')).to_have_count(1)
