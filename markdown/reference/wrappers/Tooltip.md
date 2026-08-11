```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Tooltip` displays informative text when users hover over, focus on, or tap a child element. It wraps a single child component and shows a configurable label.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`object`** (Viewable): The child component to wrap with the tooltip.
* **`open`** (bool or None): Explicitly control whether the tooltip is open. When None (default), the tooltip is managed automatically on hover/focus. Set to True or False for programmatic control.
* **`title`** (str): The text to display inside the tooltip.

##### Display

* **`arrow`** (bool): Whether the tooltip has an arrow indicating the element it refers to. Default is False.
* **`describe_child`** (bool): Whether the tooltip acts as an accessible description rather than a label. Use when the child already has a visible label and the tooltip provides supplementary information. Default is False.
* **`enter_delay`** (int): The number of milliseconds to wait before showing the tooltip. This can help avoid tooltips appearing on quick mouse passes. Default is 100.
* **`follow_cursor`** (bool): Whether the tooltip follows the cursor position. Default is False.
* **`leave_delay`** (int): The number of milliseconds to wait before hiding the tooltip. Default is 0.
* **`placement`** (str): The placement of the tooltip relative to the child element - options include 'top', 'bottom' (default), 'left', 'right', and variants with '-start' or '-end' suffixes.

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

___

### Basic Usage

Wrap any component and provide a `title` to create a tooltip:


```python
pmui.Tooltip(pmui.Button(label="Delete", icon="delete"), title="Remove this item")
```

### Arrow

Use the `arrow` parameter to add an arrow pointing to the child element:


```python
pmui.Tooltip(pmui.Button(label="Save"), title="Save your progress", arrow=True)
```

### Placement

The tooltip supports 12 placement options:


```python
pmui.Column(
    pmui.Row(
        pmui.Tooltip(pmui.Button(label="Top Start"), title="top-start", placement="top-start"),
        pmui.Tooltip(pmui.Button(label="Top"), title="top", placement="top"),
        pmui.Tooltip(pmui.Button(label="Top End"), title="top-end", placement="top-end"),
    ),
    pmui.Row(
        pmui.Tooltip(pmui.Button(label="Left"), title="left", placement="left"),
        pmui.Tooltip(pmui.Button(label="Right"), title="right", placement="right"),
    ),
    pmui.Row(
        pmui.Tooltip(pmui.Button(label="Bottom Start"), title="bottom-start", placement="bottom-start"),
        pmui.Tooltip(pmui.Button(label="Bottom"), title="bottom", placement="bottom"),
        pmui.Tooltip(pmui.Button(label="Bottom End"), title="bottom-end", placement="bottom-end"),
    ),
)
```

### Follow Cursor

Set `follow_cursor=True` to have the tooltip track the mouse position:


```python
pmui.Tooltip(
    pmui.Button(label="Hover and move", variant="outlined"),
    title="I follow your cursor",
    follow_cursor=True,
)
```

### Delay

Control how quickly the tooltip appears and disappears:


```python
pmui.Row(
    pmui.Tooltip(pmui.Button(label="Instant"), title="No delay", enter_delay=0),
    pmui.Tooltip(pmui.Button(label="Slow"), title="500ms delay", enter_delay=500),
    pmui.Tooltip(pmui.Button(label="Lingering"), title="Stays 1s", leave_delay=1000),
)
```

### Controlled Tooltip

Use the `open` parameter for programmatic control:


```python
toggle = pmui.Switch(value=True, label="Show Tooltip")

tooltip = pmui.Tooltip(
    pmui.Button(label="Controlled"),
    title="Programmatically opened",
    open=toggle, placement="right"
)

pmui.Column(tooltip, toggle)
```

### Accessible Description

When the child element already has a label, use `describe_child=True` so the tooltip acts as a description rather than a label:


```python
pmui.Row(
    pmui.Tooltip(pmui.IconButton(icon="delete"), title="Delete"),
    pmui.Tooltip(
        pmui.Button(label="Add"),
        title="Does not add if it already exists.",
        describe_child=True,
    ),
)
```

### Responsive Sizing

When the wrapped component uses a responsive `sizing_mode` (e.g. `"stretch_width"`), set the same on the `Tooltip` so the child fills the available width; otherwise the tooltip hugs the child's intrinsic size.


```python
pmui.Column(
    pmui.Tooltip(
        pmui.Button(label="Stretches to full width", variant="contained", sizing_mode="stretch_width"),
        title="Full-width button",
        sizing_mode="stretch_width",
    ),
    sizing_mode="stretch_width",
)
```
