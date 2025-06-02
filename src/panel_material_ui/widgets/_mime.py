import io
import json
import tempfile
from functools import partial

from panel.pane import GIF, JPG, JSON, PDF, PNG, SVG, Audio, Markdown, Video, WebP
from panel.widgets import CodeEditor, Tabulator


class NoConverter(Exception):
    """Exception raised when no converter is available for a MIME type."""


def _csv_to_dataframe(value: bytes):
    """
    Reads a CSV file from bytes data using pandas.

    Parameters
    ----------
    value : bytes
        The bytes data of the CSV file.

    Returns
    -------
    pandas.DataFrame
        The DataFrame containing the CSV data.
    """
    import pandas as pd
    if not value:
        return pd.DataFrame()
    return pd.read_csv(io.BytesIO(value))

def _to_string(value: bytes) -> str:
    return value.decode('utf-8')

def _excel_to_dataframe(value: bytes):
    """
    Reads an Excel file from bytes data using pandas.

    Parameters
    ----------
    value : bytes
        The bytes data of the Excel file.

    Returns
    -------
    pandas.DataFrame
        The DataFrame containing the Excel data.
    """
    import pandas as pd
    if not value:
        return pd.DataFrame()
    return pd.read_excel(io.BytesIO(value))

def _ods_to_dataframe(value: bytes):
    """
    Reads an ODS spreadsheet file from bytes data using pandas.

    Parameters
    ----------
    value : bytes
        The bytes data of the ODS file.

    Returns
    -------
    pandas.DataFrame
        The DataFrame containing the ODS data.
    """
    import pandas as pd
    if not value:
        return pd.DataFrame()
    return pd.read_excel(io.BytesIO(value), engine='odf')

def _json_to_dict(value: bytes) -> dict:
    """
    Converts bytes data to a dictionary by decoding JSON.

    Parameters
    ----------
    value : bytes
        The bytes data containing JSON.

    Returns
    -------
    dict
        The dictionary representation of the JSON data.
    """
    return json.loads(value.decode('utf-8'))

def _to_pil_image(value: bytes):
    """
    Converts bytes data to a PIL Image.

    Parameters
    ----------
    value : bytes
        The bytes data of the image.

    Returns
    -------
    PIL.Image.Image
        The PIL Image object.
    """
    from PIL import Image
    return Image.open(io.BytesIO(value))

def _no_conversion(value: bytes) -> bytes:
    """
    Returns the bytes data without any conversion.

    Parameters
    ----------
    value : bytes
        The bytes data to return.

    Returns
    -------
    bytes
        The original bytes data.
    """
    return value

def _save_to_tempfile(data: bytes, suffix: str) -> str:
    """
    Save bytes data to a temporary file and return the file path.

    Parameters
    ----------
    data : bytes
        The bytes data to save.
    filename : str
        The name of the file to save the data as.

    Returns
    -------
    str
        The path to the temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + suffix) as temp_file:
        temp_file.write(data)
        return temp_file.name


MIME_TYPES = {
    # Text Files
    "text/plain": {"converter": _to_string, "view": Markdown},
    "text/markdown": {"converter": _to_string, "view": Markdown},
    "text/x-markdown": {"converter": _to_string, "view": Markdown},
    # Dataframe Files
    "text/csv": {"converter": _csv_to_dataframe, "view": Tabulator},
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
        "converter": _excel_to_dataframe, "view": Tabulator
    },
    "application/vnd.ms-excel": {
        "converter": _excel_to_dataframe, "view": Tabulator
    },
    "application/vnd.oasis.opendocument.spreadsheet": {
        "converter": _ods_to_dataframe, "view": Tabulator
    },
    # Code Files
    "text/javascript": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "javascript", "disabled": True}
    },
    "application/javascript": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "javascript", "disabled": True}
    },
    "text/x-python": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "python", "disabled": True}
    },
    "application/x-python": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "python", "disabled": True}
    },
    "text/css": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "css", "disabled": True}
    },
    "application/x-httpd-php": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "php", "disabled": True}
    },
    "application/x-sh": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "bash", "disabled": True}},
    "application/sql": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "sql", "disabled": True}},
    "application/x-yaml": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "yaml", "disabled": True}},
    "text/yaml": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "yaml", "disabled": True}},
    "text/x-yaml": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "yaml", "disabled": True}},
    "application/xml": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "xml", "disabled": True}},
    "text/xml": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "xml", "disabled": True}},
    "text/html": {
        "converter": _to_string,
        "view": CodeEditor,
        "view_kwargs": {"language": "html", "disabled": True}},
    # # Media files
    "image/svg+xml": {"converter": _to_string, "view": SVG},
    "image/png": {"converter": _to_pil_image, "view": PNG},
    "image/jpeg": {"converter": _to_pil_image, "view": JPG},
    "image/gif": {"converter": _no_conversion, "view": GIF},
    "image/webp": {"converter": _no_conversion, "view": WebP},
    "audio/wav": {"converter": partial(_save_to_tempfile, suffix="wav"), "view": Audio},
    "audio/mpeg": {"converter": partial(_save_to_tempfile, suffix="mp3"), "view": Audio},
    "audio/ogg": {"converter": partial(_save_to_tempfile, suffix="ogg"), "view": Audio},
    "video/mp4": {"converter": partial(_save_to_tempfile, suffix="mp4"), "view": Video},
    # Other files
    "application/pdf": {"converter": partial(_save_to_tempfile, suffix="pdf"), "view": PDF},
    "application/json": {"converter": _json_to_dict, "view": JSON},
}
