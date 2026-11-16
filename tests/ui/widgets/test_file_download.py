import io
import re

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component
from playwright.sync_api import expect

from panel_material_ui.widgets import FileDownload

pytestmark = pytest.mark.ui


def test_file_download_auto_refetches_callback_on_every_click(page):
    counter = {'n': 0}

    def callback():
        counter['n'] += 1
        return io.StringIO(f'download #{counter["n"]}\n')

    widget = FileDownload(callback=callback, filename='f.txt', label='Download')

    serve_component(page, widget)

    button = page.locator('.MuiButton-root')
    expect_download = page.expect_download

    with expect_download() as download_info:
        button.click()
    download1 = download_info.value
    path1 = download1.path()

    with expect_download() as download_info:
        button.click()
    download2 = download_info.value
    path2 = download2.path()

    assert path1.read_bytes() == b'download #1\n'
    assert path2.read_bytes() == b'download #2\n'
    assert counter['n'] == 2


BLOB_COUNTER = """
window.__blobs = [];
window.__revoked = 0;
const create = URL.createObjectURL;
URL.createObjectURL = function(b) { window.__blobs.push((b && b.size) || 0); return create.call(URL, b) };
const revoke = URL.revokeObjectURL;
URL.revokeObjectURL = function(u) { window.__revoked++; return revoke.call(URL, u) };
"""


def test_file_download_rerender_does_not_leak_blob_urls(page):
    payload = b'x' * 100_000
    page.add_init_script(BLOB_COUNTER)
    widget = FileDownload(file=io.BytesIO(payload), filename='a.bin', embed=True, auto=False)
    serve_component(page, widget)
    expect(page.locator('.MuiButton-root a')).to_have_attribute('href', re.compile('^blob:'))

    for i in range(10):
        widget.color = 'secondary' if i % 2 == 0 else 'primary'
    expect(page.locator('.MuiButton-root.MuiButton-colorPrimary')).to_have_count(1)

    sizes = page.evaluate("window.__blobs")
    assert sizes.count(len(payload)) == 1


def test_file_download_clear_data(page):
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.add_init_script(BLOB_COUNTER)
    widget = FileDownload(file=io.BytesIO(b'abc'), filename='a.bin', embed=True, auto=False)
    serve_component(page, widget)
    link = page.locator('.MuiButton-root a')
    expect(link).to_have_attribute('href', re.compile('^blob:'))

    widget.data = None
    expect(link).not_to_have_attribute('href', re.compile('^blob:'))
    expect(page.locator('.MuiButton-root')).to_have_count(1)
    assert page.evaluate("window.__revoked") >= 1
    assert not errors
