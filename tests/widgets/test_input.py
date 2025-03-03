import numpy as np
import pytest

from pathlib import Path

from panel_material_ui.widgets import FileInput



def test_file_input(document, comm):
    file_input = FileInput(accept='.txt')

    widget = file_input.get_root(document, comm=comm)

    file_input._process_events({'mime_type': 'text/plain', 'value': 'U29tZSB0ZXh0Cg==', 'filename': 'testfile'})
    assert file_input.value == b'Some text\n'
    assert file_input.mime_type == 'text/plain'
    assert file_input.accept == '.txt'
    assert file_input.filename == 'testfile'


def test_file_input_save_one_file(document, comm, tmpdir):
    file_input = FileInput(accept='.txt')

    widget = file_input.get_root(document, comm=comm)

    file_input._process_events({'mime_type': 'text/plain', 'value': 'U29tZSB0ZXh0Cg==', 'filename': 'testfile'})

    fpath = Path(tmpdir) / 'out.txt'
    file_input.save(str(fpath))

    assert fpath.exists()
    content = fpath.read_text()
    assert content == 'Some text\n'
