import panel as pn
import param
import pytest

pytest.importorskip('playwright')

from panel.custom import Children, JSComponent
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui import (
    Button,
    Checkbox,
    Column,
    Compiled,
    Page,
    Row,
    TextInput,
    Typography,
)

pytestmark = pytest.mark.ui


def test_compiled_click_updates_other_node(page):
    status = Typography("clicks: 0", css_classes=["status"])
    button = Button(label="Run")
    button.on_click(lambda event: status.param.update(object=f"clicks: {button.clicks}"))
    serve_component(page, Compiled(Column(status, Row(button))))

    page.locator(".MuiButton-root").click()
    expect(page.locator(".status")).to_contain_text("clicks: 1")
    page.locator(".MuiButton-root").click()
    expect(page.locator(".status")).to_contain_text("clicks: 2")


def test_compiled_patch_keeps_sibling_dom(page):
    first, second = Button(label="First"), Button(label="Second")
    serve_component(page, Compiled(Column(Row(first, second))))

    buttons = page.locator(".MuiButton-root")
    expect(buttons).to_have_count(2)
    handle = buttons.nth(1).element_handle()
    first.label = "Renamed"
    expect(buttons.nth(0)).to_have_text("Renamed")
    assert handle.evaluate("el => el.isConnected")


def test_compiled_text_input_syncs_both_ways(page):
    text = TextInput(value="a")
    serve_component(page, Compiled(Column(text)))

    field = page.locator("input")
    expect(field).to_have_value("a")
    field.fill("typed")
    field.press("Enter")
    wait_until(lambda: text.value == "typed", page)
    text.value = "from python"
    expect(field).to_have_value("from python")


def test_compiled_checkbox_syncs_both_ways(page):
    checkbox = Checkbox(label="On", value=False)
    serve_component(page, Compiled(Column(checkbox)))

    box = page.locator("input[type='checkbox']")
    box.click()
    wait_until(lambda: checkbox.value, page)
    checkbox.value = False
    expect(box).not_to_be_checked()


def test_compiled_visible_toggle(page):
    button = Button(label="Run")
    serve_component(page, Compiled(Column(Row(button))))

    expect(page.locator(".MuiButton-root")).to_be_visible()
    button.visible = False
    expect(page.locator(".MuiButton-root")).to_be_hidden()
    button.visible = True
    expect(page.locator(".MuiButton-root")).to_be_visible()


def test_compiled_add_and_remove_children(page):
    inner = Column(Button(label="A"))
    serve_component(page, Compiled(Column(Row(inner))))

    buttons = page.locator(".MuiButton-root")
    expect(buttons).to_have_count(1)
    added = Button(label="B")
    inner.append(added)
    expect(buttons).to_have_count(2)
    added.label = "C"
    expect(buttons.nth(1)).to_have_text("C")
    inner.remove(added)
    expect(buttons).to_have_count(1)


def test_compiled_fallback_children(page):
    inner = Column(pn.pane.Markdown("classic one", css_classes=["one"]))
    serve_component(page, Compiled(Column(Row(inner), Button(label="Run"))))

    expect(page.locator(".one p")).to_have_text("classic one")
    inner.append(pn.pane.Markdown("classic two", css_classes=["two"]))
    expect(page.locator(".two p")).to_have_text("classic two")
    expect(page.locator(".one p")).to_have_text("classic one")
    expect(page.locator(".MuiButton-root")).to_have_count(1)


def test_compiled_layout_change_rebuilds(page):
    button = Button(label="Run", width=120)
    other = Button(label="Other")
    serve_component(page, Compiled(Column(Row(button, other))))

    buttons = page.locator(".MuiButton-root")
    expect(buttons).to_have_count(2)
    button.width = 300
    wait_until(lambda: buttons.nth(0).bounding_box()["width"] > 250, page)
    other.label = "Renamed"
    expect(buttons.nth(1)).to_have_text("Renamed")


def test_compiled_recovers_from_missed_patches(page):
    button = Button(label="Run")
    compiled = Compiled(Column(Row(button)))
    serve_component(page, compiled)

    expect(page.locator(".MuiButton-root")).to_have_text("Run")
    # Skips a revision, as if a patch had been sent before the view listened.
    compiled._rev += 1
    button.label = "Missed"
    expect(page.locator(".MuiButton-root")).to_have_text("Missed")


def test_compiled_page(page):
    status = Typography("clicks: 0", css_classes=["status"])
    button = Button(label="Run")
    button.on_click(lambda event: status.param.update(object=f"clicks: {button.clicks}"))
    serve_component(page, Compiled(Page(main=[status, button], sidebar=[Checkbox(label="On")], title="Compiled page")))

    expect(page.locator(".title")).to_have_text("Compiled page")
    expect(page.locator("input[type='checkbox']")).to_have_count(1)
    page.locator(".MuiButton-root").click()
    expect(page.locator(".status")).to_contain_text("clicks: 1")


def test_compiled_focus(page):
    text = TextInput(label="Name")
    serve_component(page, Compiled(Column(Button(label="Run"), text)))
    expect(page.locator(".MuiInputBase-input")).to_have_count(1)

    text.focus()

    expect(page.locator(".MuiInputBase-input")).to_be_focused()


def test_compiled_header_inverts_theme(page):
    pg = Page(header=[Button(label="Action", variant="contained")], main=[Button(label="Main", variant="contained")])
    serve_component(page, Compiled(pg))

    expect(page.get_by_role("button", name="Action")).to_have_css("background-color", "rgb(255, 255, 255)")
    expect(page.get_by_role("button", name="Main")).to_have_css("background-color", "rgb(25, 118, 210)")


class Counter(JSComponent):

    label = param.String(default="count")
    value = param.Integer(default=0)
    objects = Children()

    _compilable = True
    _esm = """
    export function render({model, el}) {
      const button = document.createElement("button")
      button.className = "counter"
      const update = () => { button.textContent = `${model.label}: ${model.value}` }
      update()
      button.onclick = () => { model.value = model.value + 1 }
      model.on(["value", "label"], update)
      model.on("msg:custom", (msg) => { button.dataset.msg = msg.text })
      const items = document.createElement("div")
      items.className = "items"
      for (const child of model.get_child("objects")) {
        const item = document.createElement("div")
        item.className = "item"
        item.append(child)
        items.append(item)
      }
      el.append(button, items)
    }
    """


class Manual(Counter):

    _compilable = True
    _render_policy = "manual"
    _esm = """
    export function render({model, el, view}) {
      const items = document.createElement("div")
      items.className = "items"
      el.append(items)
      const place = () => {
        const children = model.get_child("objects")
        items.dataset.models = model.objects.map(child => view.get_child_view(child) ? "view" : "none").join(" ")
        items.replaceChildren(...children)
      }
      place()
      model.on("objects", place)
    }
    """


class Reaching(JSComponent):

    _compilable = True
    _esm = """
    export function render({model, el}) {
      el.textContent = "reaching"
      model.setv({})
    }
    """


def test_compiled_js_component_renders_and_syncs(page):
    counter = Counter(label="hits", value=2)
    compiled = Compiled(Column(counter))
    serve_component(page, compiled)

    button = page.locator("button.counter")
    expect(button).to_have_text("hits: 2")
    assert page.evaluate("Bokeh.documents[0].all_models.size") < 12
    assert compiled.fallbacks == []

    button.click()
    wait_until(lambda: counter.value == 3, page)
    expect(button).to_have_text("hits: 3")

    counter.param.update(label="total", value=10)
    expect(button).to_have_text("total: 10")

    counter._send_msg({"text": "hello"})
    expect(button).to_have_attribute("data-msg", "hello")


def test_compiled_js_component_places_its_children(page):
    status = Typography("clicks: 0", css_classes=["status"])
    button = Button(label="Run")
    button.on_click(lambda event: status.param.update(object=f"clicks: {button.clicks}"))
    counter = Counter(objects=[button, status, pn.pane.Markdown("classic child")])
    serve_component(page, Compiled(Column(counter)))

    expect(page.locator(".item")).to_have_count(3)
    expect(page.locator(".item").nth(2)).to_contain_text("classic child")
    # The children are sealed off from the queries of the component.
    assert page.evaluate("""() => {
      const walk = (root) => {
        for (const el of root.querySelectorAll("*")) {
          if (el.classList.contains("item")) { return el.querySelectorAll("button").length }
          const found = el.shadowRoot && walk(el.shadowRoot)
          if (found != null) { return found }
        }
      }
      return walk(document)
    }""") == 0

    page.locator(".MuiButton-root").click()
    expect(page.locator(".status")).to_contain_text("clicks: 1")
    assert page.locator(".MuiButton-root").evaluate("el => getComputedStyle(el).backgroundColor") != "rgba(0, 0, 0, 0)"


def test_compiled_js_component_rerenders_when_its_children_change(page):
    counter = Counter(objects=[Button(label="A")], value=4)
    serve_component(page, Compiled(Column(counter)))

    expect(page.locator(".item")).to_have_count(1)
    counter.objects = [*counter.objects, Button(label="B"), pn.pane.Markdown("classic child")]
    expect(page.locator(".item")).to_have_count(3)
    expect(page.locator(".MuiButton-root")).to_have_count(2)
    expect(page.locator(".item").nth(2)).to_contain_text("classic child")
    expect(page.locator("button.counter")).to_have_text("count: 4")


def test_compiled_js_component_with_manual_children(page):
    manual = Manual(objects=[Button(label="A")])
    serve_component(page, Compiled(Column(manual)))

    expect(page.locator(".MuiButton-root")).to_have_count(1)
    manual.objects = [*manual.objects, Button(label="B")]
    expect(page.locator(".MuiButton-root")).to_have_count(2)
    expect(page.locator(".items")).to_have_attribute("data-models", "view view")


def test_compiled_js_component_falls_back_on_what_it_cannot_provide(page):
    reaching = Reaching()
    compiled = Compiled(Column(reaching, Button(label="Run")))
    serve_component(page, compiled)

    wait_until(lambda: compiled.fallbacks == [reaching], page)
    expect(page.locator(".MuiButton-root")).to_have_text("Run")
