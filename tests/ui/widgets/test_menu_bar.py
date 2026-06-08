import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import MenuBar
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


_BASIC_ITEMS = [
    {'label': 'File', 'items': [
        {'label': 'New', 'icon': 'note_add', 'hint': 'Ctrl+N'},
        {'label': 'Open', 'icon': 'folder_open', 'hint': 'Ctrl+O'},
        None,
        {'label': 'Save', 'icon': 'save', 'hint': 'Ctrl+S'},
    ]},
    {'label': 'Edit', 'items': [
        {'label': 'Undo', 'icon': 'undo'},
        {'label': 'Redo', 'icon': 'redo'},
    ]},
]


def test_menu_bar_renders(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    serve_component(page, widget)

    buttons = page.locator('.MuiButton-root')
    expect(buttons).to_have_count(2)
    expect(buttons.nth(0)).to_have_text('File')
    expect(buttons.nth(1)).to_have_text('Edit')


def test_menu_bar_open_menu(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    menu_items = page.locator('.MuiMenuItem-root')
    expect(menu_items).to_have_count(3)


def test_menu_bar_click_item(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()
    page.locator('.MuiMenuItem-root').nth(0).click()

    wait_until(lambda: widget.active == (0, 0), page)
    assert widget.value == {'label': 'New', 'icon': 'note_add', 'hint': 'Ctrl+N'}


def test_menu_bar_click_callback(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    events = []
    widget.on_click(events.append)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(1).click()
    page.locator('.MuiMenuItem-root').nth(0).click()

    wait_until(lambda: len(events) == 1, page)
    assert events[0]['label'] == 'Undo'


def test_menu_bar_divider(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    expect(page.locator('.MuiDivider-root')).to_have_count(1)


def test_menu_bar_hint(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    hint = page.locator('.MuiMenuItem-root').nth(0).locator('p.MuiTypography-body2')
    expect(hint).to_have_text('Ctrl+N')


def test_menu_bar_icons(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    icons = page.locator('.MuiMenuItem-root .material-icons')
    expect(icons.nth(0)).to_have_text('note_add')
    expect(icons.nth(1)).to_have_text('folder_open')


def test_menu_bar_submenu(page):
    items = [
        {'label': 'File', 'items': [
            {'label': 'Open Recent', 'icon': 'history', 'items': [
                {'label': 'project.py'},
                {'label': 'analysis.ipynb'},
            ]},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()
    page.locator('.MuiMenuItem-root').nth(0).click()

    submenu_items = page.locator('.MuiMenuItem-root')
    expect(submenu_items).to_have_count(3)


def test_menu_bar_submenu_click(page):
    items = [
        {'label': 'File', 'items': [
            {'label': 'Open Recent', 'icon': 'history', 'items': [
                {'label': 'project.py'},
                {'label': 'analysis.ipynb'},
            ]},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()
    page.locator('.MuiMenuItem-root').nth(0).click()

    page.locator('.MuiMenuItem-root').filter(has_text='analysis.ipynb').click()

    wait_until(lambda: widget.active == (0, 0, 1), page)
    assert widget.value == {'label': 'analysis.ipynb'}


def test_menu_bar_checkbox(page):
    items = [
        {'label': 'View', 'items': [
            {'label': 'Show Toolbar', 'checkbox': True},
            {'label': 'Show Sidebar', 'checkbox': False},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    checkboxes = page.locator('.MuiCheckbox-root')
    expect(checkboxes).to_have_count(2)
    expect(checkboxes.nth(0).locator('input')).to_be_checked()
    expect(checkboxes.nth(1).locator('input')).not_to_be_checked()


def test_menu_bar_checkbox_toggle(page):
    items = [
        {'label': 'View', 'items': [
            {'label': 'Show Toolbar', 'checkbox': True},
            {'label': 'Show Sidebar', 'checkbox': False},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()
    page.locator('.MuiMenuItem-root').nth(1).click()

    wait_until(lambda: widget.items[0]['items'][1]['checkbox'] is True, page)


def test_menu_bar_radio(page):
    items = [
        {'label': 'Theme', 'items': [
            {'label': 'Light', 'radio': 'light', '_radio_selected': True},
            {'label': 'Dark', 'radio': 'dark'},
            {'label': 'System', 'radio': 'system'},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    radios = page.locator('.MuiRadio-root')
    expect(radios).to_have_count(3)
    expect(radios.nth(0).locator('input')).to_be_checked()
    expect(radios.nth(1).locator('input')).not_to_be_checked()


def test_menu_bar_radio_select(page):
    items = [
        {'label': 'Theme', 'items': [
            {'label': 'Light', 'radio': 'light', '_radio_selected': True},
            {'label': 'Dark', 'radio': 'dark'},
            {'label': 'System', 'radio': 'system'},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()
    page.locator('.MuiMenuItem-root').nth(1).click()

    wait_until(lambda: widget.items[0]['items'][1].get('_radio_selected') is True, page)
    assert widget.items[0]['items'][0].get('_radio_selected') is False


def test_menu_bar_group(page):
    items = [
        {'label': 'Format', 'items': [
            {'label': 'Text', 'group': True, 'items': [
                {'label': 'Bold', 'icon': 'format_bold'},
                {'label': 'Italic', 'icon': 'format_italic'},
            ]},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    expect(page.locator('.MuiListSubheader-root')).to_have_count(1)
    expect(page.locator('.MuiListSubheader-root')).to_have_text('Text')
    expect(page.locator('.MuiMenuItem-root')).to_have_count(2)


def test_menu_bar_disabled_menu(page):
    items = [
        {'label': 'File', 'items': [{'label': 'New'}]},
        {'label': 'Edit', 'disabled': True, 'items': [{'label': 'Undo'}]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    buttons = page.locator('.MuiButton-root')
    expect(buttons.nth(1)).to_be_disabled()


def test_menu_bar_disabled_item(page):
    items = [
        {'label': 'File', 'items': [
            {'label': 'New'},
            {'label': 'Save', 'disabled': True},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()

    expect(page.locator('.MuiMenuItem-root.Mui-disabled')).to_have_count(1)


def test_menu_bar_color(page):
    widget = MenuBar(items=_BASIC_ITEMS, color='primary')
    serve_component(page, widget)

    buttons = page.locator('.MuiButton-root.MuiButton-colorPrimary')
    expect(buttons).to_have_count(2)


def test_menu_bar_variant_outlined(page):
    widget = MenuBar(items=_BASIC_ITEMS, variant='outlined')
    serve_component(page, widget)

    paper = page.locator('.MuiPaper-outlined')
    expect(paper).to_have_count(1)


def test_menu_bar_closes_on_item_click(page):
    widget = MenuBar(items=_BASIC_ITEMS)
    serve_component(page, widget)

    page.locator('.MuiButton-root').nth(0).click()
    expect(page.locator('.MuiMenuItem-root')).to_have_count(3)

    page.locator('.MuiMenuItem-root').nth(0).click()

    wait_until(lambda: widget.value is not None, page)
    expect(page.locator('.MuiMenuItem-root')).to_have_count(0)


def test_menu_bar_top_level_icon(page):
    items = [
        {'label': 'File', 'icon': 'description', 'items': [
            {'label': 'New'},
        ]},
    ]
    widget = MenuBar(items=items)
    serve_component(page, widget)

    icon = page.locator('.MuiButton-root .material-icons')
    expect(icon).to_have_text('description')
