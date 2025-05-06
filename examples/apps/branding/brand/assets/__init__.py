from pathlib import Path

ROOT = Path(__file__).parent

def _absolute(path):
    """
    Convert a path to a string.
    """
    return str(Path(ROOT/path).absolute())

# We need to convert to absolute paths because meta.icon etc does not support `Path` objects
FAVICON_PATH = _absolute("favicon.ico") # Source: https://favicon.io/favicon-generator/
LOGO_SVG_URL = ROOT / "brand/assets/logo.svg" # Source: https://text-to-svg.com/montserrat-font-to-svg
LOGO_PNG_URL = ROOT / "brand/assets/logo.png" # Source: https://svgtopng.com/
PRODUCT_URL = ROOT / "brand/assets/orbitron_products.png" # Source: ChatGPT
STYLE_CSS_URL = ROOT / "brand/assets/style.css" # Source: https://www.w3schools.com/w3css/w3css_templates.asp

RAW_CSS = (ROOT/ "style.css").read_text()
