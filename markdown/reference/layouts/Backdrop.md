```python
import panel as pn
from panel_material_ui import Backdrop, Button, Column

pn.extension()
```

The Backdrop signals a state change within the application and can be used for creating loaders, dialogs, and more. In its simplest form, the Backdrop component will add a dimmed layer over your application.

## Parameters:

### Core

* **`open`** (`boolean`): Whether the backdrop is visible.

---

The `Backdrop` can be opened and closed programmatically by setting the `open` parameter:


```python
open = Button(label='Open')
close = Button(label='Close')

dialog = Backdrop(close)

open.js_on_click(args={'dialog': dialog}, code="dialog.data.open = true")
close.js_on_click(args={'dialog': dialog}, code="dialog.data.open = false")

Column(open, dialog).preview()
```
