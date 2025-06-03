import sys
from pathlib import Path

import pytest

pytest.importorskip('playwright')

from playwright.sync_api import Error, expect
from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import FileInput

pytestmark = pytest.mark.ui


def test_fileinput_text_file(page):
    widget = FileInput()
    serve_component(page, widget)

    file = Path(__file__)

    page.set_input_files('input[type="file"]', file)

    wait_until(lambda: isinstance(widget.value, bytes), page)
    data = file.read_text()
    if sys.platform == 'win32':
        data = data.replace("\n", "\r\n")
    assert widget.value.decode('utf-8') == data

def test_fileinput_wrong_filetype_error(page):
    widget = FileInput(accept=".png")
    serve_component(page, widget)

    page.set_input_files('input[type="file"]', __file__)

    error_icon = page.locator('.MuiSvgIcon-colorError')
    expect(error_icon).to_have_count(1)
    error_icon.hover()
    tooltip = page.locator('.MuiTooltip-popper')
    expect(tooltip).to_have_text('The file(s) test_file_input.py have invalid file types. Accepted types: .png')

def test_fileinput_multiple_file_error(page):
    widget = FileInput()
    serve_component(page, widget)

    msg = "Non-multiple file input can only accept single file"
    with pytest.raises(Error, match=msg):
        page.set_input_files('input[type="file"]', [__file__, __file__])

def test_fileinput_multiple_files(page):
    widget = FileInput(multiple=True)
    serve_component(page, widget)

    file1 = Path(__file__)
    file2 = file1.parent / 'test_input.py'

    page.set_input_files('input[type="file"]', [file1, file2])
    data1 = file1.read_text()
    data2 = file2.read_text()
    if sys.platform == 'win32':
        data1 = data1.replace("\n", "\r\n")
        data2 = data2.replace("\n", "\r\n")

    wait_until(lambda: isinstance(widget.value, list), page)
    assert [v.decode('utf-8') for v in widget.value] == [data1, data2]
