```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Clickable` wrapper adds click interaction to any child component. It wraps a single child element with a clickable area, providing a `clicks` counter and an `on_click` callback mechanism. Optionally renders a Material UI ripple effect on click.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`object`** (Viewable): The child component to wrap.
* **`clicks`** (int): Number of clicks. Increments each time the component is clicked.
* **`disabled`** (bool): Whether the clickable area is disabled. Default is False.

##### Display

* **`disable_ripple`** (bool): Whether to disable the ripple effect on click. Default is False.

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization.
- **`theme_config`** (dict): Theming API for consistent design system integration.

___

### Basic Usage

Wrap any component to make it clickable:


```python
clickable = pmui.Clickable(
    pmui.Card(
        title="Click me!", elevation=3, width=200, height=100, collapsible=False
    )
)

clickable
```

### Click Counter

The `clicks` parameter increments each time the wrapped element is clicked:


```python
clickable.clicks
```

### Callback

Use `on_click` to register a callback, either as a constructor argument or method call:


```python
status = pmui.Typography("Not clicked yet")

clickable = pmui.Clickable(
    pmui.Card(title="Click this card", height=100, width=250),
    on_click=lambda e: status.param.update(object=f"Clicked {e.new} times")
)

pmui.Column(clickable, status)
```

### Disable Ripple

Set `disable_ripple=True` to remove the ripple animation on click while keeping the click behavior:


```python
pmui.Row(
    pmui.Clickable(
        pmui.Paper(pmui.Column(pn.pane.Str("With ripple")), elevation=2, width=150, height=80),
    ),
    pmui.Clickable(
        pmui.Paper(pmui.Column(pn.pane.Str("No ripple")), elevation=2, width=150, height=80),
        disable_ripple=True,
    ),
)
```

### Disabled

Set `disabled=True` to prevent clicks:


```python
pmui.Clickable(
    pmui.Paper(pmui.Column(pn.pane.Str("Can't click me")), elevation=2, width=200, height=80),
    disabled=True,
)
```

### Responsive Sizing

When the wrapped component uses a responsive `sizing_mode`, set the same on the `Clickable` so the child fills the available space:


```python
pmui.Clickable(
    pmui.Paper(
        pmui.Column(pn.pane.Str("Full width clickable area")),
        elevation=2, sizing_mode="stretch_width", height=80
    ),
    sizing_mode="stretch_width",
)
```
