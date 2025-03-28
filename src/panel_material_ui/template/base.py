from __future__ import annotations

import json
import pathlib
from typing import TYPE_CHECKING

import param
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from panel.config import config
from panel.io.resources import URL
from panel.viewable import Children

from ..base import MaterialComponent

if TYPE_CHECKING:
    from bokeh.document import Document
    from panel.io.location import LocationAreaBase


def get_env():
    ''' Get the correct Jinja2 Environment, also for frozen scripts.
    '''
    internal_path = pathlib.Path(__file__).parent / '..' / '_templates'
    return Environment(loader=FileSystemLoader([
        str(internal_path.resolve())
    ]))

def conffilter(value):
    return json.dumps(dict(value)).replace('"', '\'')

class json_dumps(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, URL):
            return str(obj)
        return super().default(obj)

_env = get_env()
_env.trim_blocks = True
_env.lstrip_blocks = True
_env.filters['json'] = lambda obj: Markup(json.dumps(obj, cls=json_dumps))
_env.filters['conffilter'] = conffilter
_env.filters['sorted'] = sorted


class Page(MaterialComponent):
    """
    The `Page` component is the equivalent of a `Template` in Panel.

    Unlike a `Template` the `Page` component is implemented entirely
    in Javascript, making it possible to dynamically update components.

    :Example:

    >>> Page(main=['# Content'], title='My App')
    """

    contextbar = Children(doc="Items rendered in the contextbar.")

    contextbar_open = param.Boolean(default=False, doc="Whether the contextbar is open or closed.")

    contextbar_width = param.Integer(default=250, doc="Width of the contextbar")

    header = Children(doc="Items rendered in the header.")

    main = Children(doc="Items rendered in the main area.")

    sidebar = Children(doc="Items rendered in the sidebar.")

    sidebar_open = param.Boolean(default=True, doc="Whether the sidebar is open or closed.")

    sidebar_variant = param.Selector(default="persistent", objects=["persistent", "drawer"])

    sidebar_width = param.Integer(default=250, doc="Width of the sidebar")

    title = param.String(doc="Title of the application.")

    _esm_base = "Page.jsx"

    @param.depends('dark_theme', watch=True)
    def _update_config(self):
        config.theme = 'dark' if self.dark_theme else 'default'

    def server_doc(
        self, doc: Document | None = None, title: str | None = None,
        location: bool | LocationAreaBase | None = True
    ) -> Document:
        doc = super().server_doc(doc, title, location)
        doc.template = _env.get_template('base.html')
        return doc

__all__ = [
    "Page"
]
