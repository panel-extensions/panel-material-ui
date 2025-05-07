import pathlib
from io import StringIO

import pytest

import panel_material_ui as pmui
from panel.config import config
from panel.io.resources import CDN_DIST

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

    assert (
        f"""<link rel="icon" href="{CDN_DIST}images/favicon.ico">"""
        in html
    )
    assert (
        f"""<link rel="apple-touch-icon" href="{CDN_DIST}images/apple-touch-icon.png">"""
        in html
    )
    assert """<meta name="name" content="Meta00""" in html
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

def test_logo():
    page = pmui.Page(logo=STATIC_PATH / "logo_horizontal_light_theme.png")
    model = page.get_root()
    assert model.data.logo.startswith("data:image/png;")
