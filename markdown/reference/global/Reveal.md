```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Reveal` scrolls to the elements on the page that carry a CSS class and briefly outlines them, e.g. to point users at the cards that failed or need their input.

It renders nothing itself: place it anywhere in your app and call `scroll_to` with a CSS class. Elements are found across Panel's shadow roots, so the class can sit on any component, however deeply nested. Users who prefer reduced motion get an instant jump and an outline without a fade.

#### Parameters:

##### Core

* **`color`** (str): The theme color of the outline, one of 'default', 'primary' (default), 'secondary', 'error', 'info', 'success', 'warning', 'light' or 'dark'.
* **`duration`** (int): Milliseconds the outline is shown before it fades. Default is 2200.

#### Methods:

* **`scroll_to(css_class, highlight=True, focus=False, block="center")`**: Scroll to the first element carrying `css_class` and outline every one. With `focus=True` keyboard focus moves to the first element, so screen reader users land on it too. `block` sets where it is aligned: 'start', 'center', 'end' or 'nearest'.

___

### Basic Usage

Mark the elements with `css_classes` and call `scroll_to`. The class may be added in the same callback as the request:


```python
reveal = pmui.Reveal(color="error")

cards = [
    pmui.Card(pmui.Typography(f"Job {i} finished"), title=f"Job {i}", collapsible=False, width=300)
    for i in range(12)
]

def show_failures(_):
    for i, card in enumerate(cards):
        card.css_classes = ["failed"] if i in (7, 10) else []
    reveal.scroll_to("failed")

button = pmui.Button(label="Show failures", color="error", on_click=show_failures)

pmui.Column(reveal, button, pmui.Column(*cards, height=400, scroll=True))
```

### Scrolling Without Highlighting

Pass `highlight=False` to only scroll, and `focus=True` to move keyboard focus to the first element:


```python
reveal = pmui.Reveal()

sections = [
    pmui.Paper(pmui.Typography(f"Section {i}", variant="h6"), height=150, css_classes=[f"section-{i}"])
    for i in range(6)
]
jump = pmui.Select(label="Jump to", options=[f"section-{i}" for i in range(6)])
jump.param.watch(lambda event: reveal.scroll_to(event.new, highlight=False, focus=True, block="start"), "value")

pmui.Column(reveal, jump, pmui.Column(*sections, height=400, scroll=True))
```

### API Reference

#### Parameters


```python
pmui.Reveal().api(jslink=True)
```

### References

**Panel Material UI:**

- [Fullscreen](../wrappers/Fullscreen.ipynb) - Show a component in full screen

**Web APIs:**

- [Element.scrollIntoView()](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView)
- [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
