import json
import os
import pathlib

from typing import Any

import param

param.parameterized.docstring_signature = False
param.parameterized.docstring_describe_params = False

from nbsite.shared_conf import *

project = 'Panel Material UI'
authors = 'Panel contributors'
copyright_years['start_year'] = '2024'
copyright = copyright_fmt.format(**copyright_years)
description = 'Panel Material UI extension'

import panel
import panel_material_ui

from panel.io.convert import (
    BOKEH_VERSION, MINIMUM_VERSIONS, PY_VERSION, PYODIDE_VERSION,
    PYSCRIPT_VERSION,
)
from panel.io.resources import CDN_ROOT

PANEL_ROOT = pathlib.Path(panel.__file__).parent

version = release = base_version(panel_material_ui.__version__)
js_version = json.loads((PANEL_ROOT / 'package.json').read_text())['version']

is_dev = any(ext in version for ext in ('a', 'b', 'rc'))

# For the interactivity warning box created by nbsite to point to the right
# git tag instead of the default i.e. main.
os.environ['BRANCH'] = f"v{release}"

html_static_path += ['_static']

html_css_files += [
    'css/custom.css',
]

html_theme = "pydata_sphinx_theme"
html_favicon = "_static/icons/favicon.ico"

current_release = panel_material_ui.__version__  # Current release version variable

html_theme_options = {
    "logo": {
        "image_light": "_static/logo_horizontal_light_theme.png",
        "image_dark": "_static/logo_horizontal_dark_theme.png",
    },
    "github_url": "https://github.com/panel-extensions/panel-material-ui",
    "icon_links": [
        {
            "name": "Twitter",
            "url": "https://twitter.com/Panel_Org",
            "icon": "fa-brands fa-twitter-square",
        },
        {
            "name": "Discourse",
            "url": "https://discourse.holoviz.org/c/panel/5",
            "icon": "fa-brands fa-discourse",
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/UXdtYyGVQX",
            "icon": "fa-brands fa-discord",
        },
    ],
    "pygments_light_style": "material",
    "pygments_dark_style": "material",
    "header_links_before_dropdown": 5,
    'secondary_sidebar_items': [
        # "github-stars-button",
        # "panelitelink",
        "page-toc",
    ],
}


extensions = [
    'numpydoc',
    'bokeh.sphinxext.bokeh_plot',
    'myst_parser',
    'sphinx_design',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.linkcode',
    'sphinx.ext.inheritance_diagram',
    'sphinx_copybutton',
    'sphinxext.rediraffe',
    'nbsite.gallery',
    'nbsite.pyodide',
    'nbsite.analytics',
]

numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = False
napoleon_numpy_docstring = True

autodoc_mock_imports = ["panel.pane.vtk"]

myst_enable_extensions = ["colon_fence", "deflist"]

gallery_endpoint = 'panel-gallery-dev' if is_dev else 'panel-gallery'
gallery_url = f'https://{gallery_endpoint}.holoviz-demo.anaconda.com'
jlite_url = 'https://holoviz-dev.github.io/panelite-dev/lab' if is_dev else 'https://panelite.holoviz.org/lab'
pyodide_url = 'https://holoviz-dev.github.io/panel/pyodide' if is_dev else 'https://panel.holoviz.org/pyodide'

nbsite_analytics = {
    'goatcounter_holoviz': True,
}

nbsite_gallery_conf = {
    'github_org': 'panel-extensions',
    'github_project': 'panel-material-ui',
    'galleries': {
        'reference': {
            'title': 'Component Gallery',
            'extensions': ['*.ipynb', '*.py', '*.md'],
            'sections': [
                'widgets',
                'menus',
                'layouts',
                'panes',
                'page',
                'chat',
                'indicators',
                'global'
            ],
            'as_pyodide': True,
            'normalize_titles': False,
        }
    },
    'thumbnail_url': 'https://assets.holoviz.org/panel-material-ui/thumbnails',
    'only_use_existing': True,
}

if panel.__version__ != version and (PANEL_ROOT / 'dist' / 'wheels').is_dir():
    py_version = panel.__version__.replace("-dirty", "")
    panel_req = f'./wheels/panel-{py_version}-py3-none-any.whl'
    bokeh_req = f'./wheels/bokeh-{BOKEH_VERSION}-py3-none-any.whl'
else:
    panel_req = f'{CDN_ROOT}wheels/panel-{PY_VERSION}-py3-none-any.whl'
    bokeh_req = f'{CDN_ROOT}wheels/bokeh-{BOKEH_VERSION}-py3-none-any.whl'

html_js_files = [
    (None, {'body': '{"shimMode": true}', 'type': 'esms-options'}),
    f'https://cdn.holoviz.org/panel/{js_version}/dist/bundled/reactiveesm/es-module-shims@^1.10.0/dist/es-module-shims.min.js',
]

nbsite_pyodide_conf = {
    'PYODIDE_URL': f'https://cdn.jsdelivr.net/pyodide/{PYODIDE_VERSION}/full/pyodide.js',
    'requirements': [bokeh_req, panel_req, 'pyodide-http'],
    'requires': ["panel-material-ui"],
}

templates_path += [
    '_templates'
]

html_context.update({
    "last_release": f"v{release}",
    "github_user": "panel-extensions",
    "github_repo": "panel-material-ui",
    "default_mode": "light",
    "panelite_endpoint": jlite_url,
    "gallery_url": gallery_url,
    "pyodide_url": pyodide_url
})

nbbuild_patterns_to_take_along = ["simple.html", "*.json", "json_*"]

# Override the Sphinx default title that appends `documentation`
html_title = f'{project} v{version}'

# Ensure the global version string includes the SHA to ensure the service
# worker is invalidated on builds between tags
if is_dev:
    version = panel.__version__

# # Patching GridItemCardDirective to be able to substitute the domain name
# # in the link option.
# from sphinx_design.cards import CardDirective
# from sphinx_design.grids import GridItemCardDirective

# orig_grid_run = GridItemCardDirective.run

# def patched_grid_run(self):
#     app = self.state.document.settings.env.app
#     existing_link = self.options.get('link')
#     domain = getattr(app.config, 'grid_item_link_domain', None)
#     if self.has_content:
#         self.content.replace('|gallery-endpoint|', domain)
#     if existing_link and domain:
#         new_link = existing_link.replace('|gallery-endpoint|', domain)
#         self.options['link'] = new_link
#     return list(orig_grid_run(self))

# GridItemCardDirective.run = patched_grid_run

# orig_card_run = CardDirective.run

# def patched_card_run(self):
#     app = self.state.document.settings.env.app
#     existing_link = self.options.get('link')
#     domain = getattr(app.config, 'grid_item_link_domain', None)
#     if existing_link and domain:
#         new_link = existing_link.replace('|gallery-endpoint|', domain)
#         self.options['link'] = new_link
#     return orig_card_run(self)

# CardDirective.run = patched_card_run

def _get_pyodide_version():
    if PYODIDE_VERSION.startswith("v"):
        return PYODIDE_VERSION[1:]
    raise NotImplementedError(F"{PYODIDE_VERSION=} is not valid")

def update_versions(app, docname, source):
    # Inspired by: https://stackoverflow.com/questions/8821511
    version_replace = {
        "{{PANEL_VERSION}}" : PY_VERSION,
        "{{BOKEH_VERSION}}" : BOKEH_VERSION,
        "{{PYSCRIPT_VERSION}}" : PYSCRIPT_VERSION,
        "{{PYODIDE_VERSION}}" : _get_pyodide_version()
    }

    for old, new in version_replace.items():
        source[0] = source[0].replace(old, new)


def setup_mystnb(app):
    from myst_nb.core.config import NbParserConfig
    from myst_nb.sphinx_ import (
        HideCodeCellNode, HideInputCells, SelectMimeType,
    )
    from myst_nb.sphinx_ext import create_mystnb_config

    _UNSET = "--unset--"
    for name, default, field in NbParserConfig().as_triple():
        if not field.metadata.get("sphinx_exclude"):
            # TODO add types?
            app.add_config_value(f"nb_{name}", default, "env", Any)  # type: ignore[arg-type]
            if "legacy_name" in field.metadata:
                app.add_config_value(
                    f"{field.metadata['legacy_name']}",
                    _UNSET,
                    "env",
                    Any,  # type: ignore[arg-type]
                )
    app.add_config_value("nb_render_priority", _UNSET, "env", Any)  # type: ignore[arg-type]
    create_mystnb_config(app)

    # add post-transform for selecting mime type from a bundle
    app.add_post_transform(SelectMimeType)

    # setup collapsible content
    app.add_post_transform(HideInputCells)
    HideCodeCellNode.add_to_app(app)


def generate_demo(app):
    subprocess.run(["python", pathlib.Path(__file__).parent / "_scripts" / "demo.py"], check=True)

def setup(app) -> None:
    try:
        from nbsite.paramdoc import param_formatter, param_skip
        app.connect('autodoc-process-docstring', param_formatter)
        app.connect('autodoc-skip-member', param_skip)
    except ImportError:
        print('no param_formatter (no param?)')

    app.connect('builder-inited', setup_mystnb)
    app.connect("builder-inited", generate_demo)

    app.connect('source-read', update_versions)
    nbbuild.setup(app)
    app.add_config_value('grid_item_link_domain', '', 'html')

    # hv_sidebar_dropdown
    app.add_config_value('nbsite_hv_sidebar_dropdown', {}, 'html')
    app.connect("html-page-context", add_hv_sidebar_dropdown_context)


grid_item_link_domain = gallery_endpoint
