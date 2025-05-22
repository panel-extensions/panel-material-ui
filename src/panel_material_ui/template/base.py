from __future__ import annotations

import functools
import io
import os
import pathlib
from typing import TYPE_CHECKING, Any, Literal

import param
from jinja2 import Template
from panel.config import _base_config, config
from panel.io.resources import ResourceComponent, Resources
from panel.io.state import state
from panel.util import edit_readonly
from panel.viewable import Child, Children

from .._utils import _read_icon
from ..base import BASE_TEMPLATE, MaterialComponent, ThemedTransform, _env
from ..widgets.base import MaterialWidget

if TYPE_CHECKING:
    from bokeh.document import Document
    from panel.io.location import LocationAreaBase
    from panel.io.resources import ResourcesType

SIDEBAR_VARIANTS = ["persistent", "temporary", "permanent", "auto"]

@functools.cache
def parse_template(tmpl, *args, **kwargs):
    if os.path.isfile(tmpl):
        tmpl = pathlib.Path(tmpl).read_text(encoding='utf-8')
    return _env.from_string(tmpl, *args, **kwargs)


class Meta(param.Parameterized):
    """
    Meta allows controlling meta tags and other HTML head elements.
    """

    name = param.String(default="Panel App", doc="The name of the page.")
    title = param.String(default=None, doc="The title of the page.")
    description = param.String(default=None, doc="The description of the page.")
    keywords = param.String(default=None, doc="The keywords of the page.")
    author = param.String(default=None, doc="The author of the page.")
    viewport = param.String(default="width=device-width, initial-scale=1.0", doc="The viewport of the page.")
    icon = param.String(default=None, doc="The 32x32 icon of the page.")
    apple_touch_icon = param.String(default=None, doc="The apple 180x180 touch icon of the page.")
    refresh = param.String(default=None, doc="The refresh of the page.")


class Page(MaterialComponent, ResourceComponent):
    """
    The `Page` component is the equivalent of a `Template` in Panel.

    Unlike a `Template` the `Page` component is implemented entirely
    in Javascript, making it possible to dynamically update components.

    :References:

    - https://panel-material-ui.holoviz.org/reference/page/Page.html

    :Example:

    >>> Page(main=['# Content'], title='My App')
    """

    busy = param.Boolean(default=False, readonly=True, doc="Whether the page is busy.")

    busy_indicator = param.Selector(default="linear", objects=["circular", "linear", None], doc="""
        The type of busy indicator to show.""")

    config = param.ClassSelector(default=_base_config(), class_=_base_config,
                                 constant=True, doc="""
        Configuration object declaring custom CSS and JS files to load
        specifically for this template.""")

    contextbar = Children(doc="Items rendered in the contextbar.")

    contextbar_open = param.Boolean(default=False, doc="Whether the contextbar is open or closed.")

    contextbar_width = param.Integer(default=250, doc="Width of the contextbar")

    favicon = param.ClassSelector(default=None, class_=(str, pathlib.Path), doc="The favicon of the page.")

    header = Children(doc="Items rendered in the header.")

    main = Children(doc="Items rendered in the main area.")

    meta = param.ClassSelector(default=Meta(), class_=Meta, doc="Meta tags and other HTML head elements.")

    logo = param.ClassSelector(default=None, class_=(str, pathlib.Path, dict), doc="""
        Logo to render in the header. Can be a string, a pathlib.Path, or a dictionary with
        breakpoints as keys, e.g. {'sm': 'logo_mobile.png', 'md': 'logo.png'}.""")

    sidebar = Children(doc="Items rendered in the sidebar.")

    sidebar_open = param.Boolean(default=True, doc="Whether the sidebar is open or closed.")

    sidebar_variant = param.Selector(default="auto", objects=SIDEBAR_VARIANTS, doc="""
        Whether the sidebar is persistent, a temporary drawer, a permanent drawer, or automatically
        switches between the two based on screen size.""")

    sidebar_width = param.Integer(default=320, doc="Width of the sidebar")

    site_url = param.String(default="/", doc="""
        URL of the site and logo. Default is '/'.""")

    template = param.ClassSelector(default=None, class_=(str, pathlib.Path, Template), doc="""
        Overrides the default jinja2 template. Template can be provided as a string,
        Path or jinja2.Template instance.""")

    theme_toggle = param.Boolean(default=True, doc="Whether to show a theme toggle button.")

    title = param.String(doc="Title of the application.")

    _esm_base = "Page.jsx"
    _rename = {"config": None, "meta": None, "favicon": None, "apple_touch_icon": None, "template": None}
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
        with edit_readonly(self):
            self.busy = state.param.busy

    @param.depends('template', watch=True, on_init=True)
    def _update_template(self):
        if self.template is None:
            self._template = BASE_TEMPLATE
        elif isinstance(self.template, (str, pathlib.Path)):
            self._template = parse_template(self.template)
        else:
            self._template = self.template

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

    def _process_param_change(self, params):
        params = super()._process_param_change(params)
        if logo := params.get('logo'):
            if isinstance(logo, dict):
                logo = {bp: _read_icon(lg) for bp, lg in logo.items()}
            else:
                logo = _read_icon(logo)
            params['logo'] = logo
        return params

    def _populate_template_variables(self, template_variables):
        template_variables['meta'] = self.meta
        if favicon := self.favicon or self.meta.icon:
            template_variables['favicon'] = _read_icon(favicon)
        if apple_touch_icon := self.meta.apple_touch_icon:
            template_variables['apple_touch_icon'] = _read_icon(apple_touch_icon)
        template_variables['resources'] = self.resolve_resources()
        template_variables['is_page'] = True

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
        if template_variables:
            template_variables = dict(template_variables)
        else:
            template_variables = {}
        if template is None:
            template = self._template
        self._populate_template_variables(template_variables)
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
        self._populate_template_variables(doc.template_variables)
        doc.template = self._template
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


class BreakpointSwitcher(MaterialComponent):
    """
    The `BreakpointSwitcher` component allows switching between two component implementations
    based on the declared breakpoint or media_query.

    :References:

    - https://panel-material-ui.holoviz.org/reference/page/BreakpointSwitcher.html

    :Example:

    >>> BreakpointSwitcher(breakpoint='sm', small=..., large=...)
    """

    current = param.Parameter(allow_refs=False, readonly=True, doc="""
        The current object.""")

    breakpoint = param.Selector(default='md', objects=["xs", "sm", "md", "lg", "xl"], doc="""
        Breakpoint at which switcher toggles between.""")

    media_query = param.String(default=None, doc="""
        Media query to use for the breakpoint (takes precedence over breakpoint).""")

    small = Child(doc="Items rendered in the small breakpoint.")

    large = Child(doc="Items rendered in the large breakpoint.")

    _esm_base = "BreakpointSwitcher.jsx"
    _rename = {"current": None}

    def _handle_msg(self, msg):
        if msg['type'] == 'switch':
            with edit_readonly(self):
                self.current = getattr(self, msg['current'])


__all__ = [
    "BreakpointSwitcher",
    "Page",
    "ThemeToggle"
]
