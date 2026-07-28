import io

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component
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
