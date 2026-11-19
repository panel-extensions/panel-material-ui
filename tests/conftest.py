"""
A module containing testing utilities and fixtures.
"""
import os
import re
import socket
import unittest

from functools import cache

import pytest

from bokeh.document import Document
from bokeh.io.doc import curdoc, set_curdoc as set_bkdoc
from pyviz_comms import Comm

from panel import config, serve
from panel.io.state import set_curdoc, state
from panel.tests.util import get_open_ports

config.apply_signatures = False

if os.name != 'nt':
    import resource

    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))


for e in os.environ:
    if e.startswith(('BOKEH_', "PANEL_")) and e not in ("PANEL_LOG_LEVEL", ):
        os.environ.pop(e, None)

@cache
def internet_available(host="8.8.8.8", port=53, timeout=3):
    """Check if the internet connection is available."""
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            conn.connect((host, port))
        return True
    except socket.error:
        return False

def port_open(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    is_open = sock.connect_ex(("127.0.0.1", port)) == 0
    sock.close()
    return is_open


def get_default_port():
    worker_count = int(os.environ.get("PYTEST_XDIST_WORKER_COUNT", "1"))
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "0")
    worker_idx = int(re.sub(r"\D", "", worker_id))
    return 9001 + (worker_idx * worker_count * 10)

optional_markers = {
    "ui": {
        "help": "Runs UI related tests",
        "marker-descr": "UI test marker",
        "skip-reason": "Test only runs with the --ui option."
    },
}


def pytest_addoption(parser):
    for marker, info in optional_markers.items():
        parser.addoption(f"--{marker}", action="store_true",
                         default=False, help=info['help'])
    parser.addoption('--repeat', action='store',
        help='Number of times to repeat each test')
    parser.addoption('--compiled', action='store_true', default=False,
        help='Wraps every component a UI test serves in Compiled')


def pytest_configure(config):
    for marker, info in optional_markers.items():
        config.addinivalue_line("markers", "{}: {}".format(marker, info['marker-descr']))

    config.addinivalue_line("markers", "from_panel: mark test as being from the panel package")
    if config.getoption("--compiled"):
        _serve_compiled()
    config.addinivalue_line("markers", "internet: mark test as requiring an internet connection")


_COMPILED_RUNS: list[dict] = []


def _tree_classes(node, compiled, fallbacks):
    if node["kind"] == "fallback":
        fallbacks.append(node["slot"])
        return
    compiled.append(node["kind"])
    for value in node.get("children", {}).values():
        for child in (value if isinstance(value, list) else [value]):
            if isinstance(child, dict) and "kind" in child:
                _tree_classes(child, compiled, fallbacks)


def _serve_compiled():
    """
    Replaces the serve_component helper the UI tests import with one that
    wraps the served component in Compiled, so the whole suite doubles as a
    parity check. Set PMUI_COMPILED_REPORT to a path to get one JSON line per
    test with what was compiled, what fell back and what the browser logged.
    """
    import panel.tests.util as util

    from panel.viewable import Viewable

    from panel_material_ui import Compiled

    serve_component = util.serve_component

    def serve_compiled(page, app, *args, **kwargs):
        run = {"compiled": [], "fallbacks": [], "errors": []}
        if isinstance(app, Viewable) and not isinstance(app, Compiled):
            run["source"] = type(app).__name__
            app = Compiled(app)
            slots: list[int] = []
            _tree_classes(app.tree["root"], run["compiled"], slots)
            run["fallbacks"] = [type(app.fallbacks[slot]).__name__ for slot in slots]
        else:
            run["source"] = None
        page.on("pageerror", lambda error: run["errors"].append(str(error)[:500]))
        page.on("console", lambda msg: msg.type == "error" and run["errors"].append(msg.text[:500]))
        _COMPILED_RUNS.append(run)
        return serve_component(page, app, *args, **kwargs)

    util.serve_component = serve_compiled


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    path = os.environ.get("PMUI_COMPILED_REPORT")
    if not path or report.when != "call":
        return
    import json

    record = {
        "test": item.nodeid, "outcome": report.outcome,
        "compiled": item.config.getoption("--compiled"), "runs": list(_COMPILED_RUNS),
        "error": str(call.excinfo.value)[:1500] if call.excinfo else None,
        "line": report.longrepr.reprcrash.lineno if call.excinfo and hasattr(report.longrepr, "reprcrash") else None,
    }
    _COMPILED_RUNS.clear()
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def pytest_generate_tests(metafunc):
    repeat = getattr(metafunc.config.option, 'repeat', None)
    if repeat is not None:
        count = int(repeat)

        # We're going to duplicate these tests by parametrizing them,
        # which requires that each test has a fixture to accept the parameter.
        # We can add a new fixture like so:
        metafunc.fixturenames.append('tmp_ct')

        # Now we parametrize. This is what happens when we do e.g.,
        # @pytest.mark.parametrize('tmp_ct', range(count))
        # def test_foo(): pass
        metafunc.parametrize('tmp_ct', range(count))

def pytest_collection_modifyitems(config, items):
    skipped, selected = [], []
    markers = [m for m in optional_markers if config.getoption(f"--{m}")]
    empty = not markers
    for item in items:
        if empty and any(m in item.keywords for m in optional_markers):
            skipped.append(item)
        elif empty:
            selected.append(item)
        elif not empty and any(m in item.keywords for m in markers):
            selected.append(item)
        else:
            skipped.append(item)

    config.hook.pytest_deselected(items=skipped)
    items[:] = selected


def pytest_runtest_setup(item):
    if "internet" in item.keywords and not internet_available():
        pytest.skip("Skipping test: No internet connection")


@pytest.fixture
def context(context):
    # Set the default timeout to 20 secs
    context.set_default_timeout(20_000)
    yield context


@pytest.fixture(autouse=True)
def cleanup_panel_servers():
    """Stop threaded Panel servers after each test."""
    try:
        yield
    finally:
        state.reset()


PORT = [get_default_port()]

@pytest.fixture
def document():
    return Document()

@pytest.fixture
def server_document():
    doc = Document()
    session_context = unittest.mock.Mock()
    doc._session_context = lambda: session_context
    try:
        with set_curdoc(doc):
            yield doc
    finally:
        doc._session_context = None

@pytest.fixture
def bokeh_curdoc():
    old_doc = curdoc()
    doc = Document()
    session_context = unittest.mock.Mock()
    doc._session_context = lambda: session_context
    set_bkdoc(doc)
    try:
        yield doc
    finally:
        set_bkdoc(old_doc)

@pytest.fixture
def comm():
    return Comm()


@pytest.fixture
def port():
    return get_open_ports()[0]
