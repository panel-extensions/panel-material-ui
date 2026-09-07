import os
from pathlib import Path

import pytest

from panel_material_ui.widgets import FileSelector


@pytest.fixture
def test_dir(tmp_path):
    test_dir = tmp_path / 'test_dir'
    subdir1 = test_dir / 'subdir1'
    subdir2 = test_dir / 'subdir2'
    a = subdir1 / "a"
    b = subdir1 / "b"

    subdir1.mkdir(parents=True)
    subdir2.mkdir(parents=True)
    a.write_text("")
    b.write_text("")

    yield str(test_dir)


@pytest.fixture
def fs():
    pytest.importorskip("fsspec")
    from fsspec.implementations.local import LocalFileSystem
    return LocalFileSystem()


@pytest.fixture
def memory_fs():
    pytest.importorskip("fsspec")
    import fsspec
    fs = fsspec.filesystem('memory')
    fs.store.clear()
    fs.pseudo_dirs.clear()
    fs.pseudo_dirs.append('')
    fs.mkdirs('/datasets/sub', exist_ok=True)
    fs.mkdirs('/other', exist_ok=True)
    with fs.open('/datasets/a.csv', 'wb') as f:
        f.write(b'a,b')
    with fs.open('/datasets/sub/b.csv', 'wb') as f:
        f.write(b'c,d')
    return fs


def names(selector):
    return [item['name'] for item in selector._items]


def paths(selector):
    return [item['path'] for item in selector._items]


def test_private_panel_imports_resolve():
    # The FileSelector reuses Panel's private file provider layer, so a
    # rename upstream should fail loudly here rather than at render time.
    from panel.widgets.file_selector import (  # noqa: F401
        BaseFileProvider,
        BaseFileSelector,
        LocalFileProvider,
        RemoteFileProvider,
        _scan_path,
    )


def test_file_selector_init(test_dir):
    selector = FileSelector(test_dir)

    assert selector.directory == test_dir
    assert selector.root_directory == test_dir
    assert selector._items == [
        {'name': 'subdir1', 'path': os.path.join(test_dir, 'subdir1'), 'type': 'directory'},
        {'name': 'subdir2', 'path': os.path.join(test_dir, 'subdir2'), 'type': 'directory'},
    ]
    assert selector._crumbs == [{'name': 'test_dir', 'path': test_dir}]
    assert not selector._can_back
    assert not selector._can_forward
    assert not selector._can_up


def test_file_selector_root_directory_defaults_to_directory(tmp_path):
    selector = FileSelector(str(tmp_path / 'test_dir'), root_directory=str(tmp_path))

    assert selector.root_directory == str(tmp_path)


def test_file_selector_address_bar(test_dir):
    selector = FileSelector(test_dir)

    subdir1 = os.path.join(test_dir, 'subdir1')
    selector._process_events({'directory': subdir1})

    assert selector.directory == subdir1
    assert selector._cwd == subdir1
    assert selector._can_back
    assert not selector._can_forward
    assert selector._can_up
    assert selector._items[0] == {
        'name': '..', 'path': test_dir, 'type': 'directory', 'parent': True
    }
    assert names(selector) == ['..', 'a', 'b']
    assert selector._crumbs == [
        {'name': 'test_dir', 'path': test_dir},
        {'name': 'subdir1', 'path': subdir1},
    ]


def test_file_selector_back_and_forward(test_dir):
    selector = FileSelector(test_dir)

    subdir1 = os.path.join(test_dir, 'subdir1')
    selector.directory = subdir1

    assert selector._cwd == subdir1
    assert selector._can_back
    assert not selector._can_forward

    selector._handle_msg({'type': 'back'})

    assert selector._cwd == test_dir
    assert selector.directory == test_dir
    assert not selector._can_back
    assert selector._can_forward

    selector._handle_msg({'type': 'forward'})

    assert selector._cwd == subdir1
    assert selector._can_back
    assert not selector._can_forward


def test_file_selector_up(test_dir):
    selector = FileSelector(test_dir, root_directory=os.path.dirname(test_dir))

    subdir1 = os.path.join(test_dir, 'subdir1')
    selector.directory = subdir1

    assert selector._cwd == subdir1

    selector._handle_msg({'type': 'up'})

    assert selector._cwd == test_dir

    selector._handle_msg({'type': 'up'})

    assert selector._cwd == os.path.dirname(test_dir)
    assert not selector._can_up


def test_file_selector_up_disabled_at_root(test_dir):
    selector = FileSelector(test_dir)

    assert not selector._can_up

    selector._handle_msg({'type': 'up'})

    assert selector._cwd == test_dir


def test_file_selector_reload_picks_up_new_files(test_dir):
    selector = FileSelector(test_dir)

    assert names(selector) == ['subdir1', 'subdir2']

    Path(test_dir, 'c').write_text("")
    selector._handle_msg({'type': 'reload'})

    assert names(selector) == ['subdir1', 'subdir2', 'c']


def test_file_selector_select_files(test_dir):
    selector = FileSelector(test_dir)

    subdir1 = os.path.join(test_dir, 'subdir1')
    selector.directory = subdir1

    a, b = os.path.join(subdir1, 'a'), os.path.join(subdir1, 'b')
    selector._process_events({'value': [a]})

    assert selector.value == [a]

    selector._process_events({'value': [a, b]})

    assert selector.value == [a, b]

    selector._process_events({'value': []})

    assert selector.value == []


def test_file_selector_multiple_across_dirs(test_dir):
    selector = FileSelector(test_dir)

    subdir2 = os.path.join(test_dir, 'subdir2')
    selector._process_events({'value': [subdir2]})

    assert selector.value == [subdir2]

    subdir1 = os.path.join(test_dir, 'subdir1')
    selector.directory = subdir1

    a = os.path.join(subdir1, 'a')
    selector._process_events({'value': [subdir2, a]})

    assert selector.value == [subdir2, a]

    selector._process_events({'value': [a]})

    assert selector.value == [a]


def test_file_selector_cannot_select_parent(test_dir):
    selector = FileSelector(test_dir)

    subdir1 = os.path.join(test_dir, 'subdir1')
    selector.directory = subdir1

    selector._process_events({'value': [test_dir]})

    assert selector.value == []


def test_file_selector_value_not_in_listing_is_dropped(test_dir):
    selector = FileSelector(test_dir)

    selector._process_events({'value': [os.path.join(test_dir, 'subdir1', 'a')]})

    assert selector.value == []


def test_file_selector_only_files(test_dir):
    selector = FileSelector(test_dir, only_files=True)

    selector._process_events({'value': [os.path.join(test_dir, 'subdir1')]})

    assert selector.value == []
    assert names(selector) == ['subdir1', 'subdir2']


def test_file_selector_only_files_filters_existing_value(test_dir):
    selector = FileSelector(test_dir)

    subdir1 = os.path.join(test_dir, 'subdir1')
    selector._process_events({'value': [subdir1]})

    assert selector.value == [subdir1]

    selector.only_files = True

    assert selector.value == []


def test_file_selector_file_pattern(test_dir):
    selector = FileSelector(test_dir, file_pattern='a')

    selector.directory = os.path.join(test_dir, 'subdir1')

    assert names(selector) == ['..', 'a']


def test_file_selector_file_pattern_update(test_dir):
    selector = FileSelector(os.path.join(test_dir, 'subdir1'))

    assert names(selector) == ['a', 'b']

    selector.file_pattern = 'b'

    assert names(selector) == ['b']


def test_file_selector_show_hidden(test_dir):
    Path(test_dir, '.hidden').write_text("")

    selector = FileSelector(test_dir)

    assert names(selector) == ['subdir1', 'subdir2']

    selector.show_hidden = True

    assert names(selector) == ['subdir1', 'subdir2', '.hidden']


def test_file_selector_file_size_and_modified(test_dir):
    Path(test_dir, 'subdir1', 'b').write_text("hello")

    selector = FileSelector(os.path.join(test_dir, 'subdir1'))

    a, b = selector._items
    assert a['size'] == 0
    assert b['size'] == 5
    assert 'modified' in a and 'modified' in b


def test_file_selector_navigation_above_root_is_refused(test_dir):
    selector = FileSelector(test_dir)

    selector._process_events({'directory': os.path.dirname(test_dir)})

    assert selector.directory == test_dir
    assert selector._cwd == test_dir


def test_file_selector_root_prefix_sibling_is_refused(tmp_path):
    root = tmp_path / 'data'
    sibling = tmp_path / 'data-private'
    root.mkdir()
    sibling.mkdir()

    selector = FileSelector(str(root))
    selector._process_events({'directory': str(sibling)})

    assert selector.directory == str(root)


def test_file_selector_symlink_escaping_root_is_refused(tmp_path):
    root = tmp_path / 'root'
    outside = tmp_path / 'outside'
    root.mkdir()
    outside.mkdir()
    link = root / 'escape'
    try:
        link.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are not supported on this platform")

    selector = FileSelector(str(root))
    selector._process_events({'directory': str(link)})

    assert selector.directory == str(root)


def test_file_selector_invalid_directory_is_refused(test_dir):
    selector = FileSelector(test_dir)

    selector._process_events({'directory': os.path.join(test_dir, 'nonexistent')})

    assert selector.directory == test_dir
    assert names(selector) == ['subdir1', 'subdir2']


def test_file_selector_refresh_period(test_dir):
    selector = FileSelector(test_dir)

    assert not selector._periodic.running

    selector.refresh_period = 1000

    assert selector._periodic.running
    assert selector._periodic.period == 1000

    selector.refresh_period = None

    assert not selector._periodic.running


def test_file_selector_remote_provider(fs, test_dir):
    selector = FileSelector(test_dir, fs=fs)

    assert selector.fs is fs
    assert names(selector) == ['subdir1', 'subdir2']
    assert paths(selector) == [
        os.path.join(test_dir, 'subdir1').replace(os.sep, '/'),
        os.path.join(test_dir, 'subdir2').replace(os.sep, '/'),
    ]

    selector.directory = os.path.join(test_dir, 'subdir1')

    assert names(selector) == ['..', 'a', 'b']


def test_file_selector_remote_provider_root_confinement(fs, test_dir):
    selector = FileSelector(test_dir, fs=fs)

    selector._process_events({'directory': os.path.dirname(test_dir)})

    assert selector.directory == test_dir


def test_file_selector_remote_scheme_is_not_normalized_locally(fs):
    # Panel's BaseFileSelector.__init__ runs in the cooperative super()
    # chain with a LocalFileProvider, which would resolve 's3://datasets'
    # against the current working directory.
    selector = FileSelector('s3://datasets', fs=fs)

    assert selector.directory == 's3://datasets'
    assert selector.root_directory == 's3://datasets'


def test_file_selector_remote_paths_are_canonical(memory_fs):
    selector = FileSelector('memory://datasets', fs=memory_fs)

    assert selector.directory == 'memory://datasets'
    # RemoteFileProvider.ls returns 'memory:///datasets/sub' here because
    # MemoryFileSystem lists absolute names; the extra separator has to be
    # collapsed or the paths cannot be compared to the directory.
    assert selector._items == [
        {'name': 'sub', 'path': 'memory://datasets/sub', 'type': 'directory'},
        {'name': 'a.csv', 'path': 'memory://datasets/a.csv', 'type': 'file'},
    ]


def test_file_selector_remote_navigation_round_trip(memory_fs):
    selector = FileSelector('memory://datasets', fs=memory_fs)

    # Navigate using the path the frontend was handed
    selector._process_events({'directory': selector._items[0]['path']})

    assert selector.directory == 'memory://datasets/sub'
    assert selector._can_up
    assert names(selector) == ['..', 'b.csv']
    assert selector._crumbs == [
        {'name': 'datasets', 'path': 'memory://datasets'},
        {'name': 'sub', 'path': 'memory://datasets/sub'},
    ]

    selector._process_events({'value': [selector._items[1]['path']]})

    assert selector.value == ['memory://datasets/sub/b.csv']

    selector._handle_msg({'type': 'up'})

    assert selector.directory == 'memory://datasets'


def test_file_selector_remote_navigation_above_root_is_refused(memory_fs):
    selector = FileSelector('memory://datasets', fs=memory_fs)

    selector._process_events({'directory': 'memory://other'})

    assert selector.directory == 'memory://datasets'


def test_file_selector_model_properties(test_dir, document, comm):
    selector = FileSelector(test_dir)

    model = selector.get_root(document, comm=comm)

    assert model.data.directory == test_dir
    assert len(model.data._items) == 2
    assert model.data.size == 10
    # Provider only parameters are kept off the wire
    for prop in ('file_pattern', 'refresh_period', 'root_directory', 'show_hidden'):
        assert prop not in model.data.properties()
