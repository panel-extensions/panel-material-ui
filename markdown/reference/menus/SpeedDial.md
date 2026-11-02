```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `SpeedDial` component is part of the `Menu` family of components. `Menu` components provide a structured way for users to navigate or choose between a series of defined items. In the case of `SpeedDial`, these items represent a series of menu options.

Each item in the `SpeedDial` list is defined by a dictionary with several supported keys:

## Item Structure

Each item can include the following keys:

- **`label`** (str, required): The text displayed for the breadcrumb item.
- **`icon`** (str, optional): An icon to display next to the label.
- **`avatar`** (str, optional): An avatar or image to show beside the label.
- **`secondary`** (str, optional): The secondary text, e.g. for describing the item.
- **`color`** (str, optional): The color of the list item

These dictionaries are passed to the component via the items parameter as a list. When one of the `items` is selected it will be available on the `value` parameter.

Since only the allowed keys are synced with the frontend, other information can be stored in the item dictionaries.

## Parameters:

### Core

* **`active`** (`int`): The index of the selected item.
* **`disabled`** (`boolean`): Whether the menu is disabled.
* **`items`** (`list`): Menu items to select from.
* **`value`** (`dict`): The currently selected item.

##### Display

* **`color`** (`str`): The color variant of the dial, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`direction`** (`Literal["right", "left", "up", "down"]`): The direction the menu opens in.
* **`icon`** (`str`): The icon to display when the menu is closed.
* **`open_icon`** (`str`): The icon to display when the menu is open.
* **`size`** (`Literal["small", "medium", "large"]`): Controls the size of the widget.

##### Styling

- **`sx`** (`dict`): Component level styling API.
- **`theme_config`** (`dict`): Theming API.

---


```python
speed_dial = pmui.SpeedDial(items=[
    {'label': 'Camera', 'icon': 'camera'},
    {'label': 'Photos', 'icon': 'photo'},
    {'label': 'Documents', 'icon': 'article'},
], active=2, margin=(50, 20))

speed_dial
```

Clicking on a particular item will highlight it and set both `active` and `value` parameters:


```python
speed_dial.value
```

## Display Options

### `color`


```python
pmui.Row(*(
    speed_dial.clone(color=color)
    for color in pmui.SpeedDial.param.color.objects
))
```

### `direction`


```python
pmui.Row(*(
    speed_dial.clone(direction=direction)
    for direction in pmui.SpeedDial.param.direction.objects
))
```

### `persistent_tooltips`


```python
pmui.Column(speed_dial.clone(persistent_tooltips=True, direction='down', margin=(20, 180)), height=260)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Explore"},
    {"label": ":material/zoom_out_map: Inspect"},
]

pmui.SpeedDial(
    label=":material/zoom_out_map: Tools",
    items=items,
    active=0,
    margin=(50, 20),
)
```

### API Reference

#### Parameters

The `SpeedDial` exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.SpeedDial(items=[
    {'label': 'Open', 'icon': 'description'},
    {'label': 'Save', 'icon': 'save'},
    {'label': 'Exit', 'icon': 'close'},
], label='File').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI SpeedDial:**

- [Material UI SpeedDial Reference](https://mui.com/material-ui/react-speed-dial) - Complete documentation for the underlying Material UI component
- [Material UI SpeedDial API](https://mui.com/material-ui/api/speed-dial/) - Detailed API reference and configuration options
