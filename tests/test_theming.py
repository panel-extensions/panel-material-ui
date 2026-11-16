import pytest
from panel.config import config

from panel_material_ui.layout import Column
from panel_material_ui.template import Page, ThemeToggle
from panel_material_ui.widgets import Button


@pytest.fixture(autouse=True)
def reset_theme():
    original = config._theme_
    try:
        yield
    finally:
        config._theme_ = original


def test_component_dark_theme_does_not_set_global_theme():
    Button(dark_theme=True)
    assert config._theme_ is None
    assert config.theme == 'default'
    assert not Button().dark_theme


def test_component_dark_theme_does_not_set_session_theme(server_document):
    Button(dark_theme=True)
    assert config.theme == 'default'


def test_dark_theme_propagates_to_children():
    button = Button()
    Column(button, dark_theme=True)
    assert button.dark_theme


def test_dark_theme_does_not_override_explicit_child():
    inner = Button(dark_theme=True)
    Column(inner, dark_theme=False)
    assert inner.dark_theme


def test_explicit_child_shields_its_descendants():
    button = Button()
    inner = Column(button, dark_theme=True)
    Column(inner, dark_theme=False)
    assert inner.dark_theme
    assert button.dark_theme


def test_page_dark_theme_sets_session_theme(server_document):
    button = Button()
    Page(main=[button], dark_theme=True)
    assert config.theme == 'dark'
    assert button.dark_theme
    assert Button().dark_theme


def test_page_without_dark_theme_does_not_set_global_theme():
    Page()
    assert config._theme_ is None


def test_theme_toggle_default_does_not_pin_global_theme():
    ThemeToggle()
    assert config._theme_ is None


def test_theme_toggle_value_sets_session_theme(server_document):
    toggle = ThemeToggle()
    toggle.value = True
    assert config.theme == 'dark'
    assert toggle.theme == 'dark'


def test_page_dark_theme_updates_rendered_components(server_document):
    button = Button()
    other = Button()
    page = Page(main=[button])
    page.get_root(server_document)
    other.get_root(server_document)

    page.dark_theme = True

    assert button.dark_theme
    assert other.dark_theme
    assert config.theme == 'dark'


def test_theme_toggle_updates_rendered_components(server_document):
    button = Button()
    toggle = ThemeToggle()
    col = Column(toggle, button)
    col.get_root(server_document)

    toggle.value = True

    assert button.dark_theme
    assert toggle.dark_theme


def test_external_esm_imports_error_boundary_from_bundle():
    from panel_material_ui.base import MaterialUIComponent

    class _External(MaterialUIComponent):
        _esm = "export function render() { return null }"

    esm = _External._render_esm_base()
    assert 'const ComponentErrorBoundary = pnmui.ComponentErrorBoundary;' in esm
    assert 'from "./utils"' not in esm
