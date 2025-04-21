# Drawer

The navigation `Drawer` (or "sidebars") provide ergonomic access to destinations in a site or app functionality such as switching accounts

```python
import panel as pn
import panel_material_ui as pmu
from panel_material_ui import Drawer, Alert
import param

pn.extension()
```

## API

The `Drawer` is built on top of the [Material UI `Drawer`](https://mui.com/material-ui/react-drawer/) and mimics its API.

### Parameters

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

#### Core

* **`*objects`: Positional arguments to view.
* **`anchor`** (str): Specifies which side of the screen the `Drawer` should originate from. One of `left` (default), `right`, `top` or `bottom`.
* **`variant`** (str): How to display the drawer. One of `temporary` (default) or `persistent`.

#### Styling

* **`sx`** (dict): Component‑level styling API.
* **`theme_config`** (dict): Theming API.

## Temporary Drawer

```python
drawer = Drawer(pmu.Divider(sizing_mode="stretch_width"), "## Settings", pmu.FloatSlider(name="Value", value=4, color="primary"))

def open_drawer(event):
    drawer.open = True

open_button = pmu.Button(name="Open Drawer", on_click=open_drawer, margin=(20,5,10,5), color="primary", variant="outlined")

def close_drawer(event):
    drawer.open = False

close_button = pmu.Button(name="Close Drawer", on_click=close_drawer, width=300, color="primary")
drawer.insert(0, close_button)

pn.Column(drawer, open_button).servable()
```

You may press ESC or click outside the drawer to close is.

## Anchor

Use the `anchor` parameter to specify which side of the screen the `Drawer` should originate from.

The default value is `left`.

```python
pn.Row(pmu.RadioButtonGroup.from_param(drawer.param.anchor), open_button).servable()
```

## Variant

The default value is `temporary`.

```python
pn.Row(pmu.RadioButtonGroup.from_param(drawer.param.variant), open_button).servable()
```

## Width

The width of the `Drawer` can be controlled via the maximum width of its child objects.

```python
pn.Row(pmu.IntSlider.from_param(close_button.param.width, start=300, end=600, step=100, margin=(10, 20, 10, 10)), open_button).servable()
```

We recommend controlling the `width` by using a `Column`

```.py
Drawer(pn.Column(
    pmu.Divider(sizing_mode="stretch_width"), "## Settings", pmu.FloatSlider(name="Value", value=4, color="primary")
), width=400)
```

Alternatively its possible to control the width via the `sx` style parameter.

```.py
drawer.sx={
    "& .MuiPaper-root": {"width": "500px"}
}
```

## JS Linking

DESCRIBE HOW TO JS_LINK A BUTTON OR BUTTONICON TO THE DRAWER.OPEN PROPERTY
