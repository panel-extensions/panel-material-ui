from pathlib import Path

FAVICON_URL = "brand/assets/favicon.ico" # Source: https://favicon.io/favicon-generator/
LOGO_SVG_URL = "brand/assets/logo.svg" # Source: https://text-to-svg.com/montserrat-font-to-svg
LOGO_PNG_URL = "brand/assets/logo.png" # Source: https://svgtopng.com/
STYLE_CSS_URL = "brand/assets/style.css" # Source: https://www.w3schools.com/w3css/w3css_templates.asp

RAW_CSS = (Path(__file__).parent / "style.css").read_text()
