"""Asset management for the branding package."""

from pathlib import Path
from typing import Union

ROOT = Path(__file__).parent


def _absolute(path: str) -> str:
    """
    Convert a relative path to an absolute path string.

    Parameters
    ----------
    path : str
        The relative path to convert

    Returns
    -------
    str
        The absolute path as a string
    """
    return str(Path(ROOT / path).resolve())


# Assets with absolute paths for compatibility with Panel APIs
FAVICON_PATH = _absolute("favicon.ico")  # Source: https://favicon.io/favicon-generator/
LOGO_PATH = _absolute("logo.png")  # Source: ChatGPT
VISION_PATH = _absolute("vision.png")

# Load CSS from file
try:
    css_file = ROOT / "style.css"
    RAW_CSS = css_file.read_text(encoding="utf-8") if css_file.exists() else ""
except Exception as e:
    import warnings

    warnings.warn(f"Failed to load CSS file: {e}")
    RAW_CSS = ""

__all__ = [
    "FAVICON_PATH",
    "LOGO_PATH",
    "VISION_PATH",
    "RAW_CSS",
    "_absolute",  # Exposed for potential reuse in related modules
]
