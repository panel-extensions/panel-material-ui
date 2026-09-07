import os

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.widgets import FileSelector

pytestmark = pytest.mark.ui


@pytest.fixture
def test_dir(tmp_path):
    test_dir = tmp_path / 'test_dir'
    subdir1 = test_dir / 'subdir1'
    subdir2 = test_dir / 'subdir2'

    subdir1.mkdir(parents=True)
    subdir2.mkdir(parents=True)
    (subdir1 / 'a').write_text("")
    (subdir1 / 'b').write_text("")
    (test_dir / 'root.txt').write_text("")

    yield str(test_dir)


def test_file_selector_renders_listing(page, test_dir):
    widget = FileSelector(test_dir)
    serve_component(page, widget)

    expect(page.locator('.file-selector')).to_have_count(1)

    items = page.locator('.file-selector-item')
    expect(items).to_have_count(3)
    # Directories are listed before files
    expect(items.nth(0)).to_contain_text('subdir1')
    expect(items.nth(1)).to_contain_text('subdir2')
    expect(items.nth(2)).to_contain_text('root.txt')
    expect(page.locator('.file-selector-directory')).to_have_count(2)
    expect(page.locator('.file-selector-file')).to_have_count(1)


def test_file_selector_double_click_navigates(page, test_dir):
    widget = FileSelector(test_dir)
    serve_component(page, widget)

    expect(page.locator('.file-selector-item')).to_have_count(3)

    page.locator('.file-selector-item').nth(0).dblclick()

    subdir1 = os.path.join(test_dir, 'subdir1')
    wait_until(lambda: widget.directory == subdir1, page)

    items = page.locator('.file-selector-item')
    expect(items).to_have_count(3)
    expect(items.nth(0)).to_contain_text('..')
    expect(items.nth(1)).to_contain_text('a')
    expect(items.nth(2)).to_contain_text('b')

    crumbs = page.locator('.file-selector-breadcrumbs .MuiBreadcrumbs-li')
    expect(crumbs).to_have_count(2)
    expect(crumbs.nth(0)).to_have_text('test_dir')
    expect(crumbs.nth(1)).to_have_text('subdir1')


def test_file_selector_enter_button_navigates(page, test_dir):
    widget = FileSelector(test_dir)
    serve_component(page, widget)

    expect(page.locator('.file-selector-item')).to_have_count(3)

    page.locator('.file-selector-enter').nth(0).click()

    subdir1 = os.path.join(test_dir, 'subdir1')
    wait_until(lambda: widget.directory == subdir1, page)
    assert widget.value == []


def test_file_selector_check_files(page, test_dir):
    widget = FileSelector(os.path.join(test_dir, 'subdir1'), root_directory=test_dir)
    serve_component(page, widget)

    expect(page.locator('.file-selector-item')).to_have_count(3)

    a = os.path.join(test_dir, 'subdir1', 'a')
    b = os.path.join(test_dir, 'subdir1', 'b')

    page.locator('.file-selector-item').nth(1).click()
    wait_until(lambda: widget.value == [a], page)

    page.locator('.file-selector-item').nth(2).click()
    wait_until(lambda: widget.value == [a, b], page)

    expect(page.locator('.file-selector-selection')).to_contain_text('Selected (2)')

    page.locator('.file-selector-clear').click()
    wait_until(lambda: widget.value == [], page)


def test_file_selector_cannot_select_parent(page, test_dir):
    widget = FileSelector(os.path.join(test_dir, 'subdir1'), root_directory=test_dir)
    serve_component(page, widget)

    items = page.locator('.file-selector-item')
    expect(items).to_have_count(3)
    expect(items.nth(0)).to_contain_text('..')

    # The parent row has no checkbox and navigates instead of selecting
    expect(items.nth(0).locator('.MuiCheckbox-root')).to_have_count(0)

    items.nth(0).click()
    wait_until(lambda: widget.directory == test_dir, page)
    assert widget.value == []


def test_file_selector_only_files_hides_directory_checkboxes(page, test_dir):
    widget = FileSelector(test_dir, only_files=True)
    serve_component(page, widget)

    expect(page.locator('.file-selector-item')).to_have_count(3)
    expect(page.locator('.file-selector-directory .MuiCheckbox-root')).to_have_count(0)
    expect(page.locator('.file-selector-file .MuiCheckbox-root')).to_have_count(1)


def test_file_selector_up_disabled_at_root(page, test_dir):
    widget = FileSelector(test_dir)
    serve_component(page, widget)

    up = page.locator('.file-selector-up')
    expect(up).to_be_disabled()
    expect(page.locator('.file-selector-back')).to_be_disabled()
    expect(page.locator('.file-selector-forward')).to_be_disabled()

    page.locator('.file-selector-item').nth(0).dblclick()
    wait_until(lambda: widget.directory == os.path.join(test_dir, 'subdir1'), page)

    expect(up).to_be_enabled()
    expect(page.locator('.file-selector-back')).to_be_enabled()

    up.click()
    wait_until(lambda: widget.directory == test_dir, page)
    expect(up).to_be_disabled()


def test_file_selector_back_and_forward(page, test_dir):
    widget = FileSelector(test_dir)
    serve_component(page, widget)

    expect(page.locator('.file-selector-item')).to_have_count(3)
    page.locator('.file-selector-item').nth(0).dblclick()

    subdir1 = os.path.join(test_dir, 'subdir1')
    wait_until(lambda: widget.directory == subdir1, page)

    page.locator('.file-selector-back').click()
    wait_until(lambda: widget.directory == test_dir, page)

    forward = page.locator('.file-selector-forward')
    expect(forward).to_be_enabled()
    forward.click()
    wait_until(lambda: widget.directory == subdir1, page)


def test_file_selector_path_field_navigates(page, test_dir):
    widget = FileSelector(test_dir)
    serve_component(page, widget)

    subdir2 = os.path.join(test_dir, 'subdir2')
    path = page.locator('.file-selector-path input')
    expect(path).to_have_value(test_dir)

    path.fill(subdir2)
    path.press('Enter')

    wait_until(lambda: widget.directory == subdir2, page)
    expect(path).to_have_value(subdir2)


def test_file_selector_path_field_outside_root_is_refused(page, test_dir):
    widget = FileSelector(test_dir)
    serve_component(page, widget)

    path = page.locator('.file-selector-path input')
    expect(path).to_have_value(test_dir)

    path.fill(os.path.dirname(test_dir))
    path.press('Enter')

    # The rejected path is replaced with the current directory
    expect(path).to_have_value(test_dir)
    assert widget.directory == test_dir


def test_file_selector_breadcrumb_navigates(page, test_dir):
    widget = FileSelector(os.path.join(test_dir, 'subdir1'), root_directory=test_dir)
    serve_component(page, widget)

    crumbs = page.locator('.file-selector-breadcrumbs .MuiBreadcrumbs-li')
    expect(crumbs).to_have_count(2)

    crumbs.nth(0).click()
    wait_until(lambda: widget.directory == test_dir, page)


def test_file_selector_size_bounds_list_height(page, test_dir):
    widget = FileSelector(test_dir, size=1)
    serve_component(page, widget)

    items = page.locator('.file-selector-items')
    expect(items).to_have_count(1)
    wait_until(lambda: items.bounding_box()['height'] < 60, page)
    assert items.evaluate('el => el.scrollHeight > el.clientHeight')
