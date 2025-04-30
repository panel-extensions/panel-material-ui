from __future__ import annotations

import io
import os
from typing import TYPE_CHECKING, Any, Literal

import param
from jinja2 import Template
from panel.config import _base_config, config
from panel.io.resources import ResourceComponent, Resources
from panel.viewable import Children

from ..base import MaterialComponent, ThemedTransform
from ..widgets.base import MaterialWidget

if TYPE_CHECKING:
    from bokeh.document import Document
    from panel.io.location import LocationAreaBase
    from panel.io.resources import ResourcesType


class Meta(param.Parameterized):
    """
    Meta allows controlling meta tags and other HTML head elements.
    """

    name = param.String(default=None, doc="The name of the page.")
    title = param.String(default=None, doc="The title of the page.")
    description = param.String(default=None, doc="The description of the page.")
    keywords = param.String(default=None, doc="The keywords of the page.")
    author = param.String(default=None, doc="The author of the page.")
    viewport = param.String(default=None, doc="The viewport of the page.")
    icon = param.String(default=None, doc="The icon of the page.")
    refresh = param.String(default=None, doc="The refresh of the page.")


class Page(MaterialComponent, ResourceComponent):
    """
    The `Page` component is the equivalent of a `Template` in Panel.

    Unlike a `Template` the `Page` component is implemented entirely
    in Javascript, making it possible to dynamically update components.

    :Example:

    >>> Page(main=['# Content'], title='My App')
    """

    config = param.ClassSelector(default=_base_config(), class_=_base_config,
                                 constant=True, doc="""
        Configuration object declaring custom CSS and JS files to load
        specifically for this template.""")

    contextbar = Children(doc="Items rendered in the contextbar.")

    contextbar_open = param.Boolean(default=False, doc="Whether the contextbar is open or closed.")

    contextbar_width = param.Integer(default=250, doc="Width of the contextbar")

    header = Children(doc="Items rendered in the header.")

    main = Children(doc="Items rendered in the main area.")

    meta = param.ClassSelector(default=Meta(), class_=Meta, doc="Meta tags and other HTML head elements.")

    sidebar = Children(doc="Items rendered in the sidebar.")

    sidebar_open = param.Boolean(default=True, doc="Whether the sidebar is open or closed.")

    sidebar_variant = param.Selector(default="auto", objects=["persistent", "temporary", "permanent", "auto"], doc="""
        Whether the sidebar is persistent, a temporary drawer, a permanent drawer, or automatically switches between the two based on screen size.""")

    sidebar_width = param.Integer(default=320, doc="Width of the sidebar")

    theme_toggle = param.Boolean(default=True, doc="Whether to show a theme toggle button.")

    title = param.String(doc="Title of the application.")

    _esm_base = "Page.jsx"
    _rename = {"config": None, "meta": None}
    _source_transforms = {
        "header": None,
        "contextbar": None,
        "sidebar": None,
        "main": None,
    }

    def __init__(self, **params):
        resources, meta = {}, {}
        for k in list(params):
            if k.startswith('meta_'):
                meta[k.replace('meta_', '')] = params.pop(k)
            elif k in _base_config.param and k != 'name':
                resources[k] = params.pop(k)
        if "title" in params and "title" not in meta:
            meta["title"] = params["title"]
        super().__init__(**params)
        self.meta.param.update(**meta)
        self.config.param.update(**resources)

    @param.depends('dark_theme', watch=True)
    def _update_config(self):
        config.theme = 'dark' if self.dark_theme else 'default'

    def _add_resources(self, resources, extras, raw_css):
        for rname, res in resources.items():
            if not res:
                continue
            elif rname == "raw_css":
                raw_css += res
            elif rname not in extras:
                extras[rname] = res
            elif isinstance(res, dict):
                extras[rname].update(res)  # type: ignore
            elif isinstance(extras[rname], dict):
                extras[rname].update({r.split('/')[-1].split('.')[0]: r for r in res})
            else:
                extras[rname] += [  # type: ignore
                    r for r in res if r not in extras.get(rname, [])  # type: ignore
                ]

    def resolve_resources(
        self,
        cdn: bool | Literal['auto'] = 'auto',
        extras: dict[str, dict[str, str]] | None = None
    ) -> ResourcesType:
        extras = extras or {}
        raw_css = []
        config_resources = {
            rt: getattr(self.config, 'css_files' if rt == 'css' else rt)
            for rt in self._resources if rt == 'css' or rt in self.config.param
        }
        design_resources = self._design.resolve_resources()
        self._add_resources(design_resources, extras, raw_css)
        self._add_resources(config_resources, extras, raw_css)
        resources = super().resolve_resources(extras=extras)
        resources["raw_css"] += raw_css
        return resources

    def save(
        self,
        filename: str | os.PathLike | io.IO,
        title: str | None = None,
        resources: Resources | None = None,
        template: str | Template | None = None,
        template_variables: dict[str, Any] | None = None,
        **kwargs
    ) -> None:
        if not template_variables:
            template_variables = {}
        template_variables['meta'] = self.meta
        template_variables['resources'] = self.resolve_resources()
        super().save(
            filename,
            title,
            resources,
            template,
            template_variables,
            **kwargs
        )

    def server_doc(
        self, doc: Document | None = None, title: str | None = None,
        location: bool | LocationAreaBase | None = True
    ) -> Document:
        title = title or self.title or self.meta.title or 'Panel Application'
        doc = super().server_doc(doc, title, location)
        doc.template_variables['meta'] = self.meta
        doc.template_variables['resources'] = self.resolve_resources()
        return doc


class ThemeToggle(MaterialWidget):
    """
    A toggle button to switch between light and dark themes.
    """

    color = param.Selector(default='primary', objects=['primary', 'secondary'], doc="The color of the theme toggle.")

    theme = param.Selector(default=None, objects=['dark', 'default'], constant=True, doc="The current theme.")

    value = param.Boolean(default=None, doc="Whether the theme toggle is on or off.")

    variant = param.Selector(default='icon', objects=['icon', 'switch'], doc="Whether to render just an icon or a toggle")

    width = param.Integer(default=None, doc="The width of the theme toggle.")

    _esm_base = "ThemeToggle.jsx"
    _esm_transforms = [ThemedTransform]
    _rename = {"theme_toggle": None}

    def __init__(self, **params):
        params['theme'] = config.theme
        params['value'] = config.theme == 'dark'
        super().__init__(**params)

    @param.depends('value', watch=True)
    def _update_theme(self):
        with param.parameterized.edit_constant(self):
            self.theme = config.theme = 'dark' if self.value else 'default'


__all__ = [
    "Page",
    "ThemeToggle"
]
