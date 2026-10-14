```python
import panel as pn
from panel_material_ui import Button, Column, Dialog

pn.extension()
```

The `Dialog` component creates modal dialogs for important content or actions.

#### Parameters

For more details on customization, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`close_on_click`** (`boolean`): Whether a click outside the Dialog area should close it.
* **`full_screen`** (`boolean`): Whether the dialog takes up the full screen.
* **`open`** (`boolean`): Whether the dialog is visible.
* **`title`** (`str`): Header text for the dialog.

##### Display

* **`scroll`** (`Literal["body", "paper"]`): Whether the dialog should scroll the content or the paper.
* **`show_close_button`** (`boolean`): Whether the dialog shows a close button.
* **`title_variant`** (`str`): The text variant of the dialog title (default="h3").
* **`width_option`** (`Literal["xs", "sm", "md", "lg", "xl", False]`): Maximum width breakpoint for the container.

##### Styling

- **`sx`** (dict): Component-level styling options.
- **`theme_config`** (dict): Theming options.

---

### Basic Usage

The `Dialog` can be programmatically opened and closed by setting the `open` parameter:


```python
open = Button(label='Open')
close = Button(label='Close')

dialog = Dialog('# This is a dialog', close)

open.js_on_click(args={'dialog': dialog}, code="dialog.data.open = true")
close.js_on_click(args={'dialog': dialog}, code="dialog.data.open = false")

Column(open, dialog).preview()
```

Here we set up a `jslink` to toggle `open` but you can toggle it programmatically:

```python
dialog.open = True
```

### Close Behavior

The Dialog can be toggled open and closed with the `open` parameter, additionally you can enable `close_on_click` and `show_close_button` options. The former automatically closes the modal when clicking outside it's area, while the latter will display a close button in the top-right:


```python
open = Button(label='Open')
close = Button(label='Close')

dialog = Dialog('# This is a dialog', close_on_click=True, show_close_button=True)

open.js_on_click(args={'dialog': dialog}, code="dialog.data.open = true")

Column(open, dialog).preview()
```

### Full Screen

It can also be rendered in full screen:


```python
open = Button(label='Open')
close = Button(label='Close')

dialog = Dialog(close, full_screen=True)

open.js_on_click(args={'dialog': dialog}, code="dialog.data.open = true")
close.js_on_click(args={'dialog': dialog}, code="dialog.data.open = false")

Column(open, dialog).preview()
```

### Width

Lastly, we can control the maximum size of the `Dialog` with the `width_option` and if we want also force it to always take on that size by setting the `sizing_mode`:


```python
open = Button(label='Open')
close = Button(label='Close')

dialog = Dialog(close, sizing_mode='stretch_width', width_option='lg')

open.js_on_click(args={'dialog': dialog}, code="dialog.data.open = true")
close.js_on_click(args={'dialog': dialog}, code="dialog.data.open = false")

Column(open, dialog).preview()
```

### References

**Material UI Dialog:**

- [Material UI Dialog Reference](https://mui.com/material-ui/react-dialog) - Complete documentation for the underlying Material UI component
- [Material UI Dialog API](https://mui.com/material-ui/api/dialog/) - Detailed API reference and configuration options
