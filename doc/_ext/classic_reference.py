"""
Cross-links the panel-material-ui component gallery with Panel's gallery.

Most components here reimplement a classic Panel component of the same name, and
from Panel 1.10 both are reachable, the Material one as ``pn.ui.Button`` and the
classic one as ``pn.widgets.Button``. This extension adds a banner to every
reference page that has a classic counterpart, pointing at its Panel page.

The set is derived at build time from Panel's intersphinx inventory and from the
classic namespaces, so it cannot drift out of sync with either project's pages.

The reciprocal banner is added by ``doc/_ext/material_reference.py`` in Panel.
"""
from __future__ import annotations

import pathlib

from sphinx.util import logging

logger = logging.getLogger(__name__)

INVENTORY = 'panel'

# Namespace on the panel package a classic component lives in, by Panel gallery
# section. Attribute access rather than import, since panel.indicators is an
# alias for panel.widgets.indicators and is not importable under that name.
CLASSIC_NAMESPACES = {
    'chat': 'chat',
    'indicators': 'indicators',
    'layouts': 'layout',
    'panes': 'pane',
    'widgets': 'widgets',
}

BANNER = """
:::{{admonition}} This component replaces a classic Panel component
:class: tip

Panel's own implementation is `{classic}`, documented in the
{{external+{inventory}:doc}}`Panel reference <{target}>`. This page documents the
Material Design version, which is what `pn.ui.{name}` resolves to in Panel 1.10
and later.
:::
"""

_cache: dict[str, object] = {}


def classic_pages(env) -> dict[str, tuple[str, str]]:
    """
    Reference pages on the Panel site that document a classic component this
    project reimplements, as ``{name: (docname, classic path)}``.
    """
    if 'pages' in _cache:
        return _cache['pages']
    inventories = getattr(env, 'intersphinx_named_inventory', {})
    if INVENTORY not in inventories:
        logger.warning(
            'No %r intersphinx inventory, classic reference banners will not be '
            'added. Is the site reachable?', INVENTORY
        )
    import panel
    pages = {}
    for docname in inventories.get(INVENTORY, {}).get('std:doc', {}):
        parts = docname.split('/')
        if len(parts) != 3 or parts[0] != 'reference' or parts[2] == 'index':
            continue
        _, section, name = parts
        attr = CLASSIC_NAMESPACES.get(section)
        namespace = getattr(panel, attr, None) if attr else None
        if namespace is None or getattr(namespace, name, None) is None:
            continue
        pages[name] = (docname, f'pn.{attr}.{name}')
    _cache['pages'] = pages
    return pages


def banner_line(lines: list[str]) -> int:
    """
    Line the banner is inserted at, after the title and the download links
    nbsite writes above the first thematic break.
    """
    for i, line in enumerate(lines[:8]):
        if line.strip() == '---':
            return i + 1
    for i, line in enumerate(lines[:4]):
        if line.startswith('# '):
            return i + 1
    return 0


def add_classic_banner(app, docname, source):
    parts = docname.split('/')
    if len(parts) != 3 or parts[0] != 'reference':
        return
    name = parts[2]
    pages = classic_pages(app.env)
    if name not in pages:
        return
    target, classic = pages[name]
    banner = BANNER.format(
        name=name, classic=classic, inventory=INVENTORY, target=target
    )
    lines = source[0].split('\n')
    at = banner_line(lines)
    source[0] = '\n'.join(lines[:at] + banner.split('\n') + lines[at:])
    logger.debug('[classic_reference] linked %s to %s', docname, target)


def clear_cache(app):
    _cache.clear()


def report(app):
    """
    Logs the number of classic components found, so that a build which silently
    stops linking them is visible in the log. Runs late so that intersphinx has
    loaded its inventories.
    """
    pages = classic_pages(app.env)
    linked = [
        path.stem for path in pathlib.Path(app.srcdir).glob('reference/*/*.md')
        if path.stem in pages
    ]
    log = logger.info if linked else logger.warning
    log('Cross-linking %d reference pages to their classic version.', len(linked))


def setup(app):
    app.connect('builder-inited', clear_cache)
    app.connect('builder-inited', report, priority=900)
    app.connect('source-read', add_classic_banner)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
