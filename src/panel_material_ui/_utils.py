from __future__ import annotations

import html
import json
import os
import re

import bokeh
from bokeh.embed.bundle import URL
from packaging.version import Version
from panel.io.cache import cache
from panel.pane.base import panel
from panel.pane.image import ImageBase

bokeh_version = Version(Version(bokeh.__version__).base_version)
BOKEH_GE_3_8 = bokeh_version >= Version('3.8')

ICON_TOKEN_PATTERN = re.compile(r':material/([a-zA-Z0-9_]+)(?:@([^:]*))?:')

ICON_VARIANT_CLASSES = {
    '': 'material-icons',
    'filled': 'material-icons',
    'outline': 'material-icons-outlined',
    'outlined': 'material-icons-outlined',
    'round': 'material-icons-round',
    'rounded': 'material-icons-round',
    'sharp': 'material-icons-sharp',
}

ICON_NAME_SUFFIXES = {
    '_outlined': 'material-icons-outlined',
    '_rounded': 'material-icons-round',
    '_sharp': 'material-icons-sharp',
}


def _icon_token_span(match: re.Match) -> str:
    icon, options = match.group(1), match.group(2) or ''
    parsed = {}
    for pair in options.split(','):
        if '=' not in pair:
            continue
        key, _, value = pair.partition('=')
        parsed[key.strip()] = value.strip()
    cls = ICON_VARIANT_CLASSES.get(parsed.get('variant', '').lstrip('-_').lower(), 'material-icons')
    for suffix, suffix_cls in ICON_NAME_SUFFIXES.items():
        if icon.endswith(suffix):
            icon, cls = icon[:-len(suffix)], suffix_cls
            break
    styles = ['vertical-align: middle', 'font-size: 1.2em']
    size = parsed.get('icon_size') or parsed.get('size')
    if size and size not in ('small', 'medium', 'large'):
        styles[1] = f'font-size: {size}'
    if 'color' in parsed:
        styles.append(f'color: {parsed["color"]}')
    return f'<span class="{cls}" style="{"; ".join(styles)}">{html.escape(icon)}</span>'


def render_icon_tokens_html(text: str | None) -> str | None:
    """
    Replaces :material/<icon>: tokens with Material Icons ``<span>`` elements.

    Used for values which are rendered by an HTML pane instead of one of the
    Material UI React components, e.g. the streaming ``ChatStep`` title.

    Parameters
    ----------
    text: str | None
        The text to render.

    Returns
    -------
    The text with icon tokens replaced by Material Icons spans.
    """
    if not text or not isinstance(text, str):
        return text
    return ICON_TOKEN_PATTERN.sub(_icon_token_span, text)


@cache
def _read_icon(icon):
    """
    Read an icon from a file or URL and return a base64 encoded string.
    """
    if os.path.isfile(icon):
        img = panel(icon)
        if not isinstance(img, ImageBase):
            raise ValueError(f"Could not determine file type of logo: {icon}.")
        imgdata = img._data(img.object)
        if imgdata:
            icon_string = img._b64(imgdata)
            if str(icon).endswith('.ico'):
                icon_string = icon_string.replace("data:image/ico;", "data:image/x-icon;")
        else:
            raise ValueError(f"Could not embed logo {icon}.")
    else:
        icon_string = icon
    return icon_string

def conffilter(value):
    return json.dumps(dict(value)).replace('"', '\'')

class json_dumps(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, URL):
            return str(obj)
        return super().default(obj)
