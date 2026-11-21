import re

import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.pane import Markdown
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Dialog
from panel_material_ui.widgets import Button
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

def test_dialog_basic(page):
    content = Column("Dialog Content")
    widget = Dialog(
        title="Test Dialog",
        objects=[content],
        open=True
    )
    serve_component(page, widget)

    # Check dialog structure
    dialog = page.locator('.MuiDialog-root')
    expect(dialog).to_have_count(1)

    # Check title
    title = page.locator('.MuiDialogTitle-root')
    expect(title).to_contain_text("Test Dialog")

    # Check content
    content = page.locator('.MuiDialogContent-root')
    expect(content).to_contain_text("Dialog Content")

def test_dialog_visibility(page):
    content = Column("Dialog Content")
    widget = Dialog(
        title="Test Dialog",
        objects=[content],
        open=False
    )
    serve_component(page, widget)

    # Initially not visible
    dialog = page.locator('.MuiDialog-root')
    expect(dialog).to_have_count(0)

    # Show dialog
    widget.open = True
    expect(dialog).to_have_count(1)

def test_dialog_full_screen(page):
    content = Column("Dialog Content")
    widget = Dialog(
        title="Test Dialog",
        objects=[content],
        open=True,
        full_screen=True
    )
    serve_component(page, widget)

    dialog_paper = page.locator('.MuiDialog-paperFullScreen')
    expect(dialog_paper).to_have_count(1)

def test_dialog_nested_components(page):
    button = Button(label="Click Me")
    widget = Dialog(
        title="Test Dialog",
        objects=[button],
        open=True
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.click('button')
    wait_until(lambda: button.clicks == 1, page)

def test_dialog_multiple_objects(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Dialog(
        title="Test Dialog",
        objects=[content1, content2],
        open=True
    )
    serve_component(page, widget)

    content = page.locator('.MuiDialogContent-root')
    expect(content).to_contain_text("Content 1")
    expect(content).to_contain_text("Content 2")

def test_dialog_scroll_paper(page):
    # Create content that would cause scrolling
    long_content = Column("<br>".join(["Content"] * 50))
    widget = Dialog(
        title="Test Dialog",
        objects=[long_content],
        open=True
    )
    serve_component(page, widget)

    dialog = page.locator('.MuiDialog-scrollPaper')
    expect(dialog).to_have_count(1)

def test_dialog_scroll_body(page):
    long_content = Column("<br>".join(["Content"] * 50))
    widget = Dialog(
        title="Test Dialog",
        objects=[long_content],
        open=True,
        scroll="body"
    )
    serve_component(page, widget)

    dialog = page.locator('.MuiDialog-scrollBody')
    expect(dialog).to_have_count(1)

@pytest.mark.parametrize('max_width', ['xs', 'sm', 'md', 'lg', 'xl'])
def test_dialog_max_width(page, max_width):
    content = Column("Dialog Content")
    widget = Dialog(
        title="Test Dialog",
        objects=[content],
        open=True,
        width_option=max_width
    )
    serve_component(page, widget)

    dialog_paper = page.locator(f'.MuiDialog-paperWidth{max_width.capitalize()}')
    expect(dialog_paper).to_have_count(1)

def test_dialog_custom_styling(page):
    content = Column("Dialog Content")
    widget = Dialog(
        title="Test Dialog",
        objects=[content],
        open=True,
        sx={'backgroundColor': 'rgb(0, 0, 255)'}
    )
    serve_component(page, widget)

    dialog = page.locator('.MuiDialog-root')
    expect(dialog).to_have_css('background-color', 'rgb(0, 0, 255)')

def test_dialog_actions_footer(page):
    cancel = Button(label="Cancel", variant="text")
    save = Button(label="Save")
    widget = Dialog("Dialog Content", title="Test Dialog", actions=[cancel, save], open=True)
    serve_component(page, widget)

    actions = page.locator('.MuiDialogActions-root')
    expect(actions).to_have_count(1)
    expect(actions).to_contain_text("Cancel")
    expect(actions).to_contain_text("Save")
    expect(page.locator('.MuiDialogContent-root')).not_to_contain_text("Save")

    save_box = actions.locator('button', has_text="Save").bounding_box()
    cancel_box = actions.locator('button', has_text="Cancel").bounding_box()
    paper_box = page.locator('.MuiDialog-paper').bounding_box()
    assert cancel_box['x'] < save_box['x']
    assert abs(paper_box['x'] + paper_box['width'] - (save_box['x'] + save_box['width']) - 20) <= 1

    actions.locator('button', has_text="Save").click()
    wait_until(lambda: save.clicks == 1, page)

def test_dialog_no_actions_footer_by_default(page):
    widget = Dialog("Dialog Content", title="Test Dialog", open=True)
    serve_component(page, widget)

    expect(page.locator('.MuiDialogContent-root')).to_have_count(1)
    expect(page.locator('.MuiDialogActions-root')).to_have_count(0)

def test_dialog_actions_stay_visible_when_scrolling(page):
    long_content = Column("<br>".join(["Content"] * 100))
    widget = Dialog(long_content, title="Test Dialog", actions=[Button(label="OK")], open=True)
    serve_component(page, widget)

    actions = page.locator('.MuiDialogActions-root')
    expect(actions).to_be_in_viewport()
    expect(actions).to_have_css('border-top-width', '1px')

def test_dialog_no_dividers_without_overflow(page):
    widget = Dialog("Short content", title="Test Dialog", actions=[Button(label="OK")], open=True)
    serve_component(page, widget)

    expect(page.locator('.MuiDialogActions-root')).to_have_css('border-top-width', '0px')

def test_dialog_close_button_aligned_with_title(page):
    widget = Dialog("Dialog Content", title="Test Dialog", show_close_button=True, open=True)
    serve_component(page, widget)

    title_box = page.locator('.MuiDialogTitle-root').bounding_box()
    close = page.locator('button[aria-label="close"]')
    close_box = close.bounding_box()
    title_center = title_box['y'] + title_box['height'] / 2
    close_center = close_box['y'] + close_box['height'] / 2
    assert abs(title_center - close_center) <= 2
    paper_box = page.locator('.MuiDialog-paper').bounding_box()
    assert abs(paper_box['x'] + paper_box['width'] - (close_box['x'] + close_box['width']) - 8) <= 1

    close.click()
    expect(page.locator('.MuiDialog-root')).to_have_count(0)
    wait_until(lambda: widget.open is False, page)

def test_dialog_title_variant_default(page):
    widget = Dialog("Dialog Content", title="Test Dialog", open=True)
    serve_component(page, widget)

    expect(page.locator('.MuiDialogTitle-root')).to_have_class(re.compile('MuiTypography-h5'))

def test_dialog_escape_closes(page):
    widget = Dialog("Dialog Content", title="Test Dialog", open=True)
    serve_component(page, widget)

    expect(page.locator('.MuiDialog-paper')).to_have_count(1)
    page.keyboard.press("Escape")
    expect(page.locator('.MuiDialog-root')).to_have_count(0)
    wait_until(lambda: widget.open is False, page)

def test_dialog_escape_disabled(page):
    widget = Dialog("Dialog Content", title="Test Dialog", close_on_escape=False, open=True)
    serve_component(page, widget)

    expect(page.locator('.MuiDialog-paper')).to_have_count(1)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    expect(page.locator('.MuiDialog-paper')).to_have_count(1)
    assert widget.open is True

def test_dialog_backdrop_click(page):
    widget = Dialog("Dialog Content", title="Test Dialog", open=True)
    serve_component(page, widget)

    page.mouse.click(5, 5)
    page.wait_for_timeout(300)
    expect(page.locator('.MuiDialog-paper')).to_have_count(1)

    widget.close_on_click = True
    page.mouse.click(5, 5)
    expect(page.locator('.MuiDialog-root')).to_have_count(0)
    wait_until(lambda: widget.open is False, page)

def test_dialog_min_width(page):
    widget = Dialog("Hi", title="T", open=True)
    serve_component(page, widget)

    assert page.locator('.MuiDialog-paper').bounding_box()['width'] >= 360

def test_dialog_small_screen_margins(page):
    page.set_viewport_size({"width": 390, "height": 760})
    widget = Dialog("Dialog Content", title="Test Dialog", open=True)
    serve_component(page, widget)

    box = page.locator('.MuiDialog-paper').bounding_box()
    assert box['x'] == 16
    assert box['width'] == 390 - 32

def test_dialog_title_aligned_with_content(page):
    # Panel children carry a 10px horizontal margin, so with the content's
    # 10px padding their text lines up with the title's 20px inset.
    widget = Dialog(Markdown("Dialog Content"), title="Test Dialog", open=True)
    serve_component(page, widget)

    title_x = page.locator('.MuiDialogTitle-root').evaluate(
        "e => { const r = document.createRange(); r.selectNodeContents(e); return r.getBoundingClientRect().x }"
    )
    content_x = page.locator('.MuiDialogContent-root p').bounding_box()['x']
    paper_x = page.locator('.MuiDialog-paper').bounding_box()['x']
    assert abs(title_x - paper_x - 20) <= 1
    assert abs(content_x - paper_x - 20) <= 1

def test_dialog_dividers_follow_swapped_objects(page):
    # Full screen fixes the content's size, so only the children's own
    # resizes reveal that it starts to overflow.
    small = Column("Short", height=50)
    widget = Dialog(small, title="Test Dialog", actions=[Button(label="OK")], full_screen=True, open=True)
    serve_component(page, widget)

    actions = page.locator('.MuiDialogActions-root')
    expect(actions).to_have_css('border-top-width', '0px')

    replacement = Column("Replacement", height=50)
    widget.objects = [replacement]
    expect(page.locator('.MuiDialogContent-root')).to_contain_text("Replacement")
    expect(actions).to_have_css('border-top-width', '0px')

    replacement.height = 3000
    expect(actions).to_have_css('border-top-width', '1px')
