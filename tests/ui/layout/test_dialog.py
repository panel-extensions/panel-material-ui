import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.widgets import Button
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Dialog
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
    button = Button(name="Click Me")
    widget = Dialog(
        title="Test Dialog",
        objects=[button],
        open=True
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.locator('button').click()
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
