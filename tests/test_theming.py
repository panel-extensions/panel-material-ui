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


def test_component_dark_theme_sets_session_theme(server_document):
    Button(dark_theme=True)
    assert config.theme == 'dark'
    assert Button().dark_theme


def test_page_dark_theme_outside_session_does_not_set_global_theme():
    Page(dark_theme=True)
    ThemeToggle(value=True)
    assert config._theme_ is None


def test_dark_theme_propagates_to_children():
    button = Button()
    Column(button, dark_theme=True)
    assert button.dark_theme


def test_explicit_parent_aligns_explicit_children():
    button = Button()
    inner = Column(button, dark_theme=True)
    Column(inner, dark_theme=False)
    assert not inner.dark_theme
    assert not button.dark_theme


def test_python_dark_theme_change_applies_to_page(server_document):
    button = Button()
    other = Button()
    Column(button, other).get_root(server_document)

    button.dark_theme = True

    assert other.dark_theme
    assert config.theme == 'dark'


def test_frontend_dark_theme_change_is_not_fanned_out(server_document):
    button = Button()
    other = Button()
    Column(button, other).get_root(server_document)

    button._process_events({'dark_theme': True})

    assert button.dark_theme
    assert not other.dark_theme


def test_explicit_component_aligns_rendered_siblings(server_document):
    other = Button()
    dark = Button(dark_theme=True)
    Column(other, dark).get_root(server_document)
    callbacks = list(server_document.session_callbacks)
    assert callbacks
    for cb in callbacks:
        cb.callback()
    assert other.dark_theme


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


def test_explicit_component_follows_switched_session_theme(server_document):
    toggle = ThemeToggle()
    Column(toggle).get_root(server_document)
    toggle.value = True
    toggle.value = False

    col = Column(Button(), dark_theme=True)

    assert not col.dark_theme
    assert not col[0].dark_theme
    assert config.theme == 'default'


def test_theme_toggle_without_value_is_not_explicit():
    assert not ThemeToggle()._dark_theme_explicit
    assert ThemeToggle(value=True)._dark_theme_explicit
    assert ThemeToggle(theme='default')._dark_theme_explicit


def test_alignment_guard_is_per_thread():
    import threading

    from panel_material_ui.base import _aligning, aligning_session_theme

    seen = []
    ready, release = threading.Event(), threading.Event()

    def other():
        ready.wait(5)
        seen.append(aligning_session_theme())
        release.set()

    thread = threading.Thread(target=other)
    thread.start()
    try:
        with _aligning():
            ready.set()
            release.wait(5)
            assert aligning_session_theme()
    finally:
        ready.set()
        thread.join(5)
    assert seen == [False]


def test_python_change_only_aligns_current_session():
    from bokeh.document import Document
    from panel.io.state import set_curdoc

    shared = Button()
    doc1, doc2 = Document(), Document()
    other1, other2 = Button(), Button()
    shared.get_root(doc1)
    other1.get_root(doc1)
    shared.get_root(doc2)
    other2.get_root(doc2)

    with set_curdoc(doc1):
        shared.dark_theme = True

    assert other1.dark_theme
    assert not other2.dark_theme
