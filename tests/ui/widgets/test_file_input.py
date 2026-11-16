import sys
from pathlib import Path

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import Error, expect

from panel_material_ui.widgets import FileInput

pytestmark = pytest.mark.ui

def test_fileinput(page):
    widget = FileInput(accept='.png,.jpeg', multiple=True)
    serve_component(page, widget)
    expect(page.locator('.file-input')).to_have_count(1)

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

def test_fileinput_focus(page):
    widget = FileInput()
    serve_component(page, widget)
    file_input = page.locator('input[type="file"]')
    expect(file_input).to_have_count(1)
    widget.focus()
    expect(file_input).to_be_focused()


def test_fileinput_max_total_file_size_counts_each_file_once(page):
    widget = FileInput(max_total_file_size=100)
    serve_component(page, widget)
    page.set_input_files('input[type="file"]', files=[
        {'name': 'a.txt', 'mimeType': 'text/plain', 'buffer': b'x' * 60}
    ])
    wait_until(lambda: widget.value == b'x' * 60, page)
    assert widget.filename == 'a.txt'


def test_fileinput_max_total_file_size_rejects_batch(page):
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    widget = FileInput(max_total_file_size=100, multiple=True)
    serve_component(page, widget)
    page.set_input_files('input[type="file"]', files=[
        {'name': 'a.txt', 'mimeType': 'text/plain', 'buffer': b'x' * 60},
        {'name': 'b.txt', 'mimeType': 'text/plain', 'buffer': b'y' * 60},
    ])
    expect(page.locator('.MuiSvgIcon-colorError')).to_have_count(1)
    assert widget.value is None
    assert widget._buffer == []
    assert widget._file_buffer == {}

    # A valid upload after the rejected one still works
    page.set_input_files('input[type="file"]', files=[
        {'name': 'c.txt', 'mimeType': 'text/plain', 'buffer': b'z' * 10},
    ])
    wait_until(lambda: widget.value == [b'z' * 10], page)


def test_fileinput_empty_file(page):
    widget = FileInput(multiple=True)
    serve_component(page, widget)
    page.set_input_files('input[type="file"]', files=[
        {'name': 'empty.txt', 'mimeType': 'text/plain', 'buffer': b''},
        {'name': 'b.txt', 'mimeType': 'text/plain', 'buffer': b'hi'},
    ])
    wait_until(lambda: widget.filename == ['empty.txt', 'b.txt'], page)
    assert widget.value == [b'', b'hi']
