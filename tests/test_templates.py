import pathlib
import re
from io import StringIO

import pytest

import panel_material_ui as pmui
from panel.config import config
from panel.io.resources import CDN_DIST
from panel_material_ui.base import _env
from panel_material_ui.theme import PANEL_DESIGN_HOOKS

STATIC_PATH = pathlib.Path(__file__).parent.parent / "doc" / "_static"


def _to_html(page: pmui.Page):
    export = StringIO()
    with config.set(inline=False):
        page.save(export)
    export.seek(0)
    return export.read()


def _render_page(**kwargs) -> str:
    """
    Render the page with the given meta information.
    """
    page = pmui.Page(**kwargs)
    return _to_html(page)


def test_default_page_parameters():
    html = _render_page()

    # Panel's base template (Panel >= 1.10) also declares the icon sizes.
    assert re.search(f'<link rel="icon"[^>]* href="{CDN_DIST}images/favicon.ico">', html)
    assert re.search(f'<link rel="apple-touch-icon"[^>]* href="{CDN_DIST}images/apple-touch-icon.png">', html)
    assert not """<meta name="name" """ in html
    assert not """<meta name="description" """ in html
    assert not """<meta name="keywords" """ in html
    assert not """<meta name="author" """ in html
    assert """<meta name="viewport" content="width=device-width, initial-scale=1.0">""" in html
    assert not """<meta http-equiv="refresh" """ in html


@pytest.mark.parametrize(
    "key, value, expected",
    [
        (
            "meta_name", "My Name", """<meta name="name" content="My Name">"""
        ),
        (
            "meta_description", "My Description", """<meta name="description" content="My Description">"""
        ),
        (
            "meta_keywords", "kw1,kw2", """<meta name="keywords" content="kw1,kw2">"""
        ),
        (
            "meta_author", "My Author", """<meta name="author" content="My Author">"""
        ),
        (
            "meta_viewport", "width=device-width, initial-scale=1.5", """<meta name="viewport" content="width=device-width, initial-scale=1.5">"""
        ),
        (
            "meta_refresh", "30", """<meta http-equiv="refresh" content="30">"""
        ),
        (
        "meta_icon",
            "https://www.wikipedia.org/static/favicon/wikipedia.ico",
            """<link rel="icon" href="https://www.wikipedia.org/static/favicon/wikipedia.ico">""",
        ),
        (
            "meta_apple_touch_icon",
            "https://www.wikipedia.org/static/apple-touch/wikipedia.png",
            """<link rel="apple-touch-icon" href="https://www.wikipedia.org/static/apple-touch/wikipedia.png">""",
        ),
        (
            "raw_css", ["body { background-color: red; }"], """body { background-color: red; }"""
        ),
    ],
)
def test_custom_page_parameters(key, value, expected):
    html = _render_page(**{key: value})
    assert expected in html


def test_favicon():
    html = _render_page(favicon=STATIC_PATH / "icons" / "icon-16x16.png")
    assert """<link rel="icon" href="data:image/png;""" in html


@pytest.mark.skipif(not PANEL_DESIGN_HOOKS, reason='Requires Panel shared base template')
def test_custom_legacy_page_template():
    html = _render_page(
        template=_env.get_template('base.html'),
        favicon='https://example.com/favicon.ico',
        meta_apple_touch_icon='https://example.com/apple-touch.png',
    )
    assert '<link rel="icon" href="https://example.com/favicon.ico">' in html
    assert '<link rel="apple-touch-icon" href="https://example.com/apple-touch.png">' in html
    assert 'data-theme-managed="true"' in html
    assert f'<link rel="stylesheet" href="{CDN_DIST}bundled/theme/default.css">' not in html


def test_logo():
    page = pmui.Page(logo=STATIC_PATH / "logo_horizontal_light_theme.png")
    model = page.get_root()
    assert model.data.logo.startswith("data:image/png;")


def test_page_defaults_to_stretch_width():
    assert pmui.Page().sizing_mode == "stretch_width"


@pytest.mark.parametrize("kwargs", [{"width": 500}, {"sizing_mode": "fixed"}, {"max_width": 800}])
def test_page_explicit_width_keeps_sizing(kwargs):
    assert pmui.Page(**kwargs).sizing_mode != "stretch_width"
