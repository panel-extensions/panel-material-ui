import base64
import pytest

from pathlib import Path
from panel import config
from datetime import date

from panel_material_ui.widgets import FileInput, IntInput, FloatInput, DatePicker
from panel_material_ui.layout import Column
from panel.pane import Markdown
from panel.widgets import Tabulator, CodeEditor



@pytest.mark.from_panel
def test_file_input(document, comm):
    file_input = FileInput(accept='.txt')

    file_input._process_events({'mime_type': 'text/plain', 'value': 'U29tZSB0ZXh0Cg==', 'filename': 'testfile'})
    assert file_input.value == b'Some text\n'
    assert file_input.mime_type == 'text/plain'
    assert file_input.accept == '.txt'
    assert file_input.filename == 'testfile'


@pytest.mark.from_panel
def test_file_input_save_one_file(document, comm, tmpdir):
    file_input = FileInput(accept='.txt')

    file_input._process_events({'mime_type': 'text/plain', 'value': 'U29tZSB0ZXh0Cg==', 'filename': 'testfile'})

    fpath = Path(tmpdir) / 'out.txt'
    file_input.save(str(fpath))

    assert fpath.exists()
    content = fpath.read_text()
    assert content == 'Some text\n'


@pytest.mark.from_panel
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


@pytest.mark.from_panel
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


@pytest.mark.from_panel
def test_date_picker():
    date_picker = DatePicker(name='DatePicker', value=date(2018, 9, 2),
                             start=date(2018, 9, 1), end=date(2018, 9, 10))

    date_picker._process_events({'value': '2018-09-03'})
    assert date_picker.value == date(2018, 9, 3)

    date_picker._process_events({'value': date(2018, 9, 5)})
    assert date_picker.value == date(2018, 9, 5)

    date_picker._process_events({'value': date(2018, 9, 6)})
    assert date_picker.value == date(2018, 9, 6)


@pytest.mark.from_panel
def test_date_picker_options():
    options = [date(2018, 9, 1), date(2018, 9, 2), date(2018, 9, 3)]
    datetime_picker = DatePicker(
        name='DatetimePicker', value=date(2018, 9, 2),
        options=options
    )
    assert datetime_picker.value == date(2018, 9, 2)
    assert datetime_picker.enabled_dates == options


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
    assert result.value.to_csv(index=False)==csv_content

    # Test view_if_none parameter
    fallback_component = Markdown("No files uploaded")
    view_with_fallback = file_input.view(view_if_none=fallback_component)
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
    assert result_0.value.to_csv(index=False)==csv_content

    result_1 = result[1]
    assert result_1.name == 'test1.csv'
    assert isinstance(result_1, Tabulator)
    assert result_1.value.to_csv(index=False)==csv_content


def test_file_input_view_code_mime_types():
    """Test FileInput view method code MIME types"""
    # Test CSS file
    for mime_type, config in FileInput._code_mime_types.items():
        css_content = b"test value"
        result = FileInput._single_view(css_content, "some.file", mime_type=mime_type)
        assert isinstance(result, CodeEditor)
        assert result.value == "test value"
        assert result.language == config['language']
        assert result.disabled


def test_file_input_view_other_mime_types():
    """Test FileInput view method other MIME types"""
    # Test Microsoft Word document
    doc_content = b"mock word document content"
    result = FileInput._single_view(doc_content, "document.docx",
                                   "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    assert hasattr(result, 'object')
    assert "Microsoft Word Document" in result.object

    # Test PowerPoint presentation
    ppt_content = b"mock powerpoint content"
    result = FileInput._single_view(ppt_content, "presentation.pptx",
                                   "application/vnd.openxmlformats-officedocument.presentationml.presentation")
    assert hasattr(result, 'object')
    assert "Microsoft PowerPoint Presentation" in result.object

    # Test OpenDocument Text
    odt_content = b"mock odt content"
    result = FileInput._single_view(odt_content, "document.odt", "application/vnd.oasis.opendocument.text")
    assert hasattr(result, 'object')
    assert "OpenDocument Text" in result.object
