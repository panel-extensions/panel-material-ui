"""
Conformance tests for the component interface (see utils.js). Each test runs
a probe component on both hosts that implement the interface, the Panel view
and a Compiled tree, and expects the same observable behaviour.
"""
import sys

import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui import Button, Compiled
from panel_material_ui._probe import Probe

pytestmark = pytest.mark.ui

PROBE = "window.pmui_probes[{key!r}]"


@pytest.fixture(params=["panel", "compiled"])
def serve(request, page, monkeypatch):
    # The Panel host is what renders a component that is served uncompiled.
    monkeypatch.setattr(sys.modules["panel_material_ui.base"], "COMPILE", False)

    def serve(component):
        served = Compiled(component) if request.param == "compiled" else component
        serve_component(page, served)
        expect(page.locator(".probe").first).to_be_visible()
        return served
    return serve


def probe(page, key, expression):
    return page.evaluate(f"() => {{ const probe = window.pmui_probes[{key!r}]; return {expression} }}")


def tree():
    child = Probe(key="child", sizing_mode="stretch_width", height=40)
    button = Button(label="Sibling", width=120)
    parent = Probe(key="parent", direction="row", objects=[child, button], width=600, height=80)
    return parent, child, button


def test_model_identity(page, serve):
    parent, _, _ = tree()
    serve(parent)

    assert probe(page, "parent", "typeof probe.model.id") == "string"
    assert probe(page, "parent", "probe.model.id !== window.pmui_probes.child.model.id")
    assert probe(page, "parent", "probe.model.kind") == "Probe"
    assert probe(page, "parent", "typeof probe.model.constants") == "object"


def test_state_from_python(page, serve):
    parent, child, _ = tree()
    serve(parent)

    child.value = 4

    expect(page.locator('.probe[data-key="child"] > .probe-value')).to_have_text("4")
    assert probe(page, "child", "probe.model.get('value')") == 4
    assert probe(page, "child", "probe.model.value") == 4
    wait_until(lambda: probe(page, "child", "probe.changes") == 1, page)
    assert probe(page, "parent", "probe.changes") == 0


def test_state_to_python(page, serve):
    parent, child, _ = tree()
    serve(parent)

    probe(page, "child", "probe.setValue(7)")

    expect(page.locator('.probe[data-key="child"] > .probe-value')).to_have_text("7")
    wait_until(lambda: child.value == 7, page)
    assert parent.value == 0


def test_set_without_sync_stays_local(page, serve):
    parent, child, _ = tree()
    serve(parent)

    probe(page, "child", "probe.model.set({value: 3}, {sync: false})")
    expect(page.locator('.probe[data-key="child"] > .probe-value')).to_have_text("3")
    page.wait_for_timeout(200)
    assert child.value == 0

    probe(page, "child", "probe.model.set({value: 5})")
    wait_until(lambda: child.value == 5, page)


def test_unknown_state_raises(page, serve):
    parent, _, _ = tree()
    serve(parent)

    error = probe(page, "parent", "(() => { try { probe.model.useState('missing') } catch (e) { return e.name } })()")
    assert error == "ReferenceError"


def test_child_handles(page, serve):
    parent, child, _ = tree()
    serve(parent)

    assert probe(page, "parent", "probe.model.children('objects').map(child => child.kind)") == ["Probe", "Button"]
    assert probe(page, "parent", "probe.model.children('objects')[0].id === window.pmui_probes.child.model.id")
    assert probe(page, "parent", "probe.model.children('objects')[0].layout.sizing_mode") == "stretch_width"
    assert probe(page, "parent", "probe.model.children('objects')[1].layout.width") == 120
    assert probe(page, "parent", "probe.model.children('objects')[1].get('label')") == "Sibling"
    assert probe(page, "parent", "probe.model.children('missing')") == []


def test_children_are_sized_along_the_direction(page, serve):
    parent, _, _ = tree()
    serve(parent)

    def boxes():
        return probe(page, "child", "[probe.host.host_el.getBoundingClientRect().width, window.pmui_probes.parent.host.host_el.getBoundingClientRect().width]")
    # The stretching child takes what the fixed sibling and its margin leave.
    wait_until(lambda: 400 < boxes()[0] < 480 and boxes()[1] == 600, page)

    parent.direction = "column"
    wait_until(lambda: boxes()[0] == 600, page)


def test_message_from_python_and_unsubscribe(page, serve):
    parent, child, _ = tree()
    serve(parent)

    child._send_msg({"hello": 1})
    wait_until(lambda: probe(page, "child", "probe.msgs") == [{"hello": 1}], page)
    assert probe(page, "parent", "probe.msgs") == []

    probe(page, "child", "probe.stop()")
    child._send_msg({"hello": 2})
    child.value = 9
    expect(page.locator('.probe[data-key="child"] > .probe-value')).to_have_text("9")
    assert probe(page, "child", "probe.msgs") == [{"hello": 1}]
    assert probe(page, "child", "probe.changes") == 0


def test_message_and_event_to_python(page, serve):
    parent, child, _ = tree()
    serve(parent)

    probe(page, "child", "probe.model.send_msg({answer: 42})")
    wait_until(lambda: child.received == [{"answer": 42}], page)
    assert parent.received == []

    probe(page, "child", """(() => {
      const target = probe.host.content_el.querySelector('.probe-value') ?? probe.host.content_el
      target.addEventListener('click', (event) => probe.model.send_event('click', event), {once: true})
      target.dispatchEvent(new MouseEvent('click', {bubbles: true, clientX: 5}))
    })()""")
    wait_until(lambda: len(child.events) == 1, page)
    event = child.events[0]
    assert event.node == "click"
    # The payload is the serialized DOM event, hosts may differ in detail.
    assert event.data["target"] is not None


def test_host_elements(page, serve):
    parent, _, _ = tree()
    serve(parent)

    own = "probe.host.host_el.querySelector('.probe[data-key=\"child\"]') ?? probe.host.host_el.shadowRoot?.querySelector('.probe[data-key=\"child\"]')"
    assert probe(page, "child", f"({own}) != null")
    assert probe(page, "child", "probe.host.content_el.querySelector('.probe[data-key=\"child\"]') != null")
    # A sibling's output is not inside this component's elements.
    assert probe(page, "child", "probe.host.content_el.querySelector('.MuiButton-root') == null")
    assert probe(page, "child", "probe.host.style_root instanceof ShadowRoot")
    # MUI accepts an element or a function that returns one as a container.
    assert probe(page, "child", "['function', 'object'].includes(typeof probe.host.overlay_root)")
    assert probe(page, "child", "typeof probe.host.shares_style_root") == "boolean"
    assert probe(page, "child", "probe.host.layout.sizing_mode") == "stretch_width"
    assert probe(page, "child", "probe.host.layout.height") == 40


def test_host_tree(page, serve):
    parent, _, _ = tree()
    serve(parent)

    assert probe(page, "child", "probe.host.parent.model.id === window.pmui_probes.parent.model.id")
    assert probe(page, "child", "probe.host.parent.model.kind") == "Probe"
    assert probe(page, "child", "probe.host.parent.has_child(probe.host)")
    assert not probe(page, "child", "probe.host.has_child(window.pmui_probes.parent.host)")
    assert not probe(page, "child", "probe.host.is_root")
    assert probe(page, "parent", "probe.host.is_root")
    assert probe(page, "parent", "probe.host.is_document_root")
    assert not probe(page, "child", "probe.host.is_document_root")


def test_host_style_does_not_leak(page, serve):
    parent, _, _ = tree()
    serve(parent)

    probe(page, "child", "probe.host.host_el.style.opacity = '0.5'")
    assert page.locator('.probe[data-key="child"]').evaluate(
        "el => { let node = el, opacity = 1; while (node) { if (node instanceof Element) { opacity *= getComputedStyle(node).opacity } node = node.parentNode ?? node.host } return opacity }"
    ) == 0.5
    assert page.locator(".MuiButton-root").evaluate(
        "el => { let node = el, opacity = 1; while (node) { if (node instanceof Element) { opacity *= getComputedStyle(node).opacity } node = node.parentNode ?? node.host } return opacity }"
    ) == 1


def test_remove_event(page, serve):
    parent, child, button = tree()
    serve(parent)
    page.evaluate("() => { window.pmui_child = window.pmui_probes.child }")

    parent.objects = [button]

    expect(page.locator('.probe[data-key="child"]')).to_have_count(0)
    wait_until(lambda: page.evaluate("() => window.pmui_child.removed"), page)
