import pytest

pytest.importorskip('playwright')

from panel.layout import Column, Row
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Dialog, Popup
from panel_material_ui.widgets import Button, TextInput

pytestmark = pytest.mark.ui

def test_popup_basic(page):
    content = Column("Popup Content")
    widget = Popup(
        objects=[content],
        open=True
    )
    serve_component(page, widget)

    # Check popup structure
    popup = page.locator('.MuiPopover-root')
    expect(popup).to_have_count(1)

    # Check content
    content = page.locator('.MuiPaper-root')
    expect(content).to_contain_text("Popup Content")

def test_popup_visibility(page):
    content = Column("Popup Content")
    widget = Popup(
        objects=[content],
        open=False
    )
    serve_component(page, widget)

    # Initially not visible
    popup = page.locator('.MuiPopover-root')
    expect(popup).to_have_count(0)

    # Show popup
    widget.open = True
    expect(popup).to_have_count(1)

def test_popup_nested_components(page):
    button = Button(label="Click Me")
    widget = Popup(
        objects=[button],
        open=True
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.click('button')
    wait_until(lambda: button.clicks == 1, page)

def test_popup_multiple_objects(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Popup(
        objects=[content1, content2],
        open=True
    )
    serve_component(page, widget)

    content = page.locator('.MuiPaper-root')
    expect(content).to_contain_text("Content 1")
    expect(content).to_contain_text("Content 2")


def _non_modal_popup(**params):
    trigger = Button(label="Details")
    field = TextInput(label="Name")
    apply = Button(label="Apply")
    popup = Popup(field, apply, modal=False, **params)
    trigger.on_click(lambda event: popup.param.update(open=not popup.open))
    after = Button(label="After")
    layout = Column(Row(trigger, popup), after)
    return layout, popup, after


def test_popup_modal_default_unchanged(page):
    serve_component(page, Popup("Content", open=True))

    expect(page.locator('.MuiBackdrop-root')).to_have_count(1)
    expect(page.get_by_role('dialog')).to_have_count(0)


def test_popup_modal_label_names_dialog(page):
    serve_component(page, Popup("Content", open=True, label="Settings"))

    expect(page.get_by_role('dialog', name='Settings')).to_have_count(1)


def test_popup_non_modal_opens_as_dialog(page):
    layout, popup, _ = _non_modal_popup()
    serve_component(page, layout)

    trigger = page.get_by_role('button', name='Details')
    expect(trigger).to_have_attribute('aria-haspopup', 'dialog')
    expect(trigger).to_have_attribute('aria-expanded', 'false')

    trigger.click()
    wait_until(lambda: popup.open, page)
    dialog = page.get_by_role('dialog', name='Details')
    expect(dialog).to_have_attribute('aria-modal', 'false')
    expect(dialog).to_be_focused()
    expect(trigger).to_have_attribute('aria-expanded', 'true')
    expect(page.locator('.MuiBackdrop-root')).to_have_count(0)


def test_popup_non_modal_label(page):
    layout, popup, _ = _non_modal_popup(label="Edit name")
    serve_component(page, layout)

    page.get_by_role('button', name='Details').click()
    expect(page.get_by_role('dialog', name='Edit name')).to_have_count(1)


def test_popup_non_modal_escape_returns_focus(page):
    layout, popup, _ = _non_modal_popup()
    serve_component(page, layout)

    trigger = page.get_by_role('button', name='Details')
    trigger.click()
    page.get_by_role('textbox', name='Name').click()
    page.keyboard.press('Escape')

    wait_until(lambda: not popup.open, page)
    expect(trigger).to_be_focused()
    expect(trigger).to_have_attribute('aria-expanded', 'false')


def test_popup_non_modal_page_stays_usable(page):
    layout, popup, after = _non_modal_popup()
    serve_component(page, layout)

    page.get_by_role('button', name='Details').click()
    expect(page.get_by_role('dialog')).to_have_count(1)

    page.get_by_role('button', name='After').click()
    wait_until(lambda: after.clicks == 1, page)
    wait_until(lambda: not popup.open, page)
    expect(page.get_by_role('button', name='After')).to_be_focused()


def test_popup_non_modal_trigger_click_toggles(page):
    layout, popup, _ = _non_modal_popup()
    serve_component(page, layout)

    trigger = page.get_by_role('button', name='Details')
    trigger.click()
    wait_until(lambda: popup.open, page)
    trigger.click()
    wait_until(lambda: not popup.open, page)


def test_popup_non_modal_tab_order(page):
    layout, popup, _ = _non_modal_popup()
    serve_component(page, layout)

    trigger = page.get_by_role('button', name='Details')
    trigger.click()
    dialog = page.get_by_role('dialog')
    expect(dialog).to_be_focused()

    # Shift+Tab goes back to the trigger and leaves the popup open.
    page.keyboard.press('Shift+Tab')
    expect(trigger).to_be_focused()
    assert popup.open

    # Tab on the trigger moves into the popup rather than past it.
    page.keyboard.press('Tab')
    expect(dialog).to_be_focused()
    page.keyboard.press('Tab')
    expect(page.get_by_role('textbox', name='Name')).to_be_focused()
    page.keyboard.press('Tab')
    expect(page.get_by_role('button', name='Apply')).to_be_focused()

    # Tab past the end closes the popup and returns to the trigger.
    page.keyboard.press('Tab')
    wait_until(lambda: not popup.open, page)
    expect(trigger).to_be_focused()


def test_popup_non_modal_focus_elsewhere_closes(page):
    layout, popup, after = _non_modal_popup()
    serve_component(page, layout)

    page.get_by_role('button', name='Details').click()
    expect(page.get_by_role('dialog')).to_be_focused()
    after.focus()

    wait_until(lambda: not popup.open, page)
    expect(page.get_by_role('button', name='After')).to_be_focused()


def test_popup_non_modal_stays_open_under_a_dialog(page):
    trigger = Button(label="Details")
    cancel = Button(label="Cancel")
    dialog = Dialog(cancel, title="Confirm")
    delete = Button(label="Delete")
    popup = Popup(delete, dialog, modal=False)
    trigger.on_click(lambda event: popup.param.update(open=not popup.open))
    delete.on_click(lambda event: dialog.param.update(open=True))
    cancel.on_click(lambda event: dialog.param.update(open=False))
    serve_component(page, Column(Row(trigger, popup)))

    page.get_by_role('button', name='Details').click()
    page.get_by_role('button', name='Delete').click()
    wait_until(lambda: dialog.open, page)
    page.get_by_role('button', name='Cancel').click()
    wait_until(lambda: not dialog.open, page)
    expect(page.locator('.MuiDialog-root')).to_have_count(0)

    assert popup.open
    expect(page.get_by_role('dialog', name='Details')).to_be_visible()
    wait_until(lambda: page.evaluate("""() => {
        let el = document.activeElement
        while (el && el.shadowRoot && el.shadowRoot.activeElement) { el = el.shadowRoot.activeElement }
        return el != null && el !== document.body
    }"""), page)
    page.keyboard.press('Escape')
    wait_until(lambda: not popup.open, page)
    expect(page.get_by_role('button', name='Details')).to_be_focused()
