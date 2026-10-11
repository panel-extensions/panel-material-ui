import pytest

pytest.importorskip("playwright")

from panel.config import config
from panel.tests.util import serve_component
from playwright.sync_api import expect

from panel_material_ui.widgets import Button, DatePicker

pytestmark = pytest.mark.ui


def _record_requests(page):
    requests = []
    page.on("request", lambda request: requests.append(request.url))
    return requests


def test_lazy_widget_chunk_not_loaded_when_unused(page):
    requests = _record_requests(page)
    serve_component(page, Button(label="Click"))

    expect(page.locator(".MuiButton-root")).to_have_count(1)
    assert not any("DateTimePicker-" in url for url in requests)


def test_lazy_widget_chunk_loaded_on_render(page):
    requests = _record_requests(page)
    serve_component(page, DatePicker(label="Date"))

    expect(page.locator(".MuiPickersInputBase-root, .MuiInputBase-root")).to_have_count(1)
    assert any("DateTimePicker-" in url for url in requests)


def test_lazy_widget_renders_in_inlined_output(page, tmp_path):
    # Inlined bundles are imported from a blob, so they have to include the
    # lazily loaded widgets instead of loading them from chunks
    filename = tmp_path / "date.html"
    inline = config.inline
    config.inline = True
    try:
        DatePicker(label="Date").save(filename, resources="inline")
    finally:
        config.inline = inline

    page.goto(filename.as_uri())
    expect(page.locator("label", has_text="Date")).to_have_count(1)


def test_lazy_widget_chunk_loaded_from_cdn(page, monkeypatch):
    # Releases load the bundle from the CDN, where the chunks have to be
    # resolved relative to the bundle url, so serve the local build there
    from importlib import import_module
    from types import SimpleNamespace

    from panel_material_ui.base import CDN_BASE, DIST_PATH

    # The package exports a wrappers submodule under the same name
    base = import_module("panel_material_ui.base")
    monkeypatch.setattr(base, "IS_RELEASE", True)
    monkeypatch.setattr(base, "_settings", SimpleNamespace(resources=lambda default=None: "cdn"))

    def fulfill(route):
        path = DIST_PATH / route.request.url.split("?")[0].rsplit("/", 1)[-1]
        if not path.is_file():
            return route.fulfill(status=404)
        content_type = "text/css" if path.suffix == ".css" else "text/javascript"
        route.fulfill(path=path, content_type=content_type)

    page.route(f"{CDN_BASE}/*", fulfill)
    requests = _record_requests(page)
    serve_component(page, DatePicker(label="Date"))

    expect(page.locator("label", has_text="Date")).to_have_count(1)
    assert any(url.startswith(f"{CDN_BASE}/panel-material-ui.bundle.js") for url in requests)
    assert any(url.startswith(f"{CDN_BASE}/DateTimePicker-") for url in requests)
