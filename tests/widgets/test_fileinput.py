#!/usr/bin/env python3
"""
Test script for FileInput chunked upload functionality.
This script tests both legacy (small files) and chunked (large files) upload paths.
"""

import sys
import pytest

from panel_material_ui.widgets.input import FileInput

import base64
import pytest

from pathlib import Path

from panel_material_ui.widgets import FileInput
from panel_material_ui.layout import Column
from panel.pane import Markdown
from panel.widgets import Tabulator

@pytest.mark.from_panel
def test_file_input(document, comm):
    file_input = FileInput(accept='.txt')

    file_input._process_events({'mime_type': 'text/plain', 'value': 'U29tZSB0ZXh0Cg==', 'filename': 'testfile'})
    assert file_input.value == b'Some text\n'
    assert file_input.mime_type == 'text/plain'
    assert file_input.accept == '.txt'
    assert file_input.filename == 'testfile'


def test_file_input_view():
    """Test the view method of FileInput widget."""
    file_input = FileInput(accept='.txt,.csv')

    # When no files are uploaded, the view should be invisible
    view = file_input.view()
    assert not view().visible


    # When custom layout is provided, it should be used
    view_with_layout = file_input.view(layout=Column)
    assert isinstance(view_with_layout(), Column)

    # Test view with uploaded file
    csv_content = "name,value\ntest1,10\ntest2,20\n"
    csv_bytes = csv_content.encode('utf-8')
    csv_b64 = base64.b64encode(csv_bytes).decode('utf-8')

    file_input._process_events({
        'mime_type': 'text/csv',
        'value': csv_b64,
        'filename': 'test.csv'
    })

    view_with_file = file_input.view()
    result = view_with_file()
    assert result.name == 'test.csv'
    assert isinstance(result, Tabulator)
    assert result.value.to_csv(index=False, lineterminator='\n')==csv_content

    # Test object_if_no_value parameter
    fallback_component = Markdown("No files uploaded")
    view_with_fallback = file_input.view(object_if_no_value=fallback_component)
    file_input.clear()
    fallback_result = view_with_fallback()
    assert fallback_result is fallback_component


def test_file_input_view_multiple():
    """Test the view method of FileInput with multiple=True."""
    file_input = FileInput(multiple=True, accept='.txt,.csv')
    file_view = file_input.view(layout=Column)

    # Test view with uploaded files
    csv_content = "name,value\ntest1,10\ntest2,20\n"
    csv_bytes = csv_content.encode('utf-8')
    csv_b64 = base64.b64encode(csv_bytes).decode('utf-8')

    file_input._process_events({
        'mime_type': ['text/csv']*2,
        'value': [csv_b64]*2,
        'filename': ['test0.csv', 'test1.csv']
    })

    result = file_view()
    assert isinstance(result, Column)

    result_0 = result[0]
    assert result_0.name == 'test0.csv'
    assert isinstance(result_0, Tabulator)
    assert result_0.value.to_csv(index=False, lineterminator='\n')==csv_content

    result_1 = result[1]
    assert result_1.name == 'test1.csv'
    assert isinstance(result_1, Tabulator)
    assert result_1.value.to_csv(index=False, lineterminator='\n')==csv_content

@pytest.mark.from_panel
def test_file_input_save_one_file(document, comm, tmpdir):
    file_input = FileInput(accept='.txt')

    file_input._process_events({'mime_type': 'text/plain', 'value': 'U29tZSB0ZXh0Cg==', 'filename': 'testfile'})

    fpath = Path(tmpdir) / 'out.txt'
    file_input.save(str(fpath))

    assert fpath.exists()
    content = fpath.read_text()
    assert content == 'Some text\n'

def test_file_input_initialization():
    """Test FileInput widget initialization with chunking parameters."""
    # Test default parameters
    widget = FileInput()
    assert widget.chunk_size == 10 * 1024 * 1024  # 10MB default
    assert widget.max_file_size is None
    assert widget.max_total_file_size is None
    assert hasattr(widget, '_file_buffer')
    assert widget._file_buffer == {}

    # Test custom parameters
    widget = FileInput(
        chunk_size=5 * 1024 * 1024,  # 5MB
        max_file_size=100 * 1024 * 1024,  # 100MB
        max_total_file_size=500 * 1024 * 1024  # 500MB
    )
    assert widget.chunk_size == 5 * 1024 * 1024
    assert widget.max_file_size == 100 * 1024 * 1024
    assert widget.max_total_file_size == 500 * 1024 * 1024


def test_chunk_processing():
    """Test the chunk processing functionality."""
    widget = FileInput()

    # Simulate a small file upload in chunks
    test_data = b"Hello, this is a test file content for chunked upload testing!"
    filename = "test.txt"
    mime_type = "text/plain"

    # Split into 2 chunks
    chunk_size = len(test_data) // 2
    chunk1 = test_data[:chunk_size]
    chunk2 = test_data[chunk_size:]

    # Process chunk 1
    msg1 = {
        "name": filename,
        "chunk": 1,
        "total_chunks": 2,
        "type": mime_type,
        "data": chunk1
    }
    widget._process_chunk(msg1)

    # Check that file buffer is initialized
    assert filename in widget._file_buffer
    assert widget._file_buffer[filename]["total_chunks"] == 2
    assert 1 in widget._file_buffer[filename]["chunks"]
    assert len(widget._buffer) == 0  # File not complete yet

    # Process chunk 2
    msg2 = {
        "name": filename,
        "chunk": 2,
        "total_chunks": 2,
        "type": mime_type,
        "data": chunk2
    }
    widget._process_chunk(msg2)

    # Check that file is complete and added to buffer
    assert filename not in widget._file_buffer  # Should be cleaned up
    assert len(widget._buffer) == 1
    assert widget._buffer[0]["filename"] == filename
    assert widget._buffer[0]["mime_type"] == mime_type
    assert widget._buffer[0]["value"] == test_data


def test_multiple_files():
    """Test handling multiple files in chunks."""
    print("\nTesting multiple file upload...")

    widget = FileInput()

    # File 1
    data1 = b"Content of first file"
    msg1 = {
        "name": "file1.txt",
        "chunk": 1,
        "total_chunks": 1,
        "type": "text/plain",
        "data": data1
    }

    # File 2
    data2 = b"Content of second file"
    msg2 = {
        "name": "file2.txt",
        "chunk": 1,
        "total_chunks": 1,
        "type": "text/plain",
        "data": data2
    }

    widget._process_chunk(msg1)
    widget._process_chunk(msg2)

    # Check both files were processed
    assert len(widget._buffer) == 2
    filenames = [item["filename"] for item in widget._buffer]
    assert "file1.txt" in filenames
    assert "file2.txt" in filenames
    print("  ✓ Multiple files handled correctly")


def test_incomplete_chunks():
    """Test handling of incomplete chunk sequences."""
    print("\nTesting incomplete chunk handling...")

    widget = FileInput()

    # Send only first chunk of a 2-chunk file
    msg = {
        "name": "incomplete.txt",
        "chunk": 1,
        "total_chunks": 2,
        "type": "text/plain",
        "data": b"First chunk"
    }

    widget._process_chunk(msg)

    # Check that file is not yet complete
    assert "incomplete.txt" in widget._file_buffer
    assert len(widget._buffer) == 0  # No complete files yet
    print("  ✓ Incomplete chunk sequence handled correctly")


def run_all_tests():
    """Run all tests."""
    print("🧪 Running FileInput chunked upload tests...\n")

    try:
        test_size_parsing()
        test_file_input_initialization()
        test_chunk_processing()
        test_arraybuffer_handling()
        test_base64_handling()
        test_legacy_upload_handling()
        test_multiple_files()
        test_incomplete_chunks()

        print("\n✅ All tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
