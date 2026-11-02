```python
import panel as pn
from panel_material_ui import Button, Column, IconButton, Popup

pn.extension()
```

The `Popup` component displays content in an anchored overlay that requires user interaction. It is commonly used for contextual menus, confirmations, forms, or any UI element that should appear relative to another component or screen position.

#### Parameters

For more details on customization, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`open`** (`boolean`): Whether the popup is visible.
* **`close_on_click`** (`boolean`): Whether clicking outside the popup should close it.
* **`enforce_focus`** (`boolean`): Whether focus is locked inside the popup while open.
* **`hide_backdrop`** (`boolean`): Whether to hide the backdrop behind the popup.

##### Positioning

* **`anchor_origin`** (`dict`): The vertical and horizontal alignment relative to the anchor (default: `{"horizontal": "right", "vertical": "bottom"}`).
* **`anchor_position`** (`XYCoordinates`): Absolute x/y coordinates to anchor the popup to.
* **`elevation`** (`int`): Elevation level of the popup surface.

##### Styling

* **`sx`** (`dict`): Component-level styling options.
* **`theme_config`** (`dict`): Theming options.

---

### Basic Usage

The `Popup` can be programmatically opened and closed by setting the `open` parameter:


```python
open = Button(label='Open')
close = Button(label='Close')

popup = Popup('# This is a popup', close, open=True)

open.js_on_click(args={'popup': popup}, code="popup.data.open = true")
close.js_on_click(args={'popup': popup}, code="popup.data.open = false")

Column(open, popup).preview(height=200, width=400)
```

Here we set up a `jslink` to toggle `open` but you can toggle it programmatically:

```python
popup.open = True
```

### Positioning

By default the component is anchored to its parent element, alternatively it can be `attached` to another element:


```python
popup = Popup("# An anchored Popup", open=True)
help_button = IconButton(icon="help", attached=[popup])

help_button.js_on_click(args={'popup': popup}, code="popup.data.open = true")

help_button.preview(width=400, height=200)
```

Alternatively, we can also define an absolute position using the `anchor_position` argument, a tuple of the `(vertical, horizontal)` position:


```python
popup = Popup("### Absolute position popup", open=True, anchor_position=(60, 120))

popup.preview(width=500, height=200)
```

### Anchor & Transform Origin

The `anchor_origin` determines which part of the anchor element the popup aligns to and the `transform_origin` the point on the popup which will attach to the anchor's origin:


```python
popup = Popup(
    "### Bottom-left anchored popup",
    open=True,
    anchor_origin={"horizontal": "left", "vertical": "bottom"},
    transform_origin={"horizontal": "right", "vertical": "center"}
)

anchor_btn = IconButton(icon="info", attached=[popup], styles={"margin-left": "auto"})

anchor_btn.js_on_click(args={'popup': popup}, code="popup.data.open = true")

anchor_btn.preview(width=400, height=200)
```

### References

**Material UI Popover:**

- [Material UI Popover Reference](https://mui.com/material-ui/react-popover) - Complete documentation for the underlying Material UI component
- [Material UI Popover API](https://mui.com/material-ui/api/popover/) - Detailed API reference and configuration options
