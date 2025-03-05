import numpy as np
import pytest

from pathlib import Path
from panel import config

from panel_material_ui.widgets import FileInput, IntInput, FloatInput



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


@pytest.mark.xfail(reason='')
def test_int_input(document, comm):
    int_input = IntInput(name='Int input')
    widget = int_input.get_root(document, comm=comm)

    assert widget.name == 'Int input'
    assert widget.step == 1
    assert widget.value == 0

    int_input._process_events({'value': 2})
    assert int_input.value == 2
    int_input._process_events({'value_throttled': 2})
    assert int_input.value_throttled == 2

    int_input.value = 0
    assert widget.value == 0

    # Testing throttled mode
    with config.set(throttled=True):
        int_input._process_events({'value': 1})
        assert int_input.value == 0  # no change
        int_input._process_events({'value_throttled': 1})
        assert int_input.value == 1

        int_input.value = 2
        assert widget.value == 2


@pytest.mark.xfail(reason='')
def test_float_input(document, comm):
    float_input = FloatInput(value=0.4, name="Float input")
    widget = float_input.get_root(document, comm=comm)

    assert widget.name == 'Float input'
    assert widget.step == 0.1
    assert widget.value == 0.4

    float_input._process_events({'value': 0.2})
    assert float_input.value == 0.2
    float_input._process_events({'value_throttled': 0.2})
    assert float_input.value_throttled == 0.2

    float_input.value = 0.3
    assert widget.value == 0.3

    # Testing throttled mode
    with config.set(throttled=True):
        float_input._process_events({'value': 0.4})
        assert float_input.value == 0.3  # no change
        float_input._process_events({'value_throttled': 0.4})
        assert float_input.value == 0.4

        float_input.value = 0.5
        assert widget.value == 0.5
