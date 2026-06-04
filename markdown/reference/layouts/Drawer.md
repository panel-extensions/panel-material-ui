```python
import panel as pn
from panel_material_ui import Button, Container, Drawer, Row

pn.extension()
```

The `Drawer` component (akin to a sidebar) provides ergonomic access to destinations in a site or app functionality.

## Parameters:
For details on other options for customizing the component see the layout and styling how-to guides.

### Core

* **`open`** (`boolean`): Whether the `Drawer` is open.

### Display

* **`anchor`** (`Literal["left", "right", "bottom", "right"]`): Where to position the `Drawer`.
* **`size`** (`int`): The width or height depending on whether the `Drawer` is rendered on the left/right or top/bottom respectively.
* **`variant`** (`Literal["temporary", "persistent", "permanent"]`): Whether the Drawer is temporary, persistent or permanent.

---

Temporary navigation drawers can toggle open or closed. Closed by default, the drawer opens temporarily above all other content until a section is selected.

The `Drawer` can be cancelled by clicking the overlay or pressing the Esc key. It closes when an item is selected, handled by controlling the `open` parameter.


```python
drawer = Drawer("I'm in a Drawer", size=300)

button = Button(label='Open Drawer')

button.js_on_click(args={'drawer': drawer}, code='drawer.data.open = true')

Container(button, drawer).preview()
```

`Drawer` also provides the `create_toggle` helper method to create a toggle that controls the `open` state of the drawer:


```python
drawer = Drawer("# My Drawer")

toggle = drawer.create_toggle(align='end')

Container(drawer, toggle, width_option='sm').preview()
```

### Anchor

Use the `anchor` parameter to specify which side of the screen the `Drawer` should originate from (the default value is `left`).


```python
container = Row()
for anchor in Drawer.param.anchor.objects:
    drawer = Drawer(f"I'm in a Drawer on the {anchor}", size=300, anchor=anchor)
    button = Button(label=anchor.upper(), width=100)
    button.js_on_click(args={'drawer': drawer}, code='drawer.data.open = true')
    container.extend([button, drawer])

container.preview()
```

### Persistent drawer

Persistent navigation drawers can toggle open or closed, but unlike a `temporary` they sit at the same elevation at the content and participate in the document flow.

This means that the `Drawer` should be placed in the correct place in the display hierarchy:


```python
drawer = Drawer("## I'm in a Drawer", size=300, variant="persistent")

button = drawer.create_toggle(styles={'margin-left': 'auto'})
content = Row('# Title', button, sizing_mode='stretch_width')

Row(
    drawer, Container(content, width_option='sm'),
).preview()
```


```python

```
