import io

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
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


def test_file_download_auto_false_reruns_callback_on_later_clicks(page):
    counter = {'n': 0}

    def callback():
        counter['n'] += 1
        return io.StringIO(f'download #{counter["n"]}\n')

    widget = FileDownload(callback=callback, filename='f.txt', auto=False)

    serve_component(page, widget)

    button = page.locator('.MuiButton-root')

    # The first click only prepares the data
    button.click()
    wait_until(lambda: widget.data is not None, page)
    assert counter['n'] == 1

    for n in (2, 3):
        with page.expect_download() as download_info:
            button.click()
        assert download_info.value.path().read_bytes() == f'download #{n}\n'.encode()
        assert counter['n'] == n


def test_file_download_auto_false_downloads_when_callback_data_is_unchanged(page):
    widget = FileDownload(callback=lambda: io.StringIO('same'), filename='f.txt', auto=False)

    serve_component(page, widget)

    button = page.locator('.MuiButton-root')

    button.click()
    wait_until(lambda: widget.data is not None, page)

    for _ in range(2):
        with page.expect_download() as download_info:
            button.click()
        assert download_info.value.path().read_bytes() == b'same'


def test_file_download_auto_false_failed_callback_does_not_defer_download(page):
    calls = {'n': 0}

    def callback():
        calls['n'] += 1
        if calls['n'] == 2:
            raise RuntimeError('boom')
        return io.StringIO(f'download #{calls["n"]}')

    widget = FileDownload(callback=callback, filename='f.txt', auto=False)

    serve_component(page, widget, suppress_error=True)

    button = page.locator('.MuiButton-root')

    button.click()
    wait_until(lambda: widget.data is not None, page)

    button.click()
    wait_until(lambda: calls['n'] == 2, page)
    wait_until(lambda: not widget._syncing, page)

    with page.expect_download() as download_info:
        button.click()
    assert download_info.value.path().read_bytes() == b'download #3'
