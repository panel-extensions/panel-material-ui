import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Card, Column, Dialog, Paper
from panel_material_ui.pane import Typography
from panel_material_ui.widgets import Button, TextInput
from panel_material_ui.wrappers import Fullscreen
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def _app(**params):
    paper = Paper(Typography("Dashboard"), sizing_mode="stretch_both")
    wrapper = Fullscreen(paper, height=200, width=300, **params)
    header = Button(label="Outside")
    return Column(header, wrapper), wrapper


def _native(page):
    return page.evaluate("(document.fullscreenElement ?? null) !== null")


_TOGGLE = "document.dispatchEvent(new CustomEvent('pmui:fullscreen-toggle', {cancelable: true}))"


def _wait_connected(page, count=1):
    expect(page.locator("[data-pmui-fullscreen-host]")).to_have_count(count)


def _covers(page):
    viewport = page.viewport_size
    box = page.locator("[data-pmui-fullscreen]").bounding_box()
    return box == {"x": 0, "y": 0, "width": viewport["width"], "height": viewport["height"]}


def test_fullscreen_button_enters_and_browser_exit_syncs_back(page):
    layout, wrapper = _app()
    serve_component(page, layout)

    wait_until(lambda: wrapper.supported, page)
    page.get_by_role("button", name="Enter full screen").click()
    wait_until(lambda: wrapper.active and wrapper.native, page)
    wait_until(lambda: _native(page), page)
    wait_until(lambda: _covers(page), page)
    expect(page.get_by_role("button", name="Exit full screen")).to_be_attached()

    page.evaluate("document.exitFullscreen()")
    wait_until(lambda: not wrapper.active and not wrapper.native, page)
    expect(page.locator("[data-pmui-fullscreen]")).to_have_count(0)


def test_fullscreen_exit_button_leaves(page):
    layout, wrapper = _app()
    serve_component(page, layout)

    page.get_by_role("button", name="Enter full screen").click()
    wait_until(lambda: wrapper.native, page)
    page.mouse.move(100, 100)
    page.get_by_role("button", name="Exit full screen").click()
    wait_until(lambda: not wrapper.active, page)
    wait_until(lambda: not _native(page), page)


def test_fullscreen_active_from_server_covers_window(page):
    layout, wrapper = _app()
    serve_component(page, layout)

    wrapper.active = True
    wait_until(lambda: _covers(page), page)
    page.evaluate("document.fullscreenElement && document.exitFullscreen()")
    wait_until(lambda: not wrapper.active, page)
    expect(page.locator("[data-pmui-fullscreen]")).to_have_count(0)


def test_fullscreen_escape_while_typing_does_not_leave(page):
    paper = Paper(TextInput(label="Name"), sizing_mode="stretch_both")
    wrapper = Fullscreen(paper, height=200, width=300, active=True)
    serve_component(page, wrapper)

    wait_until(lambda: _covers(page), page)
    page.get_by_label("Name").click()
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    assert wrapper.active


def test_fullscreen_without_api_covers_window(page):
    # As on iPhone Safari, which offers no full screen for elements.
    page.add_init_script("""
      for (const name of ["fullscreenEnabled", "webkitFullscreenEnabled"]) {
        Object.defineProperty(Document.prototype, name, {get: () => false})
      }
    """)
    layout, wrapper = _app()
    serve_component(page, layout)

    page.get_by_role("button", name="Enter full screen").click()
    wait_until(lambda: wrapper.active, page)
    wait_until(lambda: _covers(page), page)
    assert not wrapper.supported
    assert not _native(page)
    assert page.evaluate("document.documentElement.style.overflow") == "hidden"

    # Escape leaves the cover, as the browser does for real full screen.
    page.keyboard.press("Escape")
    wait_until(lambda: not wrapper.active, page)
    expect(page.locator("[data-pmui-fullscreen]")).to_have_count(0)
    assert page.evaluate("document.documentElement.style.overflow") == ""


def test_fullscreen_makes_rest_of_page_inert(page):
    layout, wrapper = _app()
    serve_component(page, layout)

    outside = page.get_by_role("button", name="Outside")
    expect(outside).to_be_visible()
    wrapper.active = True
    wait_until(lambda: _covers(page), page)
    wait_until(lambda: page.evaluate("""() => {
      const inert = [];
      const walk = (root) => root.querySelectorAll("*").forEach((el) => {
        if (el.inert) inert.push(el);
        if (el.shadowRoot) walk(el.shadowRoot);
      });
      walk(document);
      return inert.length > 0;
    }"""), page)

    wrapper.active = False
    wait_until(lambda: page.evaluate("""() => {
      let found = false;
      const walk = (root) => root.querySelectorAll("*").forEach((el) => {
        if (el.inert) found = true;
        if (el.shadowRoot) walk(el.shadowRoot);
      });
      walk(document);
      return !found;
    }"""), page)
    outside.click()


def test_fullscreen_toggle_class_outside(page):
    header = Button(label="Present", css_classes=["present-toggle"])
    wrapper = Fullscreen(
        Paper(Typography("Dashboard"), sizing_mode="stretch_both"),
        height=200, width=300, show_button=False, toggle_class="present-toggle",
    )
    serve_component(page, Column(header, wrapper))

    expect(page.get_by_role("button", name="Enter full screen")).to_have_count(0)
    page.get_by_role("button", name="Present").click()
    wait_until(lambda: wrapper.native, page)
    # The page outside is inert in full screen, so the toggle there no longer takes clicks.
    page.evaluate("document.exitFullscreen()")
    wait_until(lambda: not wrapper.active and not wrapper.native, page)


def test_fullscreen_toggle_event(page):
    layout, wrapper = _app()
    serve_component(page, layout)
    _wait_connected(page)

    page.evaluate(_TOGGLE)
    wait_until(lambda: wrapper.active, page)
    page.evaluate(_TOGGLE)
    wait_until(lambda: not wrapper.active, page)


def test_fullscreen_toggle_event_chooses_clicked_wrapper(page):
    a = Fullscreen(Paper(Typography("Alpha text"), sizing_mode="stretch_both"), height=100, width=300)
    b = Fullscreen(Paper(Typography("Beta text"), sizing_mode="stretch_both"), height=100, width=300)
    serve_component(page, Column(a, b))
    _wait_connected(page, 2)

    page.get_by_text("Beta text").click()
    page.evaluate(_TOGGLE)
    wait_until(lambda: a.active or b.active, page)
    assert b.active and not a.active


def test_fullscreen_exit_class_inside(page):
    exit_button = Button(label="Done", css_classes=[Fullscreen.EXIT_CLASS])
    wrapper = Fullscreen(
        Paper(exit_button, sizing_mode="stretch_both"), height=200, width=300, active=True,
    )
    serve_component(page, wrapper)

    wait_until(lambda: _covers(page), page)
    page.get_by_role("button", name="Done").click()
    wait_until(lambda: not wrapper.active, page)


def test_fullscreen_disabled_blocks_entering(page):
    layout, wrapper = _app(disabled=True)
    serve_component(page, layout)

    expect(page.get_by_role("button", name="Enter full screen")).to_be_disabled()
    _wait_connected(page)
    page.evaluate(_TOGGLE)
    page.wait_for_timeout(200)
    assert not wrapper.active


def test_fullscreen_toolbar_hides_while_idle(page):
    wrapper = Fullscreen(
        Paper(Typography("Dashboard"), sizing_mode="stretch_both"),
        toolbar=[Typography("Status OK")], hide_delay=1000, height=200, width=300, label="Report toolbar",
    )
    serve_component(page, wrapper)

    expect(page.get_by_text("Status OK")).to_have_count(0)
    wrapper.active = True
    overlay = page.get_by_role("region", name="Report toolbar")
    page.mouse.move(150, 150)
    expect(overlay).to_contain_text("Status OK")
    expect(overlay).to_have_css("opacity", "1")
    page.mouse.move(10, 10)
    expect(overlay).to_have_css("opacity", "0")
    page.mouse.move(150, 150)
    expect(overlay).to_have_css("opacity", "1")


def test_fullscreen_uses_theme_background(page):
    wrapper = Fullscreen(
        Typography("Dashboard"), height=200, width=300, active=True, dark_theme=True,
    )
    serve_component(page, wrapper)

    wait_until(lambda: _covers(page), page)
    background = page.locator("[data-pmui-fullscreen]").evaluate("el => getComputedStyle(el).backgroundColor")
    assert background == "rgb(18, 18, 18)"


def test_fullscreen_stretches_responsive_child_beyond_fixed_height(page):
    layout, wrapper = _app()
    serve_component(page, layout)

    wrapper.active = True
    wait_until(lambda: _covers(page), page)
    viewport = page.viewport_size
    paper = page.locator(".MuiPaper-root").first
    wait_until(lambda: paper.bounding_box()["height"] == viewport["height"], page)


_FOCUSED_LABEL = """() => {
  let node = document.activeElement
  while (node?.shadowRoot?.activeElement) node = node.shadowRoot.activeElement
  if (!node || node === document.body) return "body"
  if (node.classList.contains("pmui-fullscreen")) return "wrapper"
  return (node.getAttribute("aria-label") || node.textContent || "").trim()
}"""


@pytest.mark.parametrize("trigger", ["toggle_class", "event"])
def test_fullscreen_moves_focus_in_and_restores_it_on_exit(page, trigger):
    header = Button(label="Present", css_classes=["present-toggle"])
    wrapper = Fullscreen(
        Paper(Typography("Dashboard"), sizing_mode="stretch_both"),
        height=200, width=300, show_button=False, toggle_class="present-toggle",
    )
    serve_component(page, Column(header, wrapper))

    present = page.get_by_role("button", name="Present")
    if trigger == "toggle_class":
        present.click()
    else:
        _wait_connected(page)
        present.focus()
        page.evaluate(_TOGGLE)
    wait_until(lambda: wrapper.active, page)
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "wrapper", page)

    page.evaluate("document.fullscreenElement ? document.exitFullscreen() : null")
    wrapper.active = False
    wait_until(lambda: not wrapper.active, page)
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "Present", page)


def _overlaps(a, b):
    return not (
        a["x"] + a["width"] <= b["x"] or b["x"] + b["width"] <= a["x"]
        or a["y"] + a["height"] <= b["y"] or b["y"] + b["height"] <= a["y"]
    )


def test_fullscreen_button_visible_at_rest(page):
    layout, wrapper = _app()
    serve_component(page, layout)

    page.mouse.move(600, 600)
    overlay = page.locator(".pmui-fullscreen-overlay")
    expect(overlay).to_have_css("opacity", "1")
    expect(page.get_by_role("button", name="Enter full screen")).to_be_visible()


def _card_app(**params):
    card = Card(Typography("Revenue"), title="Dashboard card", collapsible=True, sizing_mode="stretch_both")
    return Fullscreen(card, height=250, width=400, **params)


def test_fullscreen_button_sits_beside_card_header_actions(page):
    serve_component(page, _card_app())

    chevron = page.get_by_role("button", name="show more")
    toggle = page.get_by_role("button", name="Enter full screen")
    expect(chevron).to_be_visible()
    wait_until(lambda: not _overlaps(toggle.bounding_box(), chevron.bounding_box()), page)
    toggle_box, chevron_box = toggle.bounding_box(), chevron.bounding_box()
    assert toggle_box["x"] + toggle_box["width"] <= chevron_box["x"]
    centers = [b["y"] + b["height"] / 2 for b in (toggle_box, chevron_box)]
    assert abs(centers[0] - centers[1]) <= 2


def test_fullscreen_toolbar_does_not_cover_card_header_actions(page):
    wrapper = _card_app(toolbar=[Typography("Live")], hide_delay=None)
    serve_component(page, wrapper)

    wrapper.active = True
    wait_until(lambda: _covers(page), page)
    chevron = page.get_by_role("button", name="show more")
    toolbar = page.locator(".pmui-fullscreen-overlay")
    expect(toolbar).to_contain_text("Live")
    wait_until(lambda: not _overlaps(toolbar.bounding_box(), chevron.bounding_box()), page)
    chevron.click()


def test_fullscreen_tab_order_matches_card_header_order(page):
    serve_component(page, _card_app())

    toggle = page.get_by_role("button", name="Enter full screen")
    chevron = page.get_by_role("button", name="show more")
    wait_until(lambda: toggle.bounding_box()["x"] < chevron.bounding_box()["x"], page)
    order = []
    for _ in range(4):
        page.keyboard.press("Tab")
        order.append(page.evaluate("""() => {
          let node = document.activeElement
          while (node?.shadowRoot?.activeElement) node = node.shadowRoot.activeElement
          return node?.getAttribute("aria-label") ?? ""
        }"""))
    assert order.index("Enter full screen") < order.index("show more"), order


@pytest.mark.parametrize("active", [False, True])
def test_fullscreen_click_inside_keeps_tab_order(page, active):
    wrapper = Fullscreen(
        Column(
            Button(label="First"),
            Typography("Some text", css_classes=["text"]),
            Button(label="Second"),
            sizing_mode="stretch_both",
        ),
        height=200, width=300, show_button=False, active=active,
    )
    serve_component(page, Column(Button(label="Outside"), wrapper))

    if active:
        wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "wrapper", page)
    page.get_by_text("Some text").click()
    assert page.evaluate(_FOCUSED_LABEL) != "wrapper"
    page.keyboard.press("Tab")
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "Second", page)


_BOX_TABINDEX = """() => {
  const find = (root) => {
    for (const el of root.querySelectorAll("*")) {
      if (el.classList.contains("pmui-fullscreen")) return el
      if (el.shadowRoot) { const found = find(el.shadowRoot); if (found) return found }
    }
    return null
  }
  return find(document).getAttribute("tabindex")
}"""


def test_fullscreen_tab_moves_focus_on_from_box(page):
    wrapper = Fullscreen(
        Column(Button(label="First"), Typography("Some text"), Button(label="Second"), sizing_mode="stretch_both"),
        height=200, width=300, show_button=False, toggle_class="present-toggle",
    )
    serve_component(page, Column(Button(label="Present", css_classes=["present-toggle"]), wrapper))

    page.get_by_role("button", name="Present").click()
    wait_until(lambda: wrapper.active, page)
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "wrapper", page)
    assert page.evaluate(_BOX_TABINDEX) == "-1"
    page.keyboard.press("Tab")
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "First", page)
    assert page.evaluate(_BOX_TABINDEX) is None
    page.keyboard.press("Tab")
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "Second", page)
    page.keyboard.press("Shift+Tab")
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "First", page)


def test_fullscreen_dialog_returns_focus_to_box(page):
    dialog = Dialog(Button(label="Inside dialog"), title="Details")
    wrapper = Fullscreen(
        Paper(Column(Typography("Dashboard"), dialog), sizing_mode="stretch_both"),
        height=200, width=300, active=True,
    )
    serve_component(page, Column(Button(label="Outside"), wrapper))
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "wrapper", page)

    dialog.open = True
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) not in ("wrapper", "body"), page)
    page.keyboard.press("Escape")
    wait_until(lambda: not dialog.open, page)
    wait_until(lambda: page.evaluate(_FOCUSED_LABEL) == "wrapper", page)
    assert wrapper.active
